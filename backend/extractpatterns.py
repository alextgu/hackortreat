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
    Summarize key attributes from posts for AI prompts.
    
    Extracts important fields and creates a short text snippet for each post.
    
    Args:
        posts (list[dict]): List of post dictionaries.

    Returns:
        list[dict]: List of summarized post dictionaries.
    """
    summaries = []
    for post in posts:
        text = post.get('generated_post_text', '')  # Post content
        hashtags = post.get('key_hashtags', [])     # List of hashtags
        summary = {
            'post_id': post.get('post_id'),
            'style_preset': post.get('style_preset'),
            'date_posted': post.get('date_posted'),
            'original_context': post.get('original_context'),
            # Take first 20 words as snippet for AI context
            'text_snippet': ' '.join(text.split()[:20]) + ('...' if len(text.split()) > 20 else ''),
            'hashtags': hashtags,
            # Count sentences by splitting on punctuation
            'num_sentences': len([s for s in re.split(r'[.!?]+', text) if s.strip()]),
            # Count paragraphs by double line breaks
            'num_paragraphs': text.count('\n\n') + 1,
            # Include engagement metrics if present
            'engagement': post.get('engagement_metrics', {})
        }
        summaries.append(summary)
    return summaries

def overall_patterns(posts):
    """
    Summarize general patterns across all posts.
    
    Calculates average length, sentences, and paragraphs across dataset.

    Args:
        posts (list[dict]): List of post dictionaries.

    Returns:
        dict: Average length, sentences, and paragraphs.
    """
    total_length = sum(len(post.get('generated_post_text', '')) for post in posts)
    total_sentences = sum(len([s for s in re.split(r'[.!?]+', post.get('generated_post_text', '')) if s.strip()]) for post in posts)
    total_paragraphs = sum(post.get('generated_post_text', '').count('\n\n') + 1 for post in posts)
    n = len(posts)
    return {
        'avg_length': total_length / n if n else 0,
        'avg_sentences': total_sentences / n if n else 0,
        'avg_paragraphs': total_paragraphs / n if n else 0
    }

if __name__ == "__main__":
    # Prompt user to input a JSON file path (relative to this script)
    filename = input("Enter the path to your JSON file (relative to this script): ").strip()
    
    #../data/raw/filename.json

    # Load the posts from the given file
    posts = load_posts(filename)
    
    # Extract summarized version of each post
    summaries = extract_summary(posts)
    
    # Calculate overall patterns across all posts
    patterns = overall_patterns(posts)
    
    # Compact summary to feed into Gemini or another AI
    ai_context = {
        'posts_summary': summaries,
        'overall_patterns': patterns
    }

    # Print the structured summary in JSON format
    print(json.dumps(ai_context, indent=2))
