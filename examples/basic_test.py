#!/usr/bin/env python3

"""
🧪 Basic API Test Example

Simple Python script to test all RAG API endpoints.
Run with: python examples/basic_test.py
"""

import requests
import json

# Configuration
API_BASE = "http://localhost:3000/api"

def test_endpoints():
    """Test all API endpoints."""
    print("🚀 Testing RAG API Endpoints")
    print("============================")
    
    # Test 1: Health check
    print("\n1. Health Check")
    try:
        response = requests.get("http://localhost:3000/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Basic chat
    print("\n2. Basic Chat")
    chat_data = {
        "messages": [
            {
                "role": "user",
                "parts": [{"type": "text", "text": "Hello! How are you?"}]
            }
        ]
    }
    
    try:
        response = requests.post(f"{API_BASE}/chat", json=chat_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Basic chat working")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: RAG chat
    print("\n3. RAG Chat")
    rag_data = {
        "messages": [
            {
                "role": "user",
                "parts": [{"type": "text", "text": "What was our Q3 2024 profit?"}]
            }
        ],
        "getContext": True
    }
    
    try:
        response = requests.post(f"{API_BASE}/chat", json=rag_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ RAG chat working")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Add context
    print("\n4. Add Context")
    context_data = {
        "text": "Q3 2024 Financial Report: Revenue $2.4M, Profit $600K, 15% growth YoY.",
        "metadata": {
            "category": "financial",
            "source": "test-script"
        }
    }
    
    try:
        response = requests.post(f"{API_BASE}/context/add", json=context_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            context_id = response.json()["id"]
            print(f"   ✅ Context added: {context_id}")
            
            # Test 5: Search context
            print("\n5. Search Context")
            search_data = {
                "query": "Q3 2024 financial",
                "limit": 3,
                "threshold": 0.3
            }
            
            response = requests.post(f"{API_BASE}/context/search", json=search_data)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                count = response.json()["count"]
                print(f"   ✅ Found {count} contexts")
            else:
                print(f"   ❌ Error: {response.text}")
            
            # Test 6: Remove context
            print("\n6. Remove Context")
            remove_data = {"id": context_id}
            
            response = requests.delete(f"{API_BASE}/context/remove", json=remove_data)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Context removed")
            else:
                print(f"   ❌ Error: {response.text}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 7: Embeddings
    print("\n7. Generate Embeddings")
    embedding_data = {
        "texts": ["Q3 2024 Financial Report", "Customer Analysis"]
    }
    
    try:
        response = requests.post(f"{API_BASE}/embedding", json=embedding_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            count = response.json()["count"]
            print(f"   ✅ Generated {count} embeddings")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n🎉 Test completed!")

if __name__ == "__main__":
    test_endpoints()
