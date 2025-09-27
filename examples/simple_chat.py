#!/usr/bin/env python3

"""
💬 Simple Chat Example

Interactive chat example with RAG functionality.
Run with: python examples/simple_chat.py
"""

import requests
import json

# Configuration
API_BASE = "http://localhost:3000/api"

def send_message(message, use_rag=True):
    """Send a message to the chat API."""
    chat_data = {
        "messages": [
            {
                "role": "user",
                "parts": [{"type": "text", "text": message}]
            }
        ],
        "getContext": use_rag
    }
    
    try:
        response = requests.post(f"{API_BASE}/chat", json=chat_data)
        if response.status_code == 200:
            return "✅ Message sent successfully (streaming response)"
        else:
            return f"❌ Error: {response.text}"
    except Exception as e:
        return f"❌ Connection error: {e}"

def main():
    """Run the simple chat example."""
    print("💬 Simple RAG Chat Example")
    print("=========================")
    print("Type 'quit' to exit, 'rag off' to disable RAG, 'rag on' to enable RAG")
    print()
    
    rag_enabled = True
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'rag off':
                rag_enabled = False
                print("🔍 RAG disabled")
                continue
            elif user_input.lower() == 'rag on':
                rag_enabled = True
                print("🔍 RAG enabled")
                continue
            elif not user_input:
                continue
            
            # Send message
            print(f"🤖 AI: {send_message(user_input, rag_enabled)}")
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
