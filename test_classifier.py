#!/usr/bin/env python
"""
Test script for the cybersecurity classifier
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_assistant.settings')
django.setup()

from assistant.classifier import cybersecurity_classifier

def test_classifier():
    """Test the cybersecurity classifier with various queries"""
    
    test_queries = [
        # Cybersecurity queries (should be classified as True)
        "How do I remove malware from my computer?",
        "What are signs of a virus infection?",
        "How to protect against ransomware?",
        "Is my WiFi secure?",
        "How to detect phishing emails?",
        "My computer is running slow, could it be malware?",
        "How to scan for viruses?",
        "What is a firewall and do I need one?",
        "How to remove spyware?",
        "My antivirus detected a threat, what should I do?",
        
        # Non-cybersecurity queries (should be classified as False)
        "What's the weather like today?",
        "How do I cook pasta?",
        "What's the best restaurant in town?",
        "How to lose weight?",
        "What movie should I watch?",
        "How to fix my car?",
        "What's the capital of France?",
        "How to play guitar?",
        "What's the best way to study?",
        "How to make friends?"
    ]
    
    print("Testing Cybersecurity Classifier")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        result = cybersecurity_classifier.classify_query(query)
        
        status = "✅ CYBERSECURITY" if result['is_cybersecurity'] else "❌ NON-CYBERSECURITY"
        confidence = f"{result['confidence']:.2f}"
        
        print(f"{i:2d}. {status} (confidence: {confidence})")
        print(f"    Query: {query}")
        print(f"    Reason: {result['reason']}")
        if result['matched_keywords']:
            print(f"    Keywords: {', '.join(result['matched_keywords'])}")
        print()

if __name__ == "__main__":
    test_classifier() 