import json
import random
import os
import re
from pathlib import Path

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ google-generativeai not installed. Using template generation.")

def load_patterns(style):
    """
    Load extracted patterns for a specific style.
    
    Args:
        style (str): Style name (performative, serious, cluely, boardy)
    
    Returns:
        dict: Patterns dictionary or None
    """
    # Map serious to professional
    if style == 'serious':
        style = 'professional'
    
    patterns_path = Path(__file__).parent.parent / 'data' / 'processed' / f'patterns_{style}.json'
    
    if patterns_path.exists():
        with open(patterns_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def load_example_posts(style):
    """
    Load 2-3 full example posts from the dataset to show complete writing style.
    """
    if style == 'serious':
        style = 'professional'
    
    dataset_path = Path(__file__).parent.parent / 'data' / 'raw' / f'{style}.json'
    
    if not dataset_path.exists():
        return []
    
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            posts = json.load(f)
        
        examples = []
        for post in posts[:2]:  # Get first 2 posts as examples
            text = post.get('generated_post_text') or post.get('full_post_text', '')
            if text:
                # Truncate if too long
                if len(text) > 800:
                    text = text[:800] + "..."
                examples.append(text)
        
        return examples
    except:
        return []

def build_gemini_prompt(context, style, patterns):
    """
    Build a detailed prompt for Gemini based on extracted patterns.
    
    Args:
        context (str): User's topic/context
        style (str): Writing style
        patterns (dict): Extracted patterns from dataset
    
    Returns:
        str: Formatted prompt for Gemini
    """
    if not patterns:
        return f"Write a detailed, flowing LinkedIn post about: {context}. Use natural paragraphs and full sentences."
    
    # Extract pattern details
    openings = patterns.get('opening_patterns', [])
    starters = patterns.get('top_sentence_starters', [])
    phrases = patterns.get('common_phrases', [])
    structure = patterns.get('structure', {})
    tone = patterns.get('tone_indicators', {})
    formatting = patterns.get('formatting_patterns', {})
    
    # Build style description
    style_desc = {
        'performative': 'humble brags, virtue signaling, and inspirational but self-promotional',
        'serious': 'professional, corporate jargon-heavy, and formal business tone',
        'cluely': 'out of touch with reality, tone-deaf, and unaware',
        'boardy': 'meeting culture, collaboration-focused, and community-driven',
        'professional': 'corporate jargon overload, formal business language'
    }.get(style, 'professional and engaging')
    
    # Load full example posts
    example_posts = load_example_posts(style)
    
    prompt = f"""You are a LinkedIn content writer. Your task is to write an authentic, engaging LinkedIn post.

CONTEXT/TOPIC: {context}

WRITING STYLE TO MATCH: "{style}" ({style_desc})

"""
    
    # Add full example posts if available
    if example_posts:
        prompt += f"Here are REAL examples of posts in this exact style. Study the voice, tone, and structure:\n\n"
        for i, example in enumerate(example_posts, 1):
            prompt += f"EXAMPLE {i}:\n{example}\n\n"
    
    # Add structure guidance
    prompt += f"\nYour post should be approximately {int(structure.get('avg_length', 500))} characters with {int(structure.get('avg_sentences', 10))}-{int(structure.get('avg_sentences', 10))+5} sentences across {int(structure.get('avg_paragraphs', 3))}-{int(structure.get('avg_paragraphs', 5))+2} paragraphs.\n\n"
    
    # Add opening inspiration
    if openings and len(openings) > 0:
        prompt += f"Consider starting with a hook similar to these styles:\n"
        for opening in openings[:2]:
            opening_text = opening[:100] + "..." if len(opening) > 100 else opening
            prompt += f'- "{opening_text}"\n'
        prompt += "\n"
    
    # Add common phrases naturally
    if phrases and len(phrases) > 5:
        phrase_list = [p[0] for p in phrases[:8]]
        prompt += f"Naturally incorporate phrases like: {', '.join(phrase_list[:5])}\n\n"
    
    # Add tone guidance
    tone_notes = []
    if tone.get('direct_address', 0) > 10:
        tone_notes.append("Address the reader directly using 'you' and 'your'")
    if tone.get('first_person', 0) > 10:
        tone_notes.append("Write in first person (I, my, we) to make it personal")
    if tone.get('questions', 0) > 5:
        tone_notes.append("Include thought-provoking questions")
    if tone.get('exclamations', 0) > 5:
        tone_notes.append("Use exclamation marks for emphasis and energy")
    
    if tone_notes:
        prompt += "Tone guidelines:\n"
        for note in tone_notes:
            prompt += f"- {note}\n"
        prompt += "\n"
    
    prompt += f"""IMPORTANT INSTRUCTIONS:
- Write ONLY the LinkedIn post content itself (no titles, no labels, no "Here's the post:")
- Use full, flowing paragraphs with natural transitions
- Expand on "{context}" with specific details, examples, or personal insights
- Write like a real person sharing authentic thoughts, not a template or outline
- NO bullet points or numbered lists in the post body
- NO hashtags (they'll be added separately)
- Make it feel genuine and emotionally resonant

Now write the LinkedIn post:"""
    
    return prompt

def clean_gemini_output(text):
    """
    Clean up Gemini output to remove any meta-text or formatting artifacts.
    
    Args:
        text (str): Raw Gemini output
    
    Returns:
        str: Cleaned post text
    """
    if not text:
        return text
    
    # Remove common meta-text patterns
    meta_patterns = [
        r'^Here\'?s? (?:the|a) (?:LinkedIn )?post:?\s*\n*',
        r'^Here (?:is|are) (?:the|a) (?:LinkedIn )?post:?\s*\n*',
        r'^LinkedIn [Pp]ost:?\s*\n*',
        r'^\*\*LinkedIn Post:?\*\*\s*\n*',
        r'^Post:?\s*\n*',
        r'^\*\*Post:?\*\*\s*\n*',
    ]
    
    for pattern in meta_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
    
    # Remove leading/trailing quotes if entire post is quoted
    text = text.strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1].strip()
    if text.startswith("'") and text.endswith("'"):
        text = text[1:-1].strip()
    
    # Remove markdown bold/italic artifacts if they appear at boundaries
    text = text.strip('*').strip('_')
    
    return text.strip()

def extract_boardy_ctas():
    """
    Extract the last lines from boardy posts that mention Boardy.
    
    Returns:
        list: List of Boardy CTA lines
    """
    boardy_ctas = [
        "if you want help surrounding yourself with people who lift you up, not drain you - you can find them on Boardy.\n\nbecause when you spend enough time around winners,\nit stops feeling impossible to win too.",
        
        "That's exactly what I'm doing now with Boardy — a place where you can connect with the most inspiring people around the world, have real conversations, and start building your own community. DM Boardy on Linkedin to get started!\nYou never know what one conversation might spark.🔥",
        
        "If you want to make the most out of your time, and meet like-minded people, use Boardy, stop waiting for the perfect moment, and network NOW.",
        
        "Boardy is doing the same thing. You message it what you need, and it connects you to the right person. simplistic peak.",
        
        "Boardy was one of those platforms where I met individuals with the same drive, the same vision, and the same desire to grow\n\nit wasn't just about networking\n\nit was about building the kind of connections that accelerate your journey, that bring you closer to your dream\n\nno dream is ever too big, you got this"
    ]
    return boardy_ctas

def add_boardy_cta(text, style):
    """
    Add Boardy call-to-action for boardy-style posts using actual CTAs from the dataset.
    
    Args:
        text (str): Post text
        style (str): Post style
    
    Returns:
        str: Post with CTA if boardy style
    """
    if style.lower() != 'boardy':
        return text
    
    # Check if boardy is already mentioned
    if 'boardy' in text.lower():
        return text
    
    # Get random CTA from actual boardy posts
    boardy_ctas = extract_boardy_ctas()
    selected_cta = random.choice(boardy_ctas)
    
    return text + "\n\n" + selected_cta

def polish_with_gemini(text, style='professional'):
    """
    Use Gemini to fix all English mistakes while keeping the same idea.
    
    Args:
        text (str): Draft post text
        style (str): Post style (for boardy CTA)
    
    Returns:
        str: Polished post text
    """
    if not GEMINI_AVAILABLE:
        return add_boardy_cta(text, style)
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return add_boardy_cta(text, style)
    
    polish_prompt = f"""You are a grammar checker. Fix ONLY grammar, spelling, and punctuation errors in this text.

DO NOT:
- Add new content
- Remove content
- Change the meaning
- Add explanations
- Add labels like "Here's the corrected version:"

DO:
- Fix spelling mistakes
- Fix grammar errors
- Fix punctuation
- Keep the exact same tone and style

Text to fix:
{text}

Output the corrected text only:"""
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(polish_prompt)
        polished = clean_gemini_output(response.text)
        
        # Validate the output isn't crazy different
        if polished and len(polished) > 50:  # Basic sanity check
            print(f"   ✨ Grammar checked and corrected")
            final_text = polished
        else:
            print(f"   ⚠️ Grammar check gave weird result, using original")
            final_text = text
        
        # Add Boardy CTA if boardy style
        final_text = add_boardy_cta(final_text, style)
        
        return final_text
            
    except Exception as e:
        print(f"   ⚠️ Grammar check failed: {e}, using original")
        return add_boardy_cta(text, style)

def generate_with_gemini(prompt, style='professional'):
    """
    Generate post using Gemini AI.
    
    Args:
        prompt (str): The prompt for generation
        style (str): Post style (for boardy CTA)
    
    Returns:
        str: Generated post text
    """
    if not GEMINI_AVAILABLE:
        return None
    
    # Get API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("⚠️ GEMINI_API_KEY not found in environment")
        return None
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        # Clean the output
        cleaned_text = clean_gemini_output(response.text)
        
        # Polish for grammar and flow (includes boardy CTA if needed)
        if cleaned_text:
            polished_text = polish_with_gemini(cleaned_text, style)
            return polished_text
        
        return cleaned_text
    except Exception as e:
        print(f"❌ Gemini generation error: {e}")
        return None

def generate_linkedin_post(context, style='professional', patterns=None):
    """
    Generate a LinkedIn post using extracted patterns and Gemini AI.

    Args:
        context (str): Topic or context for the post
        style (str): Writing style (performative, serious, cluely, boardy)
        patterns (dict): Optional pre-loaded patterns

    Returns:
        dict: Generated LinkedIn post dictionary
    """
    # Load patterns if not provided
    if patterns is None:
        patterns = load_patterns(style)
    
    # Build prompt using patterns
    prompt = build_gemini_prompt(context, style, patterns)
    
    print(f"\n🎨 [GENERATION] Generating {style} post about: {context[:50]}...")
    
    # Try to generate with Gemini
    generated_text = generate_with_gemini(prompt, style)
    
    # Fallback to template if Gemini fails
    if not generated_text:
        print("   ⚠️ Using template generation (Gemini unavailable)")
        generated_text = generate_template_post(context, style, patterns)
        # Add boardy CTA for template posts too
        generated_text = add_boardy_cta(generated_text, style)
    else:
        print("   ✅ Generated with Gemini AI")
    
    return {
        "platform": "LinkedIn",
        "style": style,
        "full_text": generated_text.strip(),
        "context": context,
        "used_patterns": bool(patterns),
        "generator": "gemini" if generated_text and GEMINI_AVAILABLE else "template"
    }

def generate_template_post(context, style, patterns):
    """
    Generate a template-based post when Gemini is unavailable.
    
    Args:
        context (str): Topic/context
        style (str): Writing style
        patterns (dict): Extracted patterns
    
    Returns:
        str: Generated post text
    """
    if not patterns:
        return f"I've been reflecting on {context} lately, and it's shifted my perspective in unexpected ways.\n\nIt's easy to overlook the impact this has on how we approach our daily work, but the more I dive into it, the more I realize how fundamental it is.\n\nThe real breakthrough comes when you stop treating it as just another task and start seeing it as an opportunity to grow.\n\nWhat's your experience with this? I'd love to hear your thoughts."
    
    # Use patterns to create a styled post
    openings = patterns.get('opening_patterns', [])
    phrases = patterns.get('common_phrases', [])
    structure = patterns.get('structure', {})
    tone = patterns.get('tone_indicators', {})
    
    # Select an appropriate opening
    opening = random.choice(openings) if openings else f"Let's talk about {context}"
    
    # Keep opening concise but natural
    if len(opening) > 150:
        # Take first sentence or two
        sentences = opening.split('.')[:2]
        opening = '. '.join(sentences) + '.'
    
    # Build body paragraphs
    paragraphs = []
    
    # Paragraph 1: Expand on context
    para1 = f"{context} has been on my mind recently."
    if tone.get('first_person', 0) > 10:
        para1 += f" I've realized that the way we approach this can make all the difference in our outcomes."
    else:
        para1 += f" It's something that affects more of us than we might think."
    paragraphs.append(para1)
    
    # Paragraph 2: Add depth with common phrases
    if phrases and len(phrases) > 5:
        common_phrase = random.choice(phrases[:5])[0]
        para2 = f"Here's what I've learned: {common_phrase} isn't just a nice idea - it's essential. "
        
        if tone.get('questions', 0) > 5:
            para2 += f"What happens when we ignore this? We miss opportunities that could transform everything."
        else:
            para2 += f"When we truly understand this, our entire perspective shifts."
        paragraphs.append(para2)
    
    # Paragraph 3: Personal reflection or call to action
    if tone.get('direct_address', 0) > 20:
        para3 = f"If you're working on {context}, you know how challenging it can be. "
        para3 += "But that challenge is exactly what makes the breakthrough so rewarding."
    else:
        para3 = f"The journey with {context} continues to surprise and teach. "
        para3 += "Every step forward reveals new insights worth sharing."
    paragraphs.append(para3)
    
    # Closing with engagement
    if tone.get('questions', 0) > 10:
        closing = f"What's your experience with this? How has {context} impacted your work?"
    else:
        closing = "Looking forward to hearing different perspectives on this."
    
    # Combine all parts
    full_post = f"{opening}\n\n" + "\n\n".join(paragraphs) + f"\n\n{closing}"
    
    return full_post

if __name__ == "__main__":
    # Load the context JSON generated by your parser
    context_file = input("Enter path to Gemini summary JSON file: ").strip()
    context = load_context(context_file)

    # Generate LinkedIn posts from all summaries
    generated_posts = []
    for summary in context.get('posts_summary', []):
        post = generate_linkedin_post(summary)
        generated_posts.append(post)

    # Output the generated LinkedIn posts JSON
    print(json.dumps(generated_posts, indent=2))
