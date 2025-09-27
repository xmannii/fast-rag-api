#!/usr/bin/env python3

"""
📊 Performance Test Example

Simple performance testing script for the RAG API.
Run with: python examples/performance_test.py
"""

import requests
import json
import time
import statistics

# Configuration
API_BASE = "http://localhost:3000/api"

def make_request(endpoint, method="GET", data=None):
    """Make a request and measure response time."""
    url = f"{API_BASE}{endpoint}"
    
    start_time = time.time()
    
    try:
        if method.upper() == "GET":
            response = requests.get(url)
        elif method.upper() == "POST":
            response = requests.post(url, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, json=data)
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        return {
            "success": response.status_code == 200,
            "status": response.status_code,
            "response_time": response_time,
            "data": response.json() if response.content else {}
        }
    except Exception as e:
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        return {
            "success": False,
            "status": 0,
            "response_time": response_time,
            "error": str(e)
        }

def test_chat_performance(num_requests=5):
    """Test chat endpoint performance."""
    print(f"🤖 Testing Chat Performance ({num_requests} requests)")
    print("-" * 50)
    
    # Test data
    test_messages = [
        "Hello! How are you?",
        "What is artificial intelligence?",
        "Tell me about machine learning",
        "How does RAG work?",
        "What are embeddings?"
    ]
    
    response_times = []
    errors = 0
    
    for i in range(num_requests):
        message = test_messages[i % len(test_messages)]
        
        data = {
            "messages": [
                {
                    "role": "user",
                    "parts": [{"type": "text", "text": message}]
                }
            ]
        }
        
        result = make_request("/chat", "POST", data)
        
        if result["success"]:
            response_times.append(result["response_time"])
            print(f"  Request {i+1}: {result['response_time']:.1f}ms ✅")
        else:
            errors += 1
            print(f"  Request {i+1}: {result['response_time']:.1f}ms ❌ ({result.get('error', 'Unknown error')})")
    
    # Calculate statistics
    if response_times:
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        median_time = statistics.median(response_times)
        
        print(f"\n📊 Chat Performance Stats:")
        print(f"  Average: {avg_time:.1f}ms")
        print(f"  Min: {min_time:.1f}ms")
        print(f"  Max: {max_time:.1f}ms")
        print(f"  Median: {median_time:.1f}ms")
        print(f"  Success Rate: {len(response_times)}/{num_requests} ({len(response_times)/num_requests*100:.1f}%)")
    
    return response_times

def test_context_search_performance(num_requests=10):
    """Test context search performance."""
    print(f"\n🔍 Testing Context Search Performance ({num_requests} requests)")
    print("-" * 50)
    
    # Test queries
    test_queries = [
        "financial report",
        "customer analysis",
        "product portfolio",
        "team structure",
        "technology stack"
    ]
    
    response_times = []
    errors = 0
    
    for i in range(num_requests):
        query = test_queries[i % len(test_queries)]
        
        data = {
            "query": query,
            "limit": 5,
            "threshold": 0.3
        }
        
        result = make_request("/context/search", "POST", data)
        
        if result["success"]:
            response_times.append(result["response_time"])
            count = result["data"]["count"]
            print(f"  Request {i+1}: {result['response_time']:.1f}ms ✅ (Found {count} results)")
        else:
            errors += 1
            print(f"  Request {i+1}: {result['response_time']:.1f}ms ❌ ({result.get('error', 'Unknown error')})")
    
    # Calculate statistics
    if response_times:
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        median_time = statistics.median(response_times)
        
        print(f"\n📊 Context Search Performance Stats:")
        print(f"  Average: {avg_time:.1f}ms")
        print(f"  Min: {min_time:.1f}ms")
        print(f"  Max: {max_time:.1f}ms")
        print(f"  Median: {median_time:.1f}ms")
        print(f"  Success Rate: {len(response_times)}/{num_requests} ({len(response_times)/num_requests*100:.1f}%)")
    
    return response_times

def test_embedding_performance(num_requests=5):
    """Test embedding generation performance."""
    print(f"\n🧠 Testing Embedding Performance ({num_requests} requests)")
    print("-" * 50)
    
    # Test texts
    test_texts = [
        ["Q3 2024 Financial Report"],
        ["Customer Analysis Report", "Product Portfolio"],
        ["Team Structure", "Technology Stack", "Company Overview"]
    ]
    
    response_times = []
    errors = 0
    
    for i in range(num_requests):
        texts = test_texts[i % len(test_texts)]
        
        data = {"texts": texts}
        
        result = make_request("/embedding", "POST", data)
        
        if result["success"]:
            response_times.append(result["response_time"])
            count = result["data"]["count"]
            print(f"  Request {i+1}: {result['response_time']:.1f}ms ✅ (Generated {count} embeddings)")
        else:
            errors += 1
            print(f"  Request {i+1}: {result['response_time']:.1f}ms ❌ ({result.get('error', 'Unknown error')})")
    
    # Calculate statistics
    if response_times:
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        median_time = statistics.median(response_times)
        
        print(f"\n📊 Embedding Performance Stats:")
        print(f"  Average: {avg_time:.1f}ms")
        print(f"  Min: {min_time:.1f}ms")
        print(f"  Max: {max_time:.1f}ms")
        print(f"  Median: {median_time:.1f}ms")
        print(f"  Success Rate: {len(response_times)}/{num_requests} ({len(response_times)/num_requests*100:.1f}%)")
    
    return response_times

def main():
    """Run the performance test."""
    print("📊 RAG API Performance Test")
    print("==========================")
    
    # Check if server is running
    try:
        response = requests.get(f"{API_BASE}/")
        if response.status_code != 200:
            print("❌ Server is not running!")
            print("💡 Start the server with: bun run dev")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Start the server with: bun run dev")
        return
    
    print("✅ Server is running")
    
    # Run performance tests
    chat_times = test_chat_performance(5)
    search_times = test_context_search_performance(10)
    embedding_times = test_embedding_performance(5)
    
    # Overall summary
    print(f"\n📈 Overall Performance Summary:")
    print("=" * 50)
    
    if chat_times:
        print(f"Chat Average: {statistics.mean(chat_times):.1f}ms")
    if search_times:
        print(f"Search Average: {statistics.mean(search_times):.1f}ms")
    if embedding_times:
        print(f"Embedding Average: {statistics.mean(embedding_times):.1f}ms")
    
    print("\n💡 Performance Tips:")
    print("  - Chat responses depend on model size and complexity")
    print("  - Context search speed depends on database size")
    print("  - Embedding generation depends on text length and model")
    print("  - Consider caching for frequently accessed data")
    
    print("\n🎉 Performance test completed!")

if __name__ == "__main__":
    main()
