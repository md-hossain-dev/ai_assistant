import re
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


class CybersecurityClassifier:
    """Classifier to determine if a query is cybersecurity-related"""
    
    def __init__(self):
        # Keywords related to cybersecurity and malware removal
        self.cybersecurity_keywords = {
            'malware': ['malware', 'virus', 'trojan', 'ransomware', 'spyware', 'adware', 'rootkit', 'keylogger', 'worm', 'backdoor', 'botnet'],
            'security': ['security', 'hack', 'breach', 'vulnerability', 'exploit', 'firewall', 'antivirus', 'encryption', 'authentication', 'authorization'],
            'network': ['network', 'wifi', 'router', 'vpn', 'proxy', 'dns', 'ip', 'port', 'protocol', 'packet', 'traffic', 'bandwidth'],
            'privacy': ['privacy', 'data breach', 'identity theft', 'phishing', 'social engineering', 'password', 'personal data', 'gdpr', 'compliance'],
            'system': ['system', 'registry', 'process', 'service', 'startup', 'task manager', 'command prompt', 'powershell', 'terminal', 'system32'],
            'removal': ['remove', 'delete', 'clean', 'scan', 'quarantine', 'disinfect', 'restore', 'uninstall', 'cleanup', 'repair'],
            'tools': ['malwarebytes', 'avast', 'norton', 'mcafee', 'kaspersky', 'windows defender', 'bitdefender', 'eset', 'trend micro'],
            'threats': ['threat', 'attack', 'infection', 'compromise', 'backdoor', 'botnet', 'ddos', 'sql injection', 'xss', 'csrf'],
            'prevention': ['prevent', 'protect', 'secure', 'update', 'patch', 'backup', 'recovery', 'monitoring', 'alert', 'detection'],
            'analysis': ['analyze', 'detect', 'identify', 'investigate', 'forensics', 'log analysis', 'incident response', 'threat hunting'],
            'cybersecurity_concepts': ['zero-day', 'penetration testing', 'red team', 'blue team', 'siem', 'soar', 'edr', 'xdr', 'mdr'],
            'compliance': ['iso 27001', 'nist', 'pci dss', 'hipaa', 'sox', 'compliance', 'audit', 'certification'],
            'incident_response': ['incident', 'response', 'containment', 'eradication', 'recovery', 'lessons learned', 'post-incident'],
            'secure_coding': ['secure coding', 'code review', 'static analysis', 'dynamic analysis', 'sast', 'dast', 'owasp'],
            'cloud_security': ['cloud security', 'aws security', 'azure security', 'gcp security', 'container security', 'kubernetes security'],
            'iot_security': ['iot security', 'smart device', 'embedded security', 'device security', 'sensor security']
        }
        
        # Common non-cybersecurity topics to exclude
        self.excluded_keywords = [
            'cooking', 'recipe', 'food', 'restaurant', 'travel', 'vacation', 'hotel',
            'shopping', 'fashion', 'clothing', 'makeup', 'beauty', 'health', 'fitness',
            'sports', 'game', 'entertainment', 'movie', 'music', 'book', 'literature',
            'education', 'school', 'university', 'course', 'study', 'homework',
            'business', 'marketing', 'sales', 'finance', 'investment', 'stock',
            'relationship', 'dating', 'marriage', 'family', 'parenting', 'children',
            'cooking', 'baking', 'recipe', 'food', 'restaurant', 'dining',
            'fashion', 'style', 'clothing', 'shoes', 'accessories',
            'travel', 'vacation', 'tourism', 'hotel', 'booking',
            'entertainment', 'movie', 'film', 'tv show', 'series',
            'music', 'song', 'artist', 'album', 'concert',
            'sports', 'football', 'basketball', 'tennis', 'golf',
            'health', 'medical', 'doctor', 'hospital', 'medicine',
            'fitness', 'workout', 'exercise', 'gym', 'yoga'
        ]
    
    def classify_query(self, query: str) -> Dict[str, any]:
        """
        Classify if a query is cybersecurity-related
        
        Args:
            query: The user's input query
            
        Returns:
            Dictionary with classification results
        """
        query_lower = query.lower().strip()
        
        # Check for excluded topics first
        if self._contains_excluded_topics(query_lower):
            return {
                'is_cybersecurity': False,
                'confidence': 0.0,
                'reason': 'Query contains non-cybersecurity topics',
                'matched_keywords': [],
                'category': 'excluded'
            }
        
        # Check for cybersecurity keywords
        matched_keywords = []
        category_scores = {}
        total_score = 0
        
        for category, keywords in self.cybersecurity_keywords.items():
            category_score = 0
            for keyword in keywords:
                if keyword in query_lower:
                    matched_keywords.append(f"{category}: {keyword}")
                    category_score += 1
                    total_score += 1
            
            if category_score > 0:
                category_scores[category] = category_score
        
        # Calculate confidence score with improved algorithm
        confidence = self._calculate_confidence(query_lower, total_score, len(matched_keywords), category_scores)
        
        # Determine primary category
        primary_category = max(category_scores.items(), key=lambda x: x[1])[0] if category_scores else 'general'
        
        is_cybersecurity = confidence >= 0.4  # Slightly higher threshold for better accuracy
        
        return {
            'is_cybersecurity': is_cybersecurity,
            'confidence': confidence,
            'reason': f"Matched {len(matched_keywords)} cybersecurity keywords across {len(category_scores)} categories" if is_cybersecurity else "Insufficient cybersecurity keywords",
            'matched_keywords': matched_keywords,
            'category_scores': category_scores,
            'primary_category': primary_category,
            'score': total_score
        }
    
    def _calculate_confidence(self, query: str, total_score: int, keyword_count: int, category_scores: Dict[str, int]) -> float:
        """Calculate confidence score using multiple factors"""
        # Base score from keyword matches
        base_score = min(total_score / 2.0, 1.0)
        
        # Bonus for multiple categories
        category_bonus = min(len(category_scores) * 0.1, 0.3)
        
        # Penalty for very short queries
        length_penalty = 0.0
        if len(query.split()) < 3:
            length_penalty = 0.2
        
        # Bonus for specific cybersecurity terms
        specific_terms = ['malware', 'virus', 'security', 'hack', 'breach', 'firewall', 'antivirus']
        specific_bonus = 0.0
        for term in specific_terms:
            if term in query:
                specific_bonus += 0.1
        
        confidence = base_score + category_bonus - length_penalty + specific_bonus
        return min(max(confidence, 0.0), 1.0)
    
    def _contains_excluded_topics(self, query: str) -> bool:
        """Check if query contains excluded non-cybersecurity topics"""
        for keyword in self.excluded_keywords:
            if keyword in query:
                return True
        return False
    
    def get_cybersecurity_prompt(self, query: str, category: str = 'general') -> str:
        """
        Generate a cybersecurity-specific prompt for the AI model
        
        Args:
            query: The user's cybersecurity query
            category: The primary category of the query
            
        Returns:
            Formatted prompt for cybersecurity assistance
        """
        category_prompts = {
            'malware': """You are a cybersecurity expert specializing in malware detection and removal. 
            Provide clear, step-by-step guidance for malware removal while emphasizing safety.
            Focus on: safe removal procedures, system protection, prevention strategies.""",
            
            'security': """You are a cybersecurity expert specializing in security best practices and threat prevention.
            Provide actionable security advice and recommendations for protecting systems and data.""",
            
            'network': """You are a cybersecurity expert specializing in network security and infrastructure protection.
            Provide guidance on network security, monitoring, and threat detection.""",
            
            'privacy': """You are a cybersecurity expert specializing in data privacy and protection.
            Provide advice on protecting personal information and maintaining privacy online.""",
            
            'removal': """You are a cybersecurity expert specializing in malware removal and system cleanup.
            Provide safe, effective procedures for removing threats and restoring system integrity.""",
            
            'analysis': """You are a cybersecurity expert specializing in threat analysis and incident response.
            Provide guidance on analyzing security incidents and implementing response procedures."""
        }
        
        system_prompt = category_prompts.get(category, """You are a cybersecurity expert specializing in malware removal and security issues. 
        Provide clear, actionable advice for cybersecurity problems. Focus on:
        - Safe malware removal procedures
        - Security best practices
        - System protection measures
        - Threat prevention strategies
        
        Always prioritize user safety and recommend professional help for serious security issues.""")
        
        return f"{system_prompt}\n\nUser Query: {query}\n\nCybersecurity Expert:"
    
    def get_rejection_message(self) -> str:
        """Get the standard rejection message for non-cybersecurity queries"""
        return "Sorry, I can only help with cybersecurity-related queries. Please ask me about malware removal, security threats, system protection, network security, privacy protection, or other cybersecurity topics."


# Global instance of the classifier
cybersecurity_classifier = CybersecurityClassifier() 