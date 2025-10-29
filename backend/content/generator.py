import json
import random
import os
from pathlib import Path

# Get the base directory for data files
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"

def load_posts_by_style(style):
    """Load example posts for a specific style"""
    style_map = {
        'performative': 'professional.json',
        'serious': 'professional.json', 
        'cluely': 'cluely.json',
        'boardy': 'boardy.json'
    }
    
    filename = style_map.get(style.lower(), 'professional.json')
    filepath = DATA_DIR / "raw" / filename
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'posts' in data:
                return data['posts']
            else:
                return []
    except FileNotFoundError:
        print(f"Warning: Posts file not found at {filepath}")
        return []

def generate_cluely_post(topic, details):
    """Generate a Cluely-style controversial post"""
    hooks = [
        f"{topic} isn't the problem — your mindset is.",
        f"Hot take: {topic} is actually the future.",
        f"Everyone's pretending they don't use {topic}. I just said the quiet part out loud.",
        f"You think {topic} is wrong until it works.",
        f"Unpopular opinion: {topic} is efficient, not unethical."
    ]
    
    templates = [
        f"{random.choice(hooks)}\n\nIf you think {details}, then you're missing the point.\n\nThe world is changing faster than your comfort zone. Adapt or get left behind.\n\n💭 Debate me below.",
        f"{random.choice(hooks)}\n\nLet's be real: everyone's already doing this. I'm just being honest about it.\n\n{details}\n\nStop pretending authenticity matters more than results.\n\nThoughts? 👇",
        f"{random.choice(hooks)}\n\nYour company's values are built on fear, not innovation.\n\n{details}\n\nThe future doesn't wait for permission.\n\n#Disruption #Innovation #AI"
    ]
    
    return random.choice(templates)

def generate_boardy_post(topic, details):
    """Generate a Boardy-style relatable/personal post"""
    openings = [
        "💭 A year ago, I felt stuck.",
        "If you're tired of feeling like everyone's life is moving faster than yours - read this:",
        "I've almost given up on my dream more times than I can count.",
        "My best friends are crushing it. And for a while, that hurt."
    ]
    
    template = f"""{random.choice(openings)}

{details}

It felt like everyone around me had it figured out. New jobs. Promotions. {topic}.

And you scroll through LinkedIn thinking:
"What am I even doing?"
"How are they so far ahead?"

But that mindset is the trap.

Once I stopped comparing and started connecting with people on the same journey, everything changed.

You realize success isn't a race. It's a community.

The more you're around people chasing real goals (not just posting about them), the more you start believing it's possible for you too.

So here's the truth:
If you want help building {topic}, you need people who get it.

Because when you spend time with the right people, you don't fall behind — you level up together.

Want to join a community like that? 👇"""
    
    return template

def generate_performative_post(topic, details):
    """Generate a classic performative LinkedIn post"""
    openings = [
        "I'm incredibly humbled to announce...",
        "I'm honored to share...",
        "After years of hard work...",
        "Today marks a significant milestone...",
        "I never thought I'd be saying this, but..."
    ]
    
    templates = [
        f"""{random.choice(openings)}

{details}

This journey wouldn't have been possible without the amazing team who believed in {topic} from day one.

Key learnings:
✅ Always stay curious
✅ Embrace failure as growth
✅ Network with purpose
✅ Give back to the community

Here's to the next chapter! 🚀

What's your biggest career lesson this year? Drop it below! 👇

#Leadership #Growth #Success #Grateful""",
        
        f"""Lesson learned about {topic}:

{details}

5 years ago, I would have never imagined this.

But here's what I've learned:
→ Success is a team sport
→ Authenticity builds trust
→ Impact over ego
→ Always be learning

Grateful for this journey and excited for what's next! 💡

What resonates with you? Let me know in the comments!

#ThoughtLeadership #Innovation #CareerGrowth"""
    ]
    
    return random.choice(templates)

def generate_serious_post(topic, details):
    """Generate a serious/corporate jargon heavy post"""
    templates = [
        f"""Leveraging synergies in {topic}: A paradigm shift

{details}

In today's rapidly evolving landscape, organizations must pivot to embrace transformational strategies that drive stakeholder value.

Key takeaways:
🔹 Optimize vertical integration
🔹 Maximize operational excellence
🔹 Foster cross-functional collaboration
🔹 Deploy agile methodologies

Moving forward, we must think outside the box to achieve mission-critical objectives.

Let's circle back offline to drill down on these action items.

#DigitalTransformation #EnterpriseStrategy #Innovation #Leadership""",
        
        f"""Disrupting {topic} through strategic innovation

{details}

As we navigate the new normal, it's imperative to:
• Cultivate a culture of continuous improvement
• Harness the power of data-driven insights
• Scale sustainable growth initiatives
• Drive best-in-class customer experiences

At the end of the day, it's about creating value propositions that resonate with our core competencies.

Let's ideate and workshop solutions that move the needle.

#BusinessStrategy #Synergy #ThoughtLeadership"""
    ]
    
    return random.choice(templates)

def generate_post(topic, details, style='professional'):
    """Generate a LinkedIn post based on topic, details, and style"""
    style = style.lower()
    
    generators = {
        'performative': generate_performative_post,
        'serious': generate_serious_post,
        'cluely': generate_cluely_post,
        'boardy': generate_boardy_post,
        'professional': generate_performative_post
    }
    
    generator_func = generators.get(style, generate_performative_post)
    
    try:
        return generator_func(topic, details)
    except Exception as e:
        print(f"Error generating post: {e}")
        return f"Thoughts on {topic}:\n\n{details}\n\nWhat do you think? Let me know in the comments! 👇\n\n#LinkedIn #Thoughts"

