from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = Path(__file__).parent.parent / 'uploads'
DATA_FOLDER = Path(__file__).parent.parent / 'data'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'webm'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

# Ensure directories exist
UPLOAD_FOLDER.mkdir(exist_ok=True)
DATA_FOLDER.mkdir(exist_ok=True)
(DATA_FOLDER / 'raw').mkdir(exist_ok=True)
(DATA_FOLDER / 'processed').mkdir(exist_ok=True)

app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "services": {
            "video_upload": True,
            "content_generation": True,
            "pattern_extraction": True
        }
    }), 200


@app.route('/api/upload-video', methods=['POST'])
def upload_video():
    """
    Upload video file for analysis
    Expects: multipart/form-data with 'video' file and optional 'context' text
    """
    try:
        # Check if video file is present
        if 'video' not in request.files:
            return jsonify({"error": "No video file provided"}), 400
        
        file = request.files['video']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                "error": f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # Get optional context
        context = request.form.get('context', '')
        
        # Save the file
        filename = secure_filename(file.filename)
        timestamp = int(Path(filename).stem.split('-')[-1]) if '-' in filename else ''
        unique_filename = f"video-{timestamp or 'upload'}-{filename}"
        filepath = Path(app.config['UPLOAD_FOLDER']) / unique_filename
        
        file.save(str(filepath))
        
        # Call Node.js video analyzer
        result = analyze_video_with_node(str(filepath), context)
        
        return jsonify({
            "success": True,
            "filename": unique_filename,
            "filepath": str(filepath),
            "context": context,
            "analysis": result,
            "message": "Video uploaded and analyzed successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def analyze_video_with_node(video_path, context=""):
    """
    Call Node.js video analyzer script
    """
    try:
        node_script = Path(__file__).parent / 'video' / 'video-analyzer.cjs'
        
        # Run the Node.js analyzer
        result = subprocess.run(
            ['node', str(node_script), video_path, context],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"raw_output": result.stdout}
        else:
            return {"error": result.stderr or "Video analysis failed"}
            
    except subprocess.TimeoutExpired:
        return {"error": "Video analysis timed out"}
    except Exception as e:
        return {"error": f"Analysis error: {str(e)}"}


@app.route('/api/generate-post', methods=['POST'])
def generate_post():
    """
    Generate LinkedIn post from context
    Expects JSON: { "context": "...", "style": "professional|inspirational|...", "video_analysis": {...} }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        context = data.get('context', '').strip()
        style = data.get('style', 'professional').strip()
        video_analysis = data.get('video_analysis', {})
        
        if not context and not video_analysis:
            return jsonify({"error": "Either context or video_analysis is required"}), 400
        
        print(f"\n🎨 [POST GENERATION] Request received")
        print(f"   → Style: {style}")
        print(f"   → Context: {context[:100]}...")
        
        # Map serious to professional for file lookup
        dataset_name = 'professional' if style == 'serious' else style
        
        # Check if patterns exist for this style
        patterns = {}
        patterns_file = DATA_FOLDER / 'processed' / f'patterns_{dataset_name}.json'
        
        if not patterns_file.exists():
            print(f"   ⚠️ Patterns not found for {style}, extracting...")
            # Extract patterns first
            dataset_path = DATA_FOLDER / 'raw' / f'{dataset_name}.json'
            
            if dataset_path.exists():
                result = subprocess.run(
                    ['python', 'backend/extractpatterns.py', str(dataset_path), str(patterns_file)],
                    capture_output=True,
                    text=True,
                    cwd=Path(__file__).parent.parent
                )
                
                if result.returncode == 0:
                    print(f"   ✅ Patterns extracted successfully")
                else:
                    print(f"   ⚠️ Pattern extraction failed: {result.stderr}")
        
        # Load patterns
        if patterns_file.exists():
            with open(patterns_file, 'r', encoding='utf-8') as f:
                patterns = json.load(f)
            print(f"   ✅ Patterns loaded for {style}")
        else:
            print(f"   ⚠️ No patterns available, using default generation")
        
        # Generate post using patterns and context
        print(f"   🚀 Generating post...")
        post = generate_linkedin_post(context, style, video_analysis, patterns)
        print(f"   ✅ Post generated successfully!")
        
        return jsonify({
            "success": True,
            "post": post,
            "style": style,
            "patterns_used": bool(patterns)
        }), 200
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


def generate_linkedin_post(context, style, video_analysis, patterns):
    """
    Generate a LinkedIn post using extracted patterns and context
    """
    # Import the generator module
    from generator import generate_linkedin_post as generate_post
    
    # Build full context from video if available
    full_context = context
    if video_analysis:
        if 'description' in video_analysis:
            full_context += f"\n\nVideo context: {video_analysis['description']}"
        if 'key_moments' in video_analysis:
            full_context += f"\n\nKey moments: {', '.join(video_analysis['key_moments'])}"
    
    # Generate post using the new generator
    post_data = generate_post(full_context, style, patterns)
    
    return post_data


@app.route('/api/extract-patterns', methods=['POST'])
def extract_patterns():
    """
    Extract writing patterns from uploaded JSON dataset
    Expects JSON: { "dataset_name": "boardy" }
    """
    try:
        data = request.json
        dataset_name = data.get('dataset_name', 'boardy')
        original_name = dataset_name
        
        print(f"\n🔍 [PATTERN EXTRACTION] Request received for: {dataset_name}")
        
        # Map "serious" to "professional" dataset
        if dataset_name == 'serious':
            dataset_name = 'professional'
            print(f"   → Mapped 'serious' to 'professional'")
        
        # Path to the dataset
        dataset_path = DATA_FOLDER / 'raw' / f'{dataset_name}.json'
        print(f"   → Dataset path: {dataset_path}")
        
        if not dataset_path.exists():
            print(f"   ❌ Dataset not found: {dataset_path}")
            return jsonify({"error": f"Dataset {dataset_name}.json not found"}), 404
        
        # Run pattern extraction
        output_path = DATA_FOLDER / 'processed' / f'patterns_{dataset_name}.json'
        print(f"   → Output path: {output_path}")
        print(f"   🚀 Running extractpatterns.py...")
        
        result = subprocess.run(
            ['python', 'backend/extractpatterns.py', str(dataset_path), str(output_path)],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        if result.returncode == 0:
            print(f"   ✅ Extraction completed successfully!")
            
            with open(output_path, 'r') as f:
                patterns = json.load(f)
            
            print(f"   📊 Patterns loaded: {len(patterns.get('opening_patterns', []))} openings, "
                  f"{len(patterns.get('common_phrases', []))} phrases")
            print(f"   ✅ Response sent to frontend\n")
            
            return jsonify({
                "success": True,
                "patterns": patterns,
                "dataset": original_name,
                "message": f"Patterns extracted successfully from {dataset_name}.json"
            }), 200
        else:
            print(f"   ❌ Extraction failed!")
            print(f"   STDERR: {result.stderr}")
            return jsonify({"error": result.stderr}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/datasets', methods=['GET'])
def list_datasets():
    """List available datasets in data/raw/"""
    try:
        raw_folder = DATA_FOLDER / 'raw'
        datasets = [f.stem for f in raw_folder.glob('*.json')]
        
        return jsonify({
            "datasets": datasets,
            "count": len(datasets)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/patterns', methods=['GET'])
def get_patterns():
    """Get extracted patterns"""
    try:
        patterns_file = DATA_FOLDER / 'processed' / 'patterns.json'
        
        if not patterns_file.exists():
            return jsonify({"error": "No patterns found. Run extraction first."}), 404
        
        with open(patterns_file, 'r') as f:
            patterns = json.load(f)
        
        return jsonify(patterns), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Serve uploaded videos (for preview)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded video files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"📁 Data folder: {DATA_FOLDER}")
    print(f"🌐 Server running on http://localhost:5001")
    print(f"📝 API docs: backend/API_GUIDE.md")
    
    app.run(debug=True, host='0.0.0.0', port=5001)

