import json
from collections import Counter
import re

def load_posts(filepath):
    """Load posts from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_writing_style(posts):
    """Analyze writing style patterns for generation"""
    patterns = {
        'opening_patterns': [],
        'sentence_starters': [],
        'common_phrases': [],
        'formatting_patterns': [],
        'tone_indicators': [],
        'call_to_actions': []
    }
    
    for post in posts:
        text = post.get('generated_post_text') or post.get('text', '')
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Capture actual opening lines (first 1-3 lines)
        if len(lines) > 0:
            patterns['opening_patterns'].append(lines[0])
        
        # Extract sentence starters (first 3-5 words of sentences)
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        for sentence in sentences:
            words = sentence.split()
            if len(words) >= 3:
                starter = ' '.join(words[:4])
                patterns['sentence_starters'].append(starter)
        
        # Detect common phrases (3-5 word sequences)
        words = text.lower().split()
        for i in range(len(words) - 2):
            phrase = ' '.join(words[i:i+3])
            if len(phrase) > 10:  # Avoid very short phrases
                patterns['common_phrases'].append(phrase)
        
        # Formatting patterns
        if '\n\n' in text:
            patterns['formatting_patterns'].append('uses_paragraph_breaks')
        if re.search(r'^\s*[-•➢]', text, re.MULTILINE):
            patterns['formatting_patterns'].append('uses_bullet_points')
        if re.search(r'[𝗕-𝗭𝗯-𝘇]', text):  # Bold unicode
            patterns['formatting_patterns'].append('uses_bold_text')
        if re.search(r'[𝘈-𝘡𝘢-𝘻]', text):  # Italic unicode
            patterns['formatting_patterns'].append('uses_italic_text')
        
        # Tone indicators
        if '?' in text and text.count('?') >= 2:
            patterns['tone_indicators'].append('questioning_tone')
        if '!' in text and text.count('!') >= 2:
            patterns['tone_indicators'].append('excited_tone')
        if any(word in text.lower() for word in ['you', 'your', "you're"]):
            patterns['tone_indicators'].append('direct_address')
        if re.search(r'\bi\s|^i\s|\si$', text.lower()):
            patterns['tone_indicators'].append('personal_narrative')
        
        # Call to actions (ending patterns)
        if len(lines) > 0:
            last_line = lines[-1].lower()
            if any(word in last_line for word in ['dm', 'comment', 'message', 'reach out', 'connect']):
                patterns['call_to_actions'].append(lines[-1])
    
    # Count and return most common patterns
    return {
        'opening_patterns': patterns['opening_patterns'],  # Keep all for variety
        'top_sentence_starters': [phrase for phrase, _ in Counter(patterns['sentence_starters']).most_common(15)],
        'common_phrases': [phrase for phrase, _ in Counter(patterns['common_phrases']).most_common(20)],
        'formatting_patterns': list(Counter(patterns['formatting_patterns']).keys()),
        'tone_indicators': list(Counter(patterns['tone_indicators']).keys()),
        'call_to_actions': patterns['call_to_actions']  # Keep all for variety
    }

def analyze_structure(posts):
    """Analyze post structure for consistency"""
    stats = {
        'avg_length': 0,
        'avg_sentences': 0,
        'avg_paragraphs': 0,
        'avg_line_breaks': 0,
        'length_range': {'min': float('inf'), 'max': 0}
    }
    
    for post in posts:
        text = post.get('generated_post_text') or post.get('text', '')
        length = len(text)
        stats['avg_length'] += length
        stats['length_range']['min'] = min(stats['length_range']['min'], length)
        stats['length_range']['max'] = max(stats['length_range']['max'], length)
        
        sentences = re.split(r'[.!?]+', text)
        stats['avg_sentences'] += len([s for s in sentences if s.strip()])
        stats['avg_paragraphs'] += text.count('\n\n') + 1
        stats['avg_line_breaks'] += text.count('\n')
    
    n = len(posts)
    stats['avg_length'] = stats['avg_length'] / n
    stats['avg_sentences'] = stats['avg_sentences'] / n
    stats['avg_paragraphs'] = stats['avg_paragraphs'] / n
    stats['avg_line_breaks'] = stats['avg_line_breaks'] / n
    
    return stats

def extract_vocabulary(posts):
    """Extract key vocabulary and word choices"""
    all_words = []
    for post in posts:
        text = post.get('generated_post_text') or post.get('text', '')
        # Extract meaningful words (filter out common stop words)
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        all_words.extend(words)
    
    # Get most common meaningful words
    word_freq = Counter(all_words)
    common_stopwords = {'that', 'this', 'with', 'from', 'have', 'been', 'were', 'their', 'what', 'when', 'your'}
    filtered_words = [(w, c) for w, c in word_freq.most_common(30) if w not in common_stopwords]
    
    return [word for word, _ in filtered_words[:20]]

def count_emojis(posts):
    """Count emoji usage"""
    emoji_list = []
    for post in posts:
        text = post.get('generated_post_text') or post.get('text', '')
        emojis = [c for c in text if ord(c) > 0x1F300]
        emoji_list.extend(emojis)
    
    emoji_freq = Counter(emoji_list)
    return {
        'total': len(emoji_list),
        'unique': len(emoji_freq),
        'most_common': [{'emoji': e, 'count': c} for e, c in emoji_freq.most_common(10)]
    }

if __name__ == "__main__":
    import sys
    import os
    
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'data/raw/boardy.json'
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'data/processed/patterns.json'
    
    print(f"Loading posts from: {filepath}")
    posts = load_posts(filepath)
    print(f"Loaded {len(posts)} posts\n")
    
    print("=" * 60)
    print("ANALYZING WRITING STYLE PATTERNS")
    print("=" * 60)
    
    # Analyze writing style
    print("\n✍️  Extracting writing style patterns...")
    style_patterns = analyze_writing_style(posts)
    
    print(f"\n📝 Opening Patterns ({len(style_patterns['opening_patterns'])} examples):")
    for i, opening in enumerate(style_patterns['opening_patterns'][:5], 1):
        print(f"  {i}. {opening[:80]}{'...' if len(opening) > 80 else ''}")
    
    print(f"\n🎯 Common Sentence Starters ({len(style_patterns['top_sentence_starters'])} patterns):")
    for i, starter in enumerate(style_patterns['top_sentence_starters'][:8], 1):
        print(f"  {i}. '{starter}...'")
    
    print(f"\n💬 Common Phrases ({len(style_patterns['common_phrases'])} patterns):")
    for i, phrase in enumerate(style_patterns['common_phrases'][:8], 1):
        print(f"  {i}. '{phrase}'")
    
    print(f"\n🎨 Formatting Patterns:")
    for pattern in style_patterns['formatting_patterns']:
        print(f"  • {pattern.replace('_', ' ').title()}")
    
    print(f"\n🎭 Tone Indicators:")
    for tone in style_patterns['tone_indicators']:
        print(f"  • {tone.replace('_', ' ').title()}")
    
    if style_patterns['call_to_actions']:
        print(f"\n📢 Call-to-Action Examples:")
        for i, cta in enumerate(style_patterns['call_to_actions'][:3], 1):
            print(f"  {i}. {cta}")
    
    # Analyze structure
    print("\n📊 Post Structure:")
    structure = analyze_structure(posts)
    print(f"  Average length: {structure['avg_length']:.0f} chars (range: {structure['length_range']['min']}-{structure['length_range']['max']})")
    print(f"  Average sentences: {structure['avg_sentences']:.1f}")
    print(f"  Average paragraphs: {structure['avg_paragraphs']:.1f}")
    print(f"  Average line breaks: {structure['avg_line_breaks']:.1f}")
    
    # Vocabulary
    print("\n📚 Key Vocabulary:")
    vocab = extract_vocabulary(posts)
    print(f"  {', '.join(vocab[:15])}")
    
    # Emojis
    print("\n😊 Emoji Usage:")
    emoji_data = count_emojis(posts)
    print(f"  Total: {emoji_data['total']}, Unique: {emoji_data['unique']}")
    if emoji_data['most_common']:
        print(f"  Most common: {' '.join([e['emoji'] for e in emoji_data['most_common'][:5]])}")
    
    # Save comprehensive patterns
    print(f"\n💾 Saving patterns to: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    patterns = {
        'source_file': filepath,
        'total_posts': len(posts),
        'writing_style': style_patterns,
        'structure': structure,
        'vocabulary': vocab,
        'emoji_usage': emoji_data
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(patterns, f, indent=2, ensure_ascii=False)
    
    print("✅ Done! Patterns extracted for content generation.")
    print("=" * 60)
