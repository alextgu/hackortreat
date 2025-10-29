const { GoogleGenerativeAI } = require('@google/generative-ai');
const fs = require('fs');
const path = require('path');

class VideoAnalyzer {
    constructor(apiKey) {
        if (!apiKey) {
            throw new Error('Gemini API key is required');
        }
        this.genAI = new GoogleGenerativeAI(apiKey);
        this.model = this.genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });
    }

    /**
     * Convert video file to base64 for Gemini API
     */
    fileToGenerativePart(filePath, mimeType) {
        return {
            inlineData: {
                data: Buffer.from(fs.readFileSync(filePath)).toString('base64'),
                mimeType
            }
        };
    }

    /**
     * Analyze video and extract outfit, activity, and background information
     */
    async analyzeVideo(videoPath) {
        try {
            console.log('📹 Analyzing video:', videoPath);

            // Determine MIME type based on file extension
            const ext = path.extname(videoPath).toLowerCase();
            const mimeTypes = {
                '.mov': 'video/quicktime',
                '.mp4': 'video/mp4',
                '.webm': 'video/webm',
                '.avi': 'video/x-msvideo'
            };
            const mimeType = mimeTypes[ext] || 'video/mp4';

            // Check file size (Gemini has limits)
            const stats = fs.statSync(videoPath);
            const fileSizeMB = stats.size / (1024 * 1024);
            console.log(`📊 Video size: ${fileSizeMB.toFixed(2)} MB`);

            if (fileSizeMB > 100) {
                throw new Error('Video file too large. Gemini supports up to ~100MB videos.');
            }

            // Prepare the video file
            const videoPart = this.fileToGenerativePart(videoPath, mimeType);

            // Craft a detailed prompt for analysis
            const prompt = `Analyze this video and provide a detailed JSON response with the following information:

1. **Outfit**: Describe what the person is wearing (clothing items, colors, style, accessories)
2. **Activity**: Describe what the person is doing or the action taking place
3. **Background**: Describe the setting, environment, and surroundings

Please format your response as valid JSON with this exact structure:
{
  "outfit": {
    "description": "detailed description of clothing and appearance",
    "items": ["list", "of", "clothing items"],
    "colors": ["list", "of", "dominant colors"]
  },
  "activity": {
    "description": "what the person is doing",
    "actions": ["list", "of", "specific actions"],
    "intensity": "low/medium/high"
  },
  "background": {
    "description": "description of the setting",
    "location_type": "indoor/outdoor/unknown",
    "environment": "description of surroundings",
    "lighting": "description of lighting conditions"
  },
  "summary": "brief overall summary of the video scene"
}

Be specific and detailed in your observations.`;

            // Send to Gemini for analysis
            console.log('🤖 Sending video to Gemini API...');
            const result = await this.model.generateContent([prompt, videoPart]);
            const response = await result.response;
            const text = response.text();

            console.log('✅ Received response from Gemini');

            // Try to parse JSON from the response
            let analysis;
            try {
                // Extract JSON from markdown code blocks if present
                const jsonMatch = text.match(/```(?:json)?\s*(\{[\s\S]*\})\s*```/);
                const jsonText = jsonMatch ? jsonMatch[1] : text;
                analysis = JSON.parse(jsonText);
            } catch (parseError) {
                console.warn('⚠️  Could not parse as JSON, returning raw text');
                // If JSON parsing fails, create a structured response from the text
                analysis = {
                    outfit: { description: "See raw response", items: [], colors: [] },
                    activity: { description: "See raw response", actions: [], intensity: "unknown" },
                    background: { description: "See raw response", location_type: "unknown", environment: "See raw response", lighting: "unknown" },
                    summary: text,
                    raw_response: text
                };
            }

            // Add metadata
            analysis.analyzed_at = new Date().toISOString();
            analysis.video_file = path.basename(videoPath);
            analysis.video_size_mb = fileSizeMB;

            return analysis;

        } catch (error) {
            console.error('❌ Error analyzing video:', error.message);
            throw error;
        }
    }

    /**
     * Analyze video and save results to JSON file
     */
    async analyzeAndSave(videoPath, outputPath = null) {
        const analysis = await this.analyzeVideo(videoPath);

        // Default output path: same name as video but .json
        if (!outputPath) {
            outputPath = videoPath.replace(/\.[^.]+$/, '-analysis.json');
        }

        // Save analysis to file
        fs.writeFileSync(outputPath, JSON.stringify(analysis, null, 2));
        console.log('💾 Analysis saved to:', outputPath);

        return { analysis, outputPath };
    }

    /**
     * Get a human-readable summary from analysis
     */
    static formatSummary(analysis) {
        if (analysis.raw_response) {
            return analysis.raw_response;
        }

        return `
📹 Video Analysis Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👔 OUTFIT:
   ${analysis.outfit.description}
   Items: ${analysis.outfit.items.join(', ')}
   Colors: ${analysis.outfit.colors.join(', ')}

🎬 ACTIVITY:
   ${analysis.activity.description}
   Actions: ${analysis.activity.actions.join(', ')}
   Intensity: ${analysis.activity.intensity}

🏞️ BACKGROUND:
   ${analysis.background.description}
   Location: ${analysis.background.location_type}
   Environment: ${analysis.background.environment}
   Lighting: ${analysis.background.lighting}

📝 SUMMARY:
   ${analysis.summary}
`;
    }
}

module.exports = VideoAnalyzer;

