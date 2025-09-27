#!/usr/bin/env python3

"""
📚 Knowledge Base Example

Example script showing how to populate and search a knowledge base.
Run with: python examples/knowledge_base.py
"""

import requests
import json

# Configuration
API_BASE = "http://localhost:3000/api"

# Sample knowledge base data
SAMPLE_DATA = [
    {
        "text": "Company Overview: TechCorp is a leading AI solutions provider founded in 2020. We specialize in enterprise AI implementations and machine learning consulting.",
        "metadata": {
            "category": "company",
            "source": "about-page",
            "tags": ["company", "AI", "enterprise"]
        }
    },
    {
        "text": "Q3 2024 Financial Results: Revenue $2.4M (+15% YoY), Operating Expenses $1.8M (+29% YoY), Net Profit $600K (-14% YoY).",
        "metadata": {
            "category": "financial",
            "source": "quarterly-report",
            "tags": ["Q3-2024", "revenue", "profit"]
        }
    },
    {
        "text": "Product Portfolio: AI Analytics Platform, ML Model Builder, AI Chat Assistant, Predictive Analytics Suite. Total active users: 50,000+ across 200+ enterprises.",
        "metadata": {
            "category": "products",
            "source": "product-catalog",
            "tags": ["products", "AI", "platform", "users"]
        }
    },
    {
        "text": "Team Structure: Engineering Team (25), Sales Team (8), Operations Team (7). Leadership: CEO, CTO, VP Sales, VP Engineering.",
        "metadata": {
            "category": "hr",
            "source": "org-chart",
            "tags": ["team", "employees", "leadership"]
        }
    }
]

def add_context(text, metadata=None):
    """Add context to the knowledge base."""
    if metadata is None:
        metadata = {}
    
    data = {"text": text, "metadata": metadata}
    
    try:
        response = requests.post(f"{API_BASE}/context/add", json=data)
        if response.status_code == 200:
            return response.json()["id"]
        else:
            print(f"❌ Error adding context: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def search_context(query, limit=5, threshold=0.3):
    """Search the knowledge base."""
    data = {
        "query": query,
        "limit": limit,
        "threshold": threshold
    }
    
    try:
        response = requests.post(f"{API_BASE}/context/search", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error searching: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def remove_context(context_id):
    """Remove context from the knowledge base."""
    data = {"id": context_id}
    
    try:
        response = requests.delete(f"{API_BASE}/context/remove", json=data)
        if response.status_code == 200:
            return True
        else:
            print(f"❌ Error removing context: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def populate_knowledge_base():
    """Populate the knowledge base with sample data."""
    print("📚 Populating Knowledge Base")
    print("===========================")
    
    added_ids = []
    
    for i, item in enumerate(SAMPLE_DATA, 1):
        print(f"Adding item {i}/{len(SAMPLE_DATA)}: {item['metadata']['category']}")
        
        context_id = add_context(item["text"], item["metadata"])
        if context_id:
            added_ids.append(context_id)
            print(f"  ✅ Added: {context_id}")
        else:
            print(f"  ❌ Failed to add")
    
    print(f"\n📊 Summary: Added {len(added_ids)}/{len(SAMPLE_DATA)} items")
    return added_ids

def test_searches():
    """Test various search queries."""
    print("\n🔍 Testing Search Queries")
    print("========================")
    
    test_queries = [
        "financial results Q3 2024",
        "company overview AI solutions",
        "product portfolio users",
        "team structure employees"
    ]
    
    for query in test_queries:
        print(f"\nSearching: '{query}'")
        results = search_context(query, limit=3, threshold=0.3)
        
        if results:
            count = results["count"]
            print(f"  Found {count} results:")
            
            for i, result in enumerate(results["results"], 1):
                print(f"    {i}. Score: {result['score']:.3f}")
                print(f"       Text: {result['text'][:80]}...")
                print(f"       Category: {result['metadata'].get('category', 'N/A')}")
        else:
            print("  No results found")

def cleanup_knowledge_base(added_ids):
    """Clean up the knowledge base."""
    print(f"\n🧹 Cleaning up {len(added_ids)} items...")
    
    removed_count = 0
    for context_id in added_ids:
        if remove_context(context_id):
            removed_count += 1
            print(f"  ✅ Removed: {context_id}")
        else:
            print(f"  ❌ Failed to remove: {context_id}")
    
    print(f"📊 Cleanup complete: Removed {removed_count}/{len(added_ids)} items")

def main():
    """Run the knowledge base example."""
    print("📚 Knowledge Base Example")
    print("=========================")
    
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
    
    # Populate knowledge base
    added_ids = populate_knowledge_base()
    
    if added_ids:
        # Test searches
        test_searches()
        
        # Cleanup
        cleanup_knowledge_base(added_ids)
    
    print("\n🎉 Knowledge base example completed!")

if __name__ == "__main__":
    main()
