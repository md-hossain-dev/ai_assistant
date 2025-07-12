#!/usr/bin/env python3
"""
Comprehensive test script for the Cybersecurity AI Assistant API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"Test: {title}")
    print("=" * 60)

def test_health():
    """Test health endpoint"""
    print_header("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/api/health/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("PASS: Health Check")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Service: {data.get('service', 'unknown')}")
            print(f"   Classifier: {data.get('classifier', 'unknown')}")
            
            if 'model' in data:
                model_info = data['model']
                print(f"   Model: {model_info.get('model_name', 'unknown')}")
                print(f"   Provider: {model_info.get('provider', 'unknown')}")
                print(f"   OpenAI: {model_info.get('use_openai', False)}")
            
            return True
        else:
            print(f"FAIL: Health Check (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"FAIL: Health Check - {str(e)}")
        return False

def test_classification():
    """Test classification endpoint"""
    print_header("Classification Test")
    
    test_queries = [
        ("How do I remove malware from my computer?", True),
        ("What's the weather like today?", False),
        ("My computer is running slowly and showing popups", True),
        ("How to make chocolate cake?", False),
        ("I think my account was hacked", True),
        ("What's the best restaurant in town?", False),
        ("How can I protect my network from attacks?", True),
        ("What's the latest movie?", False),
        ("My antivirus detected a threat", True),
        ("How to cook pasta?", False)
    ]
    
    passed = 0
    total = len(test_queries)
    
    for query, expected in test_queries:
        try:
            response = requests.post(
                f"{BASE_URL}/api/classify/",
                json={"message": query},
                timeout=10
            )
            result = response.json()
            
            actual = result['is_cybersecurity']
            confidence = result['confidence']
            category = result.get('primary_category', 'general')
            
            status = "PASS" if actual == expected else "FAIL"
            result_text = "Cybersecurity" if actual else "Non-cybersecurity"
            expected_text = "Cybersecurity" if expected else "Non-cybersecurity"
            
            print(f"{status} '{query}'")
            print(f"   Expected: {expected_text}")
            print(f"   Got: {result_text}")
            print(f"   Confidence: {confidence:.2f}")
            print(f"   Category: {category}")
            
            if actual == expected:
                passed += 1
            
        except Exception as e:
            print(f"FAIL: Classification failed for '{query}': {e}")
    
    print(f"\nResults: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    return passed == total

def test_chat():
    """Test chat endpoint"""
    print_header("Chat Test")
    
    test_messages = [
        ("How do I remove malware from my computer?", True),
        ("What should I do if my account was hacked?", True),
        ("How can I protect my network from attacks?", True),
        ("What's the weather like today?", False),
        ("How to make chocolate cake?", False)
    ]
    
    passed = 0
    total = len(test_messages)
    
    for message, expected_cybersecurity in test_messages:
        try:
            print(f"Testing: '{message}'")
            
            response = requests.post(
                f"{BASE_URL}/api/chat/",
                json={"message": message},
                timeout=30
            )
            result = response.json()
            
            ai_response = result['response']
            is_cybersecurity = result.get('is_cybersecurity', False)
            response_time = result.get('response_time', 0)
            tokens_used = result.get('tokens_used', 0)
            
            status = "PASS" if is_cybersecurity == expected_cybersecurity else "FAIL"
            print(f"{status} Response: {ai_response[:100]}...")
            print(f"   Cybersecurity: {is_cybersecurity} (expected: {expected_cybersecurity})")
            print(f"   Response time: {response_time:.2f}s")
            print(f"   Tokens used: {tokens_used}")
            
            if is_cybersecurity == expected_cybersecurity:
                passed += 1
            
        except Exception as e:
            print(f"FAIL: Chat failed for '{message}': {e}")
    
    print(f"\nResults: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    return passed == total

def test_stats():
    """Test statistics endpoint"""
    print_header("Statistics Test")
    
    try:
        response = requests.get(f"{BASE_URL}/api/stats/?days=30", timeout=10)
        stats = response.json()
        
        print("PASS: Statistics retrieved successfully")
        print(f"   Period: {stats.get('period_days', 0)} days")
        print(f"   Total conversations: {stats.get('total_conversations', 0)}")
        print(f"   Cybersecurity conversations: {stats.get('estimated_cybersecurity_conversations', 0)}")
        print(f"   Cybersecurity percentage: {stats.get('cybersecurity_percentage', 0):.1f}%")
        
        return True
        
    except Exception as e:
        print(f"FAIL: Statistics failed: {e}")
        return False

def test_model_info():
    """Test model info endpoint"""
    print_header("Model Info Test")
    
    try:
        response = requests.get(f"{BASE_URL}/api/model-info/", timeout=10)
        model_info = response.json()
        
        print("PASS: Model info retrieved successfully")
        print(f"   Model: {model_info.get('model_name', 'unknown')}")
        print(f"   Max tokens: {model_info.get('max_tokens', 'unknown')}")
        print(f"   Provider: {model_info.get('provider', 'unknown')}")
        print(f"   OpenAI: {model_info.get('use_openai', False)}")
        
        return True
        
    except Exception as e:
        print(f"FAIL: Model info failed: {e}")
        return False

def main():
    """Main test function"""
    print("Cybersecurity AI Assistant - API Test Suite")
    print("=" * 60)
    
    # Check if server is running
    print("Checking if server is running...")
    try:
        response = requests.get(f"{BASE_URL}/api/health/", timeout=5)
        if response.status_code == 200:
            print("Server is running")
        else:
            print("Server is not responding properly")
            print("Please start the server first: python start.py")
            return
    except Exception as e:
        print("Cannot connect to server")
        print("Please start the server first: python start.py")
        return
    
    # Run all tests
    tests = [
        ("Health Check", test_health),
        ("Classification", test_classification),
        ("Chat", test_chat),
        ("Statistics", test_stats),
        ("Model Info", test_model_info)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"FAIL: {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("All tests passed! The Cybersecurity AI Assistant is working correctly.")
    else:
        print("Some tests failed. Please check the configuration and try again.")
    
    print("\nNext steps:")
    print("1. Visit http://localhost:8000 for the web interface")
    print("2. Run demo: python start.py demo")
    print("3. Try different cybersecurity queries")

if __name__ == "__main__":
    main() 