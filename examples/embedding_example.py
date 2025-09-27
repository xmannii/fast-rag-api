#!/usr/bin/env python3

"""
🧠 Embedding Example

Example script showing how to generate and work with embeddings.
Run with: python examples/embedding_example.py
"""

import requests
import json
import math

# Configuration
API_BASE = "http://localhost:3000/api"

def generate_embeddings(texts):
    """Generate embeddings for a list of texts."""
    data = {"texts": texts}
    
    try:
        response = requests.post(f"{API_BASE}/embedding", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error generating embeddings: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def get_available_models():
    """Get available embedding models."""
    try:
        response = requests.get(f"{API_BASE}/embedding/models")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error getting models: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    # Calculate dot product
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    
    # Calculate magnitudes
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(a * a for a in vec2))
    
    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    
    return dot_product / (magnitude1 * magnitude2)

def main():
    """Run the embedding example."""
    print("🧠 Embedding Example")
    print("====================")
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:3000/")
        if response.status_code != 200:
            print("❌ Server is not running!")
            print("💡 Start the server with: bun run dev")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Start the server with: bun run dev")
        return
    
    print("✅ Server is running")
    
    # Get available models
    print("\n📋 Available Embedding Models:")
    models = get_available_models()
    if models:
        print(f"  Default: {models['defaultModel']}")
        print(f"  Available: {', '.join(models['models'])}")
    else:
        print("  ❌ Could not retrieve models")
        return
    
    # Sample texts for embedding
    texts = [
        "Q3 2024 Financial Report: Revenue increased by 15% to $2.4M",
        "Customer Analysis: Top customers include Acme Corp and TechStart Inc",
        "Product Portfolio: AI Analytics Platform and ML Model Builder",
        "Team Structure: Engineering Team (25), Sales Team (8), Operations Team (7)",
        "Technology Stack: Node.js, Python, PostgreSQL, React, TypeScript"
    ]
    
    print(f"\n🔢 Generating embeddings for {len(texts)} texts...")
    
    # Generate embeddings
    result = generate_embeddings(texts)
    if not result:
        return
    
    embeddings = result["embeddings"]
    model = result["model"]
    count = result["count"]
    
    print(f"✅ Generated {count} embeddings using {model}")
    print(f"📏 Embedding dimensions: {len(embeddings[0])}")
    
    # Calculate similarities
    print("\n🔍 Calculating Similarities:")
    print("=" * 50)
    
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            similarity = cosine_similarity(embeddings[i], embeddings[j])
            print(f"Text {i+1} ↔ Text {j+1}: {similarity:.4f}")
            print(f"  '{texts[i][:40]}...'")
            print(f"  '{texts[j][:40]}...'")
            print()
    
    # Find most similar pairs
    print("🏆 Most Similar Pairs:")
    similarities = []
    
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            similarity = cosine_similarity(embeddings[i], embeddings[j])
            similarities.append((similarity, i, j))
    
    # Sort by similarity (highest first)
    similarities.sort(reverse=True)
    
    for similarity, i, j in similarities[:3]:  # Top 3
        print(f"  {similarity:.4f}: Text {i+1} ↔ Text {j+1}")
        print(f"    '{texts[i][:50]}...'")
        print(f"    '{texts[j][:50]}...'")
        print()
    
    print("🎉 Embedding example completed!")

if __name__ == "__main__":
    main()
