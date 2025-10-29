import json
import re
import os

def load_posts(filename):
    """
    Load posts from a JSON file.
    
    Args:
        filename (str): Path to the JSON file containing posts.

    Returns:
        list[dict]: List of posts as dictionaries.
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    # Construct full path relative to this script
    filepath = os.path.join(script_dir, filename)
    # Load JSON data
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_summary(posts):
    """
    Summarize key attributes from posts in a Gemini-friendly format.
    
    Extracts important fields and creates a short text snippet for each post.
    Handles multiple possible key names to avoid nulls.
    
    Args:
        posts (list[dict]): List of post dictionaries.

    Returns:
        list[dict]: List of summarized post dictionaries.
    """
    summaries = []
    for post in posts:
        # Flexible key lookup to prevent nulls
        text = post.get('generated_post_text') or post.get('full_post_text') or ''
        hashtags = post.get('key_hashtags') or post.get('hashtags') or []
        style = post.get('style_preset') or post.get('style') or ''
        theme = post.get('original_context') or post.get('primary_theme') or ''
        engagement = post.get('engagement_metrics') or post.get('engagement') or {}

        # Build Gemini-friendly summary
        summary = {
            'id': post.get('post_id') or f'post-{posts.index(post)+1}',
            'style': style,
            'theme': theme,
            # Take first 20 words as snippet for AI context
            'snippet': ' '.join(text.split()[:20]) + ('...' if len(text.split()) > 20 else ''),
            'hashtags': hashtags,
            # Count sentences by splitting on punctuation
            'sentences': len([s for s in re.split(r'[.!?]+', text) if s.strip()]),
            # Count paragraphs by double line breaks
            'paragraphs': text.count('\n\n') + 1,
            # Include engagement metrics if present
            'engagement': engagement
        }
        summaries.append(summary)
    return summaries

def overall_patterns(posts):
    """
    Summarize general patterns across all posts in a Gemini-friendly format.
    
    Calculates average length, sentences, and paragraphs across dataset.

    Args:
        posts (list[dict]): List of post dictionaries.

    Returns:
        dict: Average length, sentences, and paragraphs.
    """
    total_length = sum(len(post.get('generated_post_text') or post.get('full_post_text') or '') for post in posts)
    total_sentences = sum(len([s for s in re.split(r'[.!?]+', post.get('generated_post_text') or post.get('full_post_text') or '') if s.strip()]) for post in posts)
    total_paragraphs = sum((post.get('generated_post_text') or post.get('full_post_text') or '').count('\n\n') + 1 for post in posts)
    n = len(posts)
    return {
        # Average post length in characters
        'length': total_length / n if n else 0,
        # Average number of sentences per post
        'sentences': total_sentences / n if n else 0,
        # Average number of paragraphs per post
        'paragraphs': total_paragraphs / n if n else 0
    }

def extract_openings(posts):
    """Extract opening lines/sentences from posts"""
    openings = []
    for post in posts:
        text = post.get('generated_post_text') or post.get('full_post_text') or ''
        if text:
            # Get first sentence (split by period, question mark, or exclamation)
            first_sentence = re.split(r'[.!?]\s+', text.strip())[0]
            if first_sentence:
                openings.append(first_sentence.strip())
    return openings

def extract_sentence_starters(posts, top_n=20):
    """Extract common words that start sentences"""
    from collections import Counter
    starters = []
    
    for post in posts:
        text = post.get('generated_post_text') or post.get('full_post_text') or ''
        if text:
            # Split into sentences
            sentences = re.split(r'[.!?]\n', text)
            for sentence in sentences:
                # Get first word
                words = sentence.strip().split()
                if words:
                    first_word = words[0].lower().strip('.,!?;:')
                    if first_word and len(first_word) > 2:  # Skip very short words
                        starters.append(first_word)
    
    # Count and return top N
    counter = Counter(starters)
    return counter.most_common(top_n)

def extract_common_phrases(posts, top_n=50):
    """Extract common 2-3 word phrases"""
    from collections import Counter
    phrases = []
    
    for post in posts:
        text = post.get('generated_post_text') or post.get('full_post_text') or ''
        if text:
            # Clean and split into words
            text = text.lower()
            words = re.findall(r'\b\w+\b', text)
            
            # Extract 2-word phrases
            for i in range(len(words) - 1):
                phrase = f"{words[i]} {words[i+1]}"
                if len(words[i]) > 2 or len(words[i+1]) > 2:  # At least one substantial word
                    phrases.append(phrase)
            
            # Extract 3-word phrases
            for i in range(len(words) - 2):
                phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
                phrases.append(phrase)
    
    counter = Counter(phrases)
    return counter.most_common(top_n)

def detect_formatting_patterns(posts):
    """Detect formatting style patterns"""
    bold_count = 0
    bullet_count = 0
    emoji_count = 0
    special_chars = False
    paragraph_lengths = []
    
    for post in posts:
        text = post.get('generated_post_text') or post.get('full_post_text') or ''
        if text:
            # Count bold markers (various formats)
            bold_count += text.count('**') + text.count('𝗯') + text.count('𝘣')
            
            # Count bullets
            bullet_count += text.count('•') + text.count('➢') + text.count('→')
            
            # Count emojis (simple Unicode range check)
            emoji_count += len([c for c in text if ord(c) > 127000])
            
            # Check for special formatting characters
            if any(c in text for c in ['𝗯', '𝗶', '𝘣', '𝘪', '→', '➢', '•', '✓', '✅', '❌']):
                special_chars = True
            
            # Paragraph lengths
            paragraphs = text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    paragraph_lengths.append(len(para))
    
    return {
        'bold_usage': bold_count,
        'bullet_points': bullet_count,
        'emoji_count': emoji_count,
        'avg_paragraph_length': sum(paragraph_lengths) / len(paragraph_lengths) if paragraph_lengths else 0,
        'uses_special_characters': special_chars
    }

def detect_tone_indicators(posts):
    """Detect tone and style indicators"""
    questions = 0
    exclamations = 0
    direct_address = 0  # "you", "your"
    first_person = 0  # "I", "my", "we"
    second_person = 0
    
    for post in posts:
        text = post.get('generated_post_text') or post.get('full_post_text') or ''
        if text:
            questions += text.count('?')
            exclamations += text.count('!')
            
            text_lower = text.lower()
            direct_address += text_lower.count(' you ') + text_lower.count(' your ')
            first_person += text_lower.count(' i ') + text_lower.count(' my ') + text_lower.count(' we ')
            second_person += text_lower.count(' you ')
    
    return {
        'questions': questions,
        'exclamations': exclamations,
        'direct_address': direct_address,
        'first_person': first_person,
        'second_person': second_person
    }

def analyze_structure(posts):
    """Analyze structural patterns"""
    total_length = 0
    total_sentences = 0
    total_paragraphs = 0
    total_words = 0
    n = len(posts)
    
    for post in posts:
        text = post.get('generated_post_text') or post.get('full_post_text') or ''
        if text:
            total_length += len(text)
            
            # Count sentences
            sentences = re.split(r'[.!?]+', text)
            total_sentences += len([s for s in sentences if s.strip()])
            
            # Count paragraphs
            paragraphs = text.split('\n\n')
            total_paragraphs += len([p for p in paragraphs if p.strip()])
            
            # Count words
            words = re.findall(r'\b\w+\b', text)
            total_words += len(words)
    
    avg_sentences = total_sentences / n if n else 0
    avg_words = total_words / n if n else 0
    
    return {
        'avg_length': total_length / n if n else 0,
        'avg_sentences': avg_sentences,
        'avg_words_per_sentence': avg_words / avg_sentences if avg_sentences else 0,
        'avg_paragraphs': total_paragraphs / n if n else 0
    }

def extract_key_vocabulary(posts, top_n=30):
    """Extract most common meaningful words"""
    from collections import Counter
    
    # Common stopwords to exclude
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'been', 'be',
                 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
    
    words = []
    for post in posts:
        text = post.get('generated_post_text') or post.get('full_post_text') or ''
        if text:
            # Extract words (lowercase)
            text_words = re.findall(r'\b\w+\b', text.lower())
            for word in text_words:
                if word not in stopwords and len(word) > 3:
                    words.append(word)
    
    counter = Counter(words)
    return counter.most_common(top_n)

def extract_patterns_from_file(input_path, output_path):
    """
    Extract patterns from a JSON file and save to output path.
    
    Args:
        input_path (str): Path to input JSON file
        output_path (str): Path to save patterns JSON
    """
    # Load the posts from the given file
    with open(input_path, 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    # Extract all patterns
    patterns = {
        'opening_patterns': extract_openings(posts),
        'top_sentence_starters': extract_sentence_starters(posts),
        'common_phrases': extract_common_phrases(posts),
        'formatting_patterns': detect_formatting_patterns(posts),
        'tone_indicators': detect_tone_indicators(posts),
        'structure': analyze_structure(posts),
        'vocabulary': extract_key_vocabulary(posts)
    }
    
    # Save to output file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(patterns, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Patterns extracted and saved to: {output_path}")
    return patterns

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) >= 3:
        # Command line arguments provided (called from API)
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        patterns = extract_patterns_from_file(input_path, output_path)
    else:
        # Interactive mode (manual testing)
        filename = input("Enter the path to your JSON file: ").strip()
        output = input("Enter output path (or press enter for stdout): ").strip()
        
        if output:
            patterns = extract_patterns_from_file(filename, output)
        else:
            # Old behavior - print to stdout
            posts = load_posts(filename)
            summaries = extract_summary(posts)
            averages = overall_patterns(posts)
            ai_context = {
                'posts': summaries,
                'averages': averages
            }
            print(json.dumps(ai_context, indent=2))
