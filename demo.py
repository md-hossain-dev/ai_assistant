#!/usr/bin/env python3
"""
Demo script for Cybersecurity AI Assistant
Shows the classification and response capabilities
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"Demo: {title}")
    print("=" * 60)

def test_classification_demo():
    """Demo the classification system"""
    print_header("Cybersecurity Classification Demo")
    
    test_queries = [
        ("How do I remove malware from my computer?", "Cybersecurity - Malware removal"),
        ("What's the weather like today?", "Non-cybersecurity - Weather"),
        ("My computer is running slowly and showing popups", "Cybersecurity - System issues"),
        ("How to make chocolate cake?", "Non-cybersecurity - Cooking"),
        ("I think my account was hacked", "Cybersecurity - Account security"),
        ("What's the best restaurant in town?", "Non-cybersecurity - Food"),
        ("How can I protect my network from attacks?", "Cybersecurity - Network security"),
        ("What's the latest movie?", "Non-cybersecurity - Entertainment")
    ]
    
    for query, expected in test_queries:
        try:
            response = requests.post(
                f"{BASE_URL}/api/classify/",
                json={"message": query}
            )
            result = response.json()
            
            status = "SECURITY" if result['is_cybersecurity'] else "NON-SECURITY"
            confidence = result['confidence']
            category = result.get('primary_category', 'general')
            
            print(f"{status} Query: '{query}'")
            print(f"   Expected: {expected}")
            print(f"   Result: {'Cybersecurity' if result['is_cybersecurity'] else 'Non-cybersecurity'}")
            print(f"   Confidence: {confidence:.2f}")
            print(f"   Category: {category}")
            print()
            
        except Exception as e:
            print(f"Error testing query '{query}': {e}")

def test_chat_demo():
    """Demo the chat functionality"""
    print_header("Cybersecurity Chat Demo")
    
    test_messages = [
        "How do I remove malware from my computer?",
        "What should I do if my account was hacked?",
        "How can I protect my network from attacks?",
        "What's the weather like today?",
        "How to make chocolate cake?"
    ]
    
    for message in test_messages:
        try:
            print(f"User: {message}")
            
            response = requests.post(
                f"{BASE_URL}/api/chat/",
                json={"message": message}
            )
            result = response.json()
            
            # Show response
            ai_response = result['response']
            is_cybersecurity = result.get('is_cybersecurity', False)
            
            if is_cybersecurity:
                print(f"AI (Security): {ai_response[:200]}...")
            else:
                print(f"AI (Rejection): {ai_response}")
            
            print(f"   Response time: {result.get('response_time', 0):.2f}s")
            print(f"   Tokens used: {result.get('tokens_used', 0)}")
            print()
            
            time.sleep(1)  # Small delay for demo effect
            
        except Exception as e:
            print(f"Error testing message '{message}': {e}")

def test_stats_demo():
    """Demo the statistics functionality"""
    print_header("Statistics Demo")
    
    try:
        response = requests.get(f"{BASE_URL}/api/stats/")
        stats = response.json()
        
        print("Current Statistics:")
        print(f"   Period: {stats.get('period_days', 0)} days")
        print(f"   Total conversations: {stats.get('total_conversations', 0)}")
        print(f"   Cybersecurity conversations: {stats.get('estimated_cybersecurity_conversations', 0)}")
        print(f"   Cybersecurity percentage: {stats.get('cybersecurity_percentage', 0):.1f}%")
        
    except Exception as e:
        print(f"Error getting statistics: {e}")

def test_health_demo():
    """Demo the health check"""
    print_header("Health Check Demo")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health/")
        health = response.json()
        
        print("System Health:")
        print(f"   Status: {health.get('status', 'unknown')}")
        print(f"   Service: {health.get('service', 'unknown')}")
        print(f"   Classifier: {health.get('classifier', 'unknown')}")
        
        if 'model' in health:
            model_info = health['model']
            print(f"   Model: {model_info.get('model_name', 'unknown')}")
            print(f"   Provider: {model_info.get('provider', 'unknown')}")
            print(f"   OpenAI: {model_info.get('use_openai', False)}")
        
    except Exception as e:
        print(f"Error checking health: {e}")

def main():
    """Main demo function"""
    print("Cybersecurity AI Assistant - Demo")
    print("This demo showcases the classification and response capabilities")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/api/health/", timeout=5)
        if response.status_code == 200:
            print("Server is running")
        else:
            print("Server is not responding properly")
            return
    except Exception as e:
        print("Cannot connect to server. Please start the server first:")
        print("   python start.py")
        return
    
    # Run demos
    test_health_demo()
    test_classification_demo()
    test_chat_demo()
    test_stats_demo()
    
    print_header("Demo Complete")
    print("Demo completed successfully!")
    print("\nNext steps:")
    print("1. Visit http://localhost:8000 for the web interface")
    print("2. Try different cybersecurity queries")
    print("3. Check the API documentation")
    print("4. Explore the code structure")

if __name__ == "__main__":
    main() 