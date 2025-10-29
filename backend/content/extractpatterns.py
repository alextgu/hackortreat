import json
import spacy
import emoji
from collections import Counter
import re
  
nlp = spacy.load("en_core_web_sm")
  
def load_posts(filepath):
    """Load posts from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
  
def extract_openings(posts, n_words=7):
    """Extract first N words of each post"""
    openings = []
    for post in posts:
        words = post['text'].split()[:n_words]
        openings.append(' '.join(words))
    return Counter(openings).most_common(10)
  
def count_emojis(posts):
    """Count emoji usage"""
    emoji_count = 0
    emoji_list = []
    for post in posts:
        emojis = [c for c in post['text'] if c in emoji.EMOJI_DATA]
        emoji_count += len(emojis)
        emoji_list.extend(emojis)
    return emoji_count, Counter(emoji_list).most_common(10)
  
def analyze_structure(posts):
    """Analyze post structure"""
    stats = {
        'avg_length': 0,
        'avg_sentences': 0,
        'avg_paragraphs': 0,
        'avg_line_breaks': 0
    }
      
    for post in posts:
        text = post['text']
        doc = nlp(text)
        stats['avg_length'] += len(text)
        stats['avg_sentences'] += len(list(doc.sents))
        stats['avg_paragraphs'] += text.count('\n\n') + 1
        stats['avg_line_breaks'] += text.count('\n')
      
    n = len(posts)
    return {k: v/n for k, v in stats.items()}
  
def extract_hashtags(posts):
    """Extract hashtags"""
    all_hashtags = []
    for post in posts:
        hashtags = re.findall(r'#\w+', post['text'])
        all_hashtags.extend(hashtags)
    return Counter(all_hashtags).most_common(10)
  
if __name__ == "__main__":
    # Will implement in Hour 2
    pass