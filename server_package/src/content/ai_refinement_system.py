import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
from pathlib import Path

class AIRefinementSystem:
    """Advanced AI system for refining and optimizing content quality"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.refinement_rules = self._load_refinement_rules()
        self.quality_metrics = {}
        self.refinement_history = []
        
    def _load_refinement_rules(self) -> Dict:
        """Load content refinement rules and standards"""
        return {
            'title_optimization': {
                'max_length': 60,
                'min_length': 30,
                'power_words': ['Ultimate', 'Secret', 'Proven', 'Instant', 'Revolutionary'],
                'emotional_triggers': ['Amazing', 'Shocking', 'Incredible', 'Unbelievable'],
                'numbers': r'\d+',
                'questions': r'\?$'
            },
            'description_optimization': {
                'min_length': 125,
                'max_length': 5000,
                'keyword_density': {'min': 0.02, 'max': 0.05},
                'call_to_action': ['subscribe', 'like', 'comment', 'share', 'click']
            },
            'content_quality': {
                'readability_score': {'min': 60, 'target': 80},
                'engagement_elements': ['questions', 'polls', 'challenges'],
                'structure_elements': ['intro', 'main_points', 'conclusion', 'cta']
            },
            'seo_optimization': {
                'primary_keyword_frequency': {'min': 3, 'max': 8},
                'secondary_keywords': {'count': 5, 'frequency': 2},
                'meta_tags': ['title', 'description', 'keywords']
            }
        }
    
    def refine_content(self, content: Dict) -> Dict:
        """Main content refinement function"""
        try:
            self.logger.info(f"Starting content refinement for: {content.get('title', 'Unknown')}")
            
            refined_content = content.copy()
            refinement_report = {
                'original_quality_score': self._calculate_quality_score(content),
                'refinements_applied': [],
                'improvement_areas': []
            }
            
            # Apply refinements
            refined_content = self._refine_title(refined_content, refinement_report)
            refined_content = self._refine_description(refined_content, refinement_report)
            refined_content = self._optimize_keywords(refined_content, refinement_report)
            refined_content = self._enhance_engagement(refined_content, refinement_report)
            refined_content = self._improve_structure(refined_content, refinement_report)
            refined_content = self._optimize_seo(refined_content, refinement_report)
            
            # Calculate final quality score
            refinement_report['final_quality_score'] = self._calculate_quality_score(refined_content)
            refinement_report['improvement_percentage'] = (
                (refinement_report['final_quality_score'] - refinement_report['original_quality_score']) 
                / refinement_report['original_quality_score'] * 100
            )
            
            refined_content['refinement_report'] = refinement_report
            
            # Store refinement history
            self.refinement_history.append({
                'timestamp': datetime.now().isoformat(),
                'original_score': refinement_report['original_quality_score'],
                'final_score': refinement_report['final_quality_score'],
                'improvements': len(refinement_report['refinements_applied'])
            })
            
            self.logger.info(f"Content refinement completed. Quality improved by {refinement_report['improvement_percentage']:.1f}%")
            return refined_content
            
        except Exception as e:
            self.logger.error(f"Error in content refinement: {e}")
            return content
    
    def _calculate_quality_score(self, content: Dict) -> float:
        """Calculate overall content quality score (0-100)"""
        try:
            scores = {
                'title_quality': self._score_title_quality(content.get('title', '')),
                'description_quality': self._score_description_quality(content.get('description', '')),
                'keyword_optimization': self._score_keyword_optimization(content),
                'engagement_potential': self._score_engagement_potential(content),
                'structure_quality': self._score_structure_quality(content),
                'seo_optimization': self._score_seo_optimization(content)
            }
            
            # Weighted average
            weights = {
                'title_quality': 0.25,
                'description_quality': 0.20,
                'keyword_optimization': 0.15,
                'engagement_potential': 0.15,
                'structure_quality': 0.15,
                'seo_optimization': 0.10
            }
            
            total_score = sum(scores[key] * weights[key] for key in scores)
            return round(total_score, 2)
            
        except Exception as e:
            self.logger.error(f"Error calculating quality score: {e}")
            return 50.0
    
    def _score_title_quality(self, title: str) -> float:
        """Score title quality (0-100)"""
        try:
            score = 0
            rules = self.refinement_rules['title_optimization']
            
            # Length check
            if rules['min_length'] <= len(title) <= rules['max_length']:
                score += 30
            elif len(title) < rules['min_length']:
                score += 15
            
            # Power words
            power_word_count = sum(1 for word in rules['power_words'] if word.lower() in title.lower())
            score += min(power_word_count * 15, 30)
            
            # Numbers
            if re.search(rules['numbers'], title):
                score += 20
            
            # Questions
            if re.search(rules['questions'], title):
                score += 20
            
            return min(score, 100)
            
        except Exception:
            return 50
    
    def _score_description_quality(self, description: str) -> float:
        """Score description quality (0-100)"""
        try:
            score = 0
            rules = self.refinement_rules['description_optimization']
            
            # Length check
            if len(description) >= rules['min_length']:
                score += 40
            else:
                score += (len(description) / rules['min_length']) * 40
            
            # Call to action
            cta_count = sum(1 for cta in rules['call_to_action'] if cta.lower() in description.lower())
            score += min(cta_count * 15, 30)
            
            # Structure (paragraphs)
            paragraphs = description.split('\n\n')
            if len(paragraphs) >= 3:
                score += 30
            else:
                score += len(paragraphs) * 10
            
            return min(score, 100)
            
        except Exception:
            return 50
    
    def _score_keyword_optimization(self, content: Dict) -> float:
        """Score keyword optimization (0-100)"""
        try:
            score = 0
            title = content.get('title', '').lower()
            description = content.get('description', '').lower()
            keywords = content.get('keywords', [])
            
            if not keywords:
                return 20  # Base score for having some content
            
            primary_keyword = keywords[0].lower() if keywords else ''
            
            # Primary keyword in title
            if primary_keyword in title:
                score += 30
            
            # Primary keyword frequency in description
            keyword_count = description.count(primary_keyword)
            if 3 <= keyword_count <= 8:
                score += 40
            elif keyword_count > 0:
                score += 20
            
            # Secondary keywords
            secondary_keywords = keywords[1:6] if len(keywords) > 1 else []
            secondary_found = sum(1 for kw in secondary_keywords if kw.lower() in description)
            score += min(secondary_found * 6, 30)
            
            return min(score, 100)
            
        except Exception:
            return 50
    
    def _score_engagement_potential(self, content: Dict) -> float:
        """Score engagement potential (0-100)"""
        try:
            score = 0
            title = content.get('title', '').lower()
            description = content.get('description', '').lower()
            
            # Questions in title or description
            if '?' in title or '?' in description:
                score += 25
            
            # Emotional triggers
            emotional_words = self.refinement_rules['title_optimization']['emotional_triggers']
            emotion_count = sum(1 for word in emotional_words if word.lower() in f"{title} {description}")
            score += min(emotion_count * 15, 30)
            
            # Call to action
            cta_words = self.refinement_rules['description_optimization']['call_to_action']
            cta_count = sum(1 for cta in cta_words if cta in description)
            score += min(cta_count * 10, 25)
            
            # Urgency indicators
            urgency_words = ['now', 'today', 'urgent', 'limited', 'exclusive']
            urgency_count = sum(1 for word in urgency_words if word in f"{title} {description}")
            score += min(urgency_count * 10, 20)
            
            return min(score, 100)
            
        except Exception:
            return 50
    
    def _score_structure_quality(self, content: Dict) -> float:
        """Score content structure quality (0-100)"""
        try:
            score = 0
            description = content.get('description', '')
            
            # Paragraph structure
            paragraphs = description.split('\n\n')
            if len(paragraphs) >= 3:
                score += 30
            
            # Bullet points or lists
            if '•' in description or '-' in description or re.search(r'\d+\.', description):
                score += 25
            
            # Clear sections
            section_indicators = ['introduction', 'overview', 'conclusion', 'summary']
            section_count = sum(1 for indicator in section_indicators if indicator.lower() in description.lower())
            score += min(section_count * 15, 30)
            
            # Timestamps (for video content)
            if re.search(r'\d+:\d+', description):
                score += 15
            
            return min(score, 100)
            
        except Exception:
            return 50
    
    def _score_seo_optimization(self, content: Dict) -> float:
        """Score SEO optimization (0-100)"""
        try:
            score = 0
            
            # Has keywords
            if content.get('keywords'):
                score += 30
            
            # Has tags
            if content.get('tags'):
                score += 25
            
            # Has category
            if content.get('category'):
                score += 20
            
            # Meta description length
            description = content.get('description', '')
            if 125 <= len(description) <= 300:
                score += 25
            
            return min(score, 100)
            
        except Exception:
            return 50
    
    def _refine_title(self, content: Dict, report: Dict) -> Dict:
        """Refine the content title"""
        try:
            title = content.get('title', '')
            original_title = title
            rules = self.refinement_rules['title_optimization']
            
            # Length optimization
            if len(title) > rules['max_length']:
                title = title[:rules['max_length']-3] + '...'
                report['refinements_applied'].append('Title length optimized')
            
            # Add power words if missing
            if not any(word.lower() in title.lower() for word in rules['power_words']):
                if 'finance' in title.lower():
                    title = f"Ultimate {title}"
                    report['refinements_applied'].append('Added power word to title')
            
            # Add numbers if missing and appropriate
            if not re.search(rules['numbers'], title) and len(title) < 50:
                if 'tips' in title.lower() or 'ways' in title.lower():
                    title = re.sub(r'\btips\b', '7 Tips', title, flags=re.IGNORECASE)
                    title = re.sub(r'\bways\b', '5 Ways', title, flags=re.IGNORECASE)
                    report['refinements_applied'].append('Added numbers to title')
            
            # Ensure question format if appropriate
            if 'how' in title.lower() and not title.endswith('?'):
                title += '?'
                report['refinements_applied'].append('Converted to question format')
            
            content['title'] = title
            
            if title != original_title:
                report['improvement_areas'].append('title_optimization')
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error refining title: {e}")
            return content
    
    def _refine_description(self, content: Dict, report: Dict) -> Dict:
        """Refine the content description"""
        try:
            description = content.get('description', '')
            original_description = description
            rules = self.refinement_rules['description_optimization']
            
            # Ensure minimum length
            if len(description) < rules['min_length']:
                # Add standard finance disclaimer and engagement elements
                additions = [
                    "\n\n💰 Want to learn more about building wealth? Subscribe for daily finance tips!",
                    "\n\n📈 What's your biggest financial goal? Let us know in the comments!",
                    "\n\n🔔 Don't forget to hit the notification bell for the latest market updates!"
                ]
                
                for addition in additions:
                    if len(description + addition) <= rules['max_length']:
                        description += addition
                        break
                
                report['refinements_applied'].append('Enhanced description length')
            
            # Add call-to-action if missing
            cta_present = any(cta.lower() in description.lower() for cta in rules['call_to_action'])
            if not cta_present:
                description += "\n\n👍 Like this video if it helped you and subscribe for more finance content!"
                report['refinements_applied'].append('Added call-to-action')
            
            # Improve structure with emojis and formatting
            if '\n\n' not in description and len(description) > 200:
                # Split into paragraphs at sentence boundaries
                sentences = description.split('. ')
                if len(sentences) >= 3:
                    mid_point = len(sentences) // 2
                    description = '. '.join(sentences[:mid_point]) + '.\n\n' + '. '.join(sentences[mid_point:])
                    report['refinements_applied'].append('Improved paragraph structure')
            
            content['description'] = description
            
            if description != original_description:
                report['improvement_areas'].append('description_optimization')
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error refining description: {e}")
            return content
    
    def _optimize_keywords(self, content: Dict, report: Dict) -> Dict:
        """Optimize keyword usage"""
        try:
            keywords = content.get('keywords', [])
            title = content.get('title', '').lower()
            description = content.get('description', '').lower()
            
            if not keywords:
                # Extract keywords from title and description
                finance_keywords = ['finance', 'money', 'investing', 'stocks', 'crypto', 'wealth', 'trading']
                extracted_keywords = [kw for kw in finance_keywords if kw in f"{title} {description}"]
                
                if extracted_keywords:
                    content['keywords'] = extracted_keywords[:5]
                    report['refinements_applied'].append('Extracted and added keywords')
            
            # Ensure primary keyword appears in title
            if keywords and keywords[0].lower() not in title:
                # Try to naturally incorporate the keyword
                primary_keyword = keywords[0]
                if len(content['title']) + len(primary_keyword) + 3 <= 60:
                    content['title'] = f"{primary_keyword.title()}: {content['title']}"
                    report['refinements_applied'].append('Added primary keyword to title')
            
            if 'keywords' in content:
                report['improvement_areas'].append('keyword_optimization')
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error optimizing keywords: {e}")
            return content
    
    def _enhance_engagement(self, content: Dict, report: Dict) -> Dict:
        """Enhance engagement elements"""
        try:
            title = content.get('title', '')
            description = content.get('description', '')
            
            engagement_enhanced = False
            
            # Add engagement questions if missing
            if '?' not in description:
                engagement_questions = [
                    "What's your experience with this?",
                    "Have you tried this strategy?",
                    "What would you add to this list?",
                    "Which tip resonated with you most?"
                ]
                
                # Add a relevant question based on content
                if 'investing' in f"{title} {description}".lower():
                    description += "\n\n💭 What's your favorite investment strategy? Share in the comments!"
                    engagement_enhanced = True
                elif 'money' in f"{title} {description}".lower():
                    description += "\n\n💰 What's your biggest money goal this year? Let us know below!"
                    engagement_enhanced = True
            
            # Add interactive elements
            if 'poll' not in description.lower() and 'vote' not in description.lower():
                if len(description) < 4000:  # Ensure we don't exceed limits
                    description += "\n\n📊 Quick poll: Are you more focused on saving or investing right now?"
                    engagement_enhanced = True
            
            if engagement_enhanced:
                content['description'] = description
                report['refinements_applied'].append('Enhanced engagement elements')
                report['improvement_areas'].append('engagement_optimization')
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error enhancing engagement: {e}")
            return content
    
    def _improve_structure(self, content: Dict, report: Dict) -> Dict:
        """Improve content structure"""
        try:
            description = content.get('description', '')
            original_description = description
            
            # Add structure if missing
            if '\n\n' not in description and len(description) > 300:
                # Create structured format
                structured_description = self._create_structured_format(description)
                if structured_description != description:
                    content['description'] = structured_description
                    report['refinements_applied'].append('Improved content structure')
            
            # Add timestamps for video content
            if 'video' in content.get('type', '').lower() and ':' not in description:
                if len(description) < 4500:
                    description += "\n\n⏰ Timestamps:\n0:00 Introduction\n1:30 Main Content\n8:45 Key Takeaways\n9:30 Conclusion"
                    content['description'] = description
                    report['refinements_applied'].append('Added video timestamps')
            
            if content.get('description') != original_description:
                report['improvement_areas'].append('structure_optimization')
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error improving structure: {e}")
            return content
    
    def _create_structured_format(self, description: str) -> str:
        """Create a structured format for description"""
        try:
            # Split into sentences
            sentences = [s.strip() for s in description.split('.') if s.strip()]
            
            if len(sentences) < 3:
                return description
            
            # Group sentences into sections
            intro = sentences[0] + '.'
            main_content = '. '.join(sentences[1:-1]) + '.'
            conclusion = sentences[-1] + '.' if not sentences[-1].endswith('.') else sentences[-1]
            
            # Create structured format
            structured = f"{intro}\n\n{main_content}\n\n{conclusion}"
            
            return structured
            
        except Exception:
            return description
    
    def _optimize_seo(self, content: Dict, report: Dict) -> Dict:
        """Optimize SEO elements"""
        try:
            # Ensure tags are present
            if not content.get('tags'):
                # Generate tags from keywords and content
                keywords = content.get('keywords', [])
                title = content.get('title', '').lower()
                
                suggested_tags = []
                
                # Add keyword-based tags
                for keyword in keywords[:3]:
                    suggested_tags.append(keyword)
                
                # Add content-type tags
                if 'tutorial' in title or 'how to' in title:
                    suggested_tags.append('tutorial')
                if 'tips' in title:
                    suggested_tags.append('tips')
                if 'finance' in title:
                    suggested_tags.extend(['finance', 'money', 'financial education'])
                
                # Add trending tags
                trending_tags = ['2024', 'beginner friendly', 'step by step']
                suggested_tags.extend(trending_tags[:2])
                
                content['tags'] = list(set(suggested_tags))[:10]  # Limit to 10 unique tags
                report['refinements_applied'].append('Generated SEO tags')
            
            # Ensure category is set
            if not content.get('category'):
                title_lower = content.get('title', '').lower()
                finance_keywords = ['finance', 'money', 'investing', 'crypto', 'stock', 'trading', 'wealth', 'income', 'budget', 'savings', 'retirement', 'portfolio', 'market', 'economy', 'financial']
                if any(word in title_lower for word in finance_keywords):
                    content['category'] = 'Education'
                else:
                    content['category'] = 'Education'  # Default to Education for finance channel
                report['refinements_applied'].append('Set content category')
            
            if 'tags' in content or 'category' in content:
                report['improvement_areas'].append('seo_optimization')
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error optimizing SEO: {e}")
            return content
    
    def get_refinement_suggestions(self, content: Dict) -> List[Dict]:
        """Get specific refinement suggestions without applying them"""
        try:
            suggestions = []
            
            # Title suggestions
            title = content.get('title', '')
            if len(title) < 30:
                suggestions.append({
                    'area': 'title',
                    'issue': 'Title too short',
                    'suggestion': 'Expand title to 30-60 characters for better SEO',
                    'priority': 'medium'
                })
            
            # Description suggestions
            description = content.get('description', '')
            if len(description) < 125:
                suggestions.append({
                    'area': 'description',
                    'issue': 'Description too short',
                    'suggestion': 'Expand description to at least 125 characters',
                    'priority': 'high'
                })
            
            # Keyword suggestions
            if not content.get('keywords'):
                suggestions.append({
                    'area': 'keywords',
                    'issue': 'No keywords defined',
                    'suggestion': 'Add 3-5 relevant keywords for better discoverability',
                    'priority': 'high'
                })
            
            # Engagement suggestions
            if '?' not in f"{title} {description}":
                suggestions.append({
                    'area': 'engagement',
                    'issue': 'No questions for engagement',
                    'suggestion': 'Add questions to encourage viewer interaction',
                    'priority': 'medium'
                })
            
            return suggestions
            
        except Exception as e:
            self.logger.error(f"Error getting refinement suggestions: {e}")
            return []
    
    def get_quality_report(self, content: Dict) -> Dict:
        """Generate a comprehensive quality report"""
        try:
            quality_score = self._calculate_quality_score(content)
            suggestions = self.get_refinement_suggestions(content)
            
            report = {
                'overall_quality_score': quality_score,
                'quality_grade': self._get_quality_grade(quality_score),
                'detailed_scores': {
                    'title_quality': self._score_title_quality(content.get('title', '')),
                    'description_quality': self._score_description_quality(content.get('description', '')),
                    'keyword_optimization': self._score_keyword_optimization(content),
                    'engagement_potential': self._score_engagement_potential(content),
                    'structure_quality': self._score_structure_quality(content),
                    'seo_optimization': self._score_seo_optimization(content)
                },
                'improvement_suggestions': suggestions,
                'strengths': self._identify_strengths(content),
                'weaknesses': self._identify_weaknesses(content)
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating quality report: {e}")
            return {'overall_quality_score': 50, 'quality_grade': 'C'}
    
    def _get_quality_grade(self, score: float) -> str:
        """Convert quality score to letter grade"""
        if score >= 90:
            return 'A+'
        elif score >= 85:
            return 'A'
        elif score >= 80:
            return 'B+'
        elif score >= 75:
            return 'B'
        elif score >= 70:
            return 'C+'
        elif score >= 65:
            return 'C'
        elif score >= 60:
            return 'D+'
        elif score >= 55:
            return 'D'
        else:
            return 'F'
    
    def _identify_strengths(self, content: Dict) -> List[str]:
        """Identify content strengths"""
        strengths = []
        
        title = content.get('title', '')
        description = content.get('description', '')
        
        if 30 <= len(title) <= 60:
            strengths.append('Optimal title length')
        
        if len(description) >= 125:
            strengths.append('Adequate description length')
        
        if content.get('keywords'):
            strengths.append('Keywords defined')
        
        if '?' in f"{title} {description}":
            strengths.append('Includes engagement questions')
        
        return strengths
    
    def _identify_weaknesses(self, content: Dict) -> List[str]:
        """Identify content weaknesses"""
        weaknesses = []
        
        title = content.get('title', '')
        description = content.get('description', '')
        
        if len(title) < 30:
            weaknesses.append('Title too short')
        elif len(title) > 60:
            weaknesses.append('Title too long')
        
        if len(description) < 125:
            weaknesses.append('Description too short')
        
        if not content.get('keywords'):
            weaknesses.append('No keywords defined')
        
        if not content.get('tags'):
            weaknesses.append('No tags defined')
        
        return weaknesses