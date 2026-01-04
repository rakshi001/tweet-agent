# manual_poster.py
"""
Safe manual posting script with human-like behavior
Run this to post your pre-approved content
"""

import tweepy
import json
import time
import random
from datetime import datetime

class SafeTwitterPoster:
    def __init__(self, api_key, api_secret, access_token, access_secret):
        """Initialize Twitter API with OAuth 1.0a"""
        self.client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
        
    def post_with_human_behavior(self, text):
        """Post with delays to simulate human behavior"""
        try:
            # Random delay before posting (2-5 seconds)
            time.sleep(random.uniform(2, 5))
            
            response = self.client.create_tweet(text=text)
            print(f"✅ Posted successfully! Tweet ID: {response.data['id']}")
            
            # Random delay after posting (30-60 seconds)
            time.sleep(random.uniform(30, 60))
            
            return True
        except Exception as e:
            print(f"❌ Error posting: {e}")
            return False
    
    def post_from_queue(self, queue_file='content_queue.json', limit=None):
        """Post approved content from queue"""
        with open(queue_file, 'r') as f:
            posts = json.load(f)
        
        if limit:
            posts = posts[:limit]
        
        print(f"\n📤 Posting {len(posts)} tweets...")
        successful = 0
        
        for i, post in enumerate(posts, 1):
            print(f"\n[{i}/{len(posts)}] Posting:")
            print(f"Content: {post['content'][:100]}...")
            
            # Ask for confirmation (safety feature)
            confirm = input("Post this? (y/n/skip): ").lower()
            
            if confirm == 'y':
                if self.post_with_human_behavior(post['content']):
                    successful += 1
                    post['posted'] = True
                    post['posted_at'] = datetime.now().isoformat()
            elif confirm == 'skip':
                continue
            else:
                print("Skipped.")
        
        # Save updated queue
        with open(queue_file, 'w') as f:
            json.dump(posts, f, indent=2)
        
        print(f"\n✅ Posted {successful}/{len(posts)} tweets successfully")


def interactive_mode():
    """Interactive posting mode"""
    print("🐦 Twitter Manual Poster")
    print("=" * 50)
    
    # Load credentials (you'll add these)
    api_key = input("API Key: ").strip()
    api_secret = input("API Secret: ").strip()
    access_token = input("Access Token: ").strip()
    access_secret = input("Access Token Secret: ").strip()
    
    poster = SafeTwitterPoster(api_key, api_secret, access_token, access_secret)
    
    while True:
        print("\nOptions:")
        print("1. Post single tweet")
        print("2. Post from queue (with confirmation)")
        print("3. Exit")
        
        choice = input("\nChoose: ").strip()
        
        if choice == '1':
            text = input("Tweet text: ").strip()
            poster.post_with_human_behavior(text)
        elif choice == '2':
            limit = input("How many? (Enter for all): ").strip()
            limit = int(limit) if limit else None
            poster.post_from_queue(limit=limit)
        elif choice == '3':
            break


if __name__ == "__main__":
    interactive_mode()