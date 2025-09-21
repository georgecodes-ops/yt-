import requests
import time
from datetime import datetime, timedelta
import logging
from typing import List, Dict
import json

class RedditScraper:
    """Scrapes Reddit for finance-related discussions and unique insights"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Finance-related subreddits
        self.subreddits = [
            'personalfinance',
            'investing',
            'financialindependence',
            'SecurityAnalysis',
            'finance',
            'economy',
            'stocks',
            'cryptocurrency'
        ]
        self.base_url = "https://www.reddit.com/r/{}/top.json"
        self.headers = {
            'User-Agent': 'MonAY-Finance-Content-Bot/1.0'
        }
        
    def collect_trending_discussions(self, hours_back: int = 24, limit: int = 50) -> List[Dict]:
        """Collect trending discussions from finance subreddits"""
        all_posts = []
        
        for subreddit in self.subreddits:
            try:
                posts = self._scrape_subreddit(subreddit, hours_back, limit//len(self.subreddits))
                all_posts.extend(posts)
                self.logger.info(f"Collected {len(posts)} posts from r/{subreddit}")
                # Be respectful to Reddit servers
                time.sleep(2)
            except Exception as e:
                self.logger.error(f"Error scraping r/{subreddit}: {e}")
                
        # Sort by score and remove duplicates
        all_posts.sort(key=lambda x: x['score'], reverse=True)
        unique_posts = self._remove_duplicates(all_posts)
        
        return unique_posts[:limit]
    
    def _scrape_subreddit(self, subreddit: str, hours_back: int, limit: int) -> List[Dict]:
        """Scrape a single subreddit"""
        posts = []
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        try:
            url = self.base_url.format(subreddit)
            params = {
                'limit': limit,
                'sort': 'top',
                't': 'day'  # Top posts from the day
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            for post in data.get('data', {}).get('children', []):
                post_data = post.get('data', {})
                created_time = datetime.fromtimestamp(post_data.get('created_utc', 0))
                
                # Skip old posts
                if created_time < cutoff_time:
                    continue
                
                # Skip stickied posts and mods
                if post_data.get('stickied') or post_data.get('distinguished') == 'moderator':
                    continue
                
                post_info = {
                    'title': post_data.get('title', ''),
                    'content': post_data.get('selftext', ''),
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'score': post_data.get('score', 0),
                    'comments': post_data.get('num_comments', 0),
                    'author': post_data.get('author', ''),
                    'subreddit': subreddit,
                    'created': created_time.isoformat(),
                    'upvote_ratio': post_data.get('upvote_ratio', 0.5),
                    'keywords': self._extract_keywords(post_data.get('title', '') + ' ' + post_data.get('selftext', ''))
                }
                
                # Only include posts with substantial content
                if len(post_info['content']) > 50 or post_info['comments'] > 5:
                    posts.append(post_info)
                    
        except Exception as e:
            self.logger.error(f"Error scraping {subreddit}: {e}")
            
        return posts
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from Reddit post"""
        # Simple keyword extraction
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'hers', 'ours', 'theirs', 'reddit', 'r/', '[removed]', '[deleted]'}
        
        # Clean and extract words
        words = text.lower().replace(',', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ').replace('[', ' ').replace(']', ' ').split()
        keywords = [word for word in words if len(word) > 3 and word not in common_words and not word.startswith('http')]
        return list(set(keywords))[:15]  # Return unique keywords, limit to 15
    
    def _remove_duplicates(self, posts: List[Dict]) -> List[Dict]:
        """Remove duplicate posts based on title similarity"""
        unique_posts = []
        seen_titles = set()
        
        for post in posts:
            # Create a simplified title for comparison
            title_key = ' '.join(post['title'].lower().split()[:10])  # First 10 words
            if title_key not in seen_titles:
                unique_posts.append(post)
                seen_titles.add(title_key)
                
        return unique_posts
    
    def find_user_pain_points(self, hours_back: int = 24) -> List[Dict]:
        """Find common user questions and pain points"""
        posts = self.collect_trending_discussions(hours_back, 100)
        
        # Keywords that indicate questions or problems
        problem_indicators = ['why', 'how', 'help', 'problem', 'issue', 'confused', 'stuck', 'struggling', 'difficult', 'hard', 'trouble', 'need', 'want', 'looking', 'trying', 'can\'t', 'cannot', 'should i', 'what should', 'mistake', 'wrong', 'broken']
        
        pain_points = []
        for post in posts:
            title_lower = post['title'].lower()
            content_lower = post['content'].lower()
            
            # Check if post indicates a problem or question
            has_problem = any(indicator in title_lower or indicator in content_lower for indicator in problem_indicators)
            
            if has_problem and post['score'] > 10:  # Only high-score posts
                pain_points.append({
                    'title': post['title'],
                    'content': post['content'][:200] + '...' if len(post['content']) > 200 else post['content'],
                    'subreddit': post['subreddit'],
                    'url': post['url'],
                    'score': post['score'],
                    'keywords': post['keywords']
                })
        
        return pain_points[:30]  # Return top 30 pain points
    
    def find_contrarian_ideas(self, hours_back: int = 24) -> List[Dict]:
        """Find contrarian or unconventional financial ideas"""
        posts = self.collect_trending_discussions(hours_back, 100)
        
        # Keywords that might indicate contrarian ideas
        contrarian_indicators = ['wrong', 'myth', 'lie', 'secret', 'unpopular', 'counterintuitive', 'against', 'opposite', 'reverse', 'different', 'unique', 'weird', 'strange', 'unusual', 'rare', 'odd', 'peculiar']
        
        contrarian_ideas = []
        for post in posts:
            title_lower = post['title'].lower()
            content_lower = post['content'].lower()
            
            # Check for contrarian indicators
            has_contrarian = any(indicator in title_lower or indicator in content_lower for indicator in contrarian_indicators)
            
            if has_contrarian and post['score'] > 15:  # Only notable posts
                contrarian_ideas.append({
                    'title': post['title'],
                    'content': post['content'][:200] + '...' if len(post['content']) > 200 else post['content'],
                    'subreddit': post['subreddit'],
                    'url': post['url'],
                    'score': post['score'],
                    'keywords': post['keywords'],
                    'type': 'contrarian'
                })
        
        return contrarian_ideas[:20]  # Return top 20 contrarian ideas

if __name__ == "__main__":
    # Test the Reddit scraper
    scraper = RedditScraper()
    
    # Find pain points
    pain_points = scraper.find_user_pain_points(48)
    print(f"Found {len(pain_points)} user pain points:")
    for point in pain_points[:5]:
        print(f"- {point['title']} (score: {point['score']})")
    
    print("\n" + "="*50 + "\n")
    
    # Find contrarian ideas
    contrarian_ideas = scraper.find_contrarian_ideas(48)
    print(f"Found {len(contrarian_ideas)} contrarian ideas:")
    for idea in contrarian_ideas[:5]:
        print(f"- {idea['title']} (subreddit: {idea['subreddit']})")