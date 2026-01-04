# tech_content_agent.py
import google.generativeai as genai
import json
import os
from datetime import datetime
import time
import random

class TechContentGenerator:
    def __init__(self, gemini_api_key):
        """Initialize the content generator with Gemini API"""
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Content categories for variety
        self.categories = [
            "AI/ML insights",
            "Cloud infrastructure tips",
            "DSA problem breakdowns",
            "System design concepts",
            "Full-stack development",
            "Reinforcement learning",
            "Tech career advice",
            "Coding best practices",
            "DevOps/Infrastructure",
            "Tech industry trends"
        ]
        
        # Optimal posting times for US (EST) and India (IST)
        self.optimal_times = {
            'US_morning': '09:00',  # 9 AM EST = 7:30 PM IST
            'US_lunch': '12:00',    # 12 PM EST = 10:30 PM IST
            'India_morning': '09:00',  # 9 AM IST = 10:30 PM EST (previous day)
            'India_evening': '18:00'   # 6 PM IST = 7:30 AM EST
        }
    
    def generate_content_batch(self, num_posts=7):
        """Generate a week's worth of diverse tech content"""
        posts = []
        
        for i in range(num_posts):
            category = random.choice(self.categories)
            post_type = random.choice([
                'insight', 'tip', 'thread_starter', 
                'question', 'breakdown', 'comparison'
            ])
            
            prompt = self._build_prompt(category, post_type)
            
            try:
                response = self.model.generate_content(prompt)
                post_data = {
                    'content': response.text.strip(),
                    'category': category,
                    'type': post_type,
                    'generated_at': datetime.now().isoformat(),
                    'optimal_time': random.choice(list(self.optimal_times.keys())),
                    'hashtags': self._generate_hashtags(category)
                }
                posts.append(post_data)
                
                # Rate limiting to avoid API throttling
                time.sleep(2)
                
            except Exception as e:
                print(f"Error generating content: {e}")
                continue
        
        return posts
    
    def _build_prompt(self, category, post_type):
        """Build context-aware prompts for authentic content"""
        
        base_context = f"""You are a tech professional sharing valuable insights on X (Twitter).
        
Category: {category}
Post Type: {post_type}
Audience: Tech professionals, students, and enthusiasts in US & India

Requirements:
1. Create an engaging, authentic post (max 280 characters)
2. Use natural language, not marketing speak
3. Make it educational and valuable
4. Include 1-2 relevant hashtags naturally
5. Avoid generic advice - be specific
6. Sound like a real person sharing knowledge, not a bot

"""
        
        type_specific = {
            'insight': "Share a specific technical insight or learning experience.",
            'tip': "Provide a practical, actionable tip that solves a real problem.",
            'thread_starter': "Start a thought-provoking discussion with a question or statement.",
            'question': "Ask an engaging technical question that sparks discussion.",
            'breakdown': "Explain a complex concept simply (e.g., 'Recursion in 3 lines')",
            'comparison': "Compare two technologies/approaches with pros/cons"
        }
        
        return base_context + type_specific[post_type]
    
    def _generate_hashtags(self, category):
        """Generate relevant hashtags based on category"""
        hashtag_map = {
            "AI/ML insights": ["#MachineLearning", "#AI", "#DeepLearning"],
            "Cloud infrastructure tips": ["#CloudComputing", "#AWS", "#DevOps"],
            "DSA problem breakdowns": ["#DSA", "#Algorithms", "#CodingInterview"],
            "System design concepts": ["#SystemDesign", "#SoftwareArchitecture"],
            "Full-stack development": ["#FullStack", "#WebDev", "#JavaScript"],
            "Reinforcement learning": ["#ReinforcementLearning", "#ML", "#AI"],
            "Tech career advice": ["#TechCareers", "#SoftwareEngineering"],
            "Coding best practices": ["#CleanCode", "#Programming", "#SoftwareEngineering"],
            "DevOps/Infrastructure": ["#DevOps", "#Kubernetes", "#Docker"],
            "Tech industry trends": ["#TechTrends", "#Innovation", "#TechNews"]
        }
        return random.sample(hashtag_map.get(category, ["#Tech"]), 2)
    
    def get_trending_topics(self):
        """Use Gemini to identify current trending tech topics"""
        prompt = """List 5 currently trending topics in tech (AI, cloud, development, etc.) 
        that would interest software engineers and tech students.
        Format: Just the topic names, one per line, no numbering."""
        
        try:
            response = self.model.generate_content(prompt)
            topics = [t.strip() for t in response.text.strip().split('\n') if t.strip()]
            return topics[:5]
        except Exception as e:
            print(f"Error fetching trends: {e}")
            return []
    
    def generate_trending_post(self, topic):
        """Generate a post about a specific trending topic"""
        prompt = f"""Create an insightful X (Twitter) post about: {topic}

Requirements:
- Max 280 characters
- Valuable and educational
- Natural, authentic voice
- Include 1-2 relevant hashtags
- Appeal to both US and Indian tech audiences

Make it sound like a real tech professional sharing knowledge, not promotional."""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating trending post: {e}")
            return None
    
    def save_content_queue(self, posts, filename='content_queue.json'):
        """Save generated posts to a file for review"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved {len(posts)} posts to {filename}")
    
    def load_content_queue(self, filename='content_queue.json'):
        """Load previously generated posts"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []


class PostScheduler:
    """Smart scheduler for optimal posting times"""
    
    def __init__(self):
        self.schedule = []
    
    def create_weekly_schedule(self, posts):
        """Create a posting schedule optimized for US & India reach"""
        schedule = []
        
        # Distribute posts across optimal times
        time_slots = ['US_morning', 'India_evening', 'US_lunch', 'India_morning']
        
        for i, post in enumerate(posts):
            day = i // 2  # 2 posts per day
            time_slot = time_slots[i % len(time_slots)]
            
            schedule.append({
                'day': day + 1,
                'time_slot': time_slot,
                'post': post,
                'posted': False
            })
        
        return schedule
    
    def save_schedule(self, schedule, filename='post_schedule.json'):
        """Save schedule to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(schedule, f, indent=2, ensure_ascii=False)
        print(f"📅 Saved schedule with {len(schedule)} posts")


# Example usage
def main():
    print("🚀 Tech Content Generator")
    print("=" * 50)
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        api_key = input("Enter your Gemini API key: ").strip()
    
    generator = TechContentGenerator(api_key)
    scheduler = PostScheduler()
    
    print("\n1. Generating trending topics...")
    topics = generator.get_trending_topics()
    print(f"Found topics: {topics}")
    
    print("\n2. Generating content batch...")
    posts = generator.generate_content_batch(num_posts=14)  # 2 weeks
    
    print("\n3. Adding trending topic posts...")
    for topic in topics[:3]:
        trending_post = generator.generate_trending_post(topic)
        if trending_post:
            posts.append({
                'content': trending_post,
                'category': 'Trending',
                'type': 'trending',
                'topic': topic,
                'generated_at': datetime.now().isoformat()
            })
    
    print(f"\n4. Generated {len(posts)} total posts")
    generator.save_content_queue(posts)
    
    print("\n5. Creating posting schedule...")
    schedule = scheduler.create_weekly_schedule(posts)
    scheduler.save_schedule(schedule)
    
    print("\n✅ Content generation complete!")
    print("\nNext steps:")
    print("1. Review content_queue.json")
    print("2. Edit/approve posts you like")
    print("3. Use manual_poster.py to post approved content")


if __name__ == "__main__":
    main()