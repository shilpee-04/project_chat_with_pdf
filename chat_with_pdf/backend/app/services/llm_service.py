import os
from typing import List, Dict, Any
import openai
from groq import Groq

class LLMService:
    def __init__(self, provider: str = "groq"):
        self.provider = provider
        if provider == "groq":
            self.client = Groq(api_key="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")
            self.model = "llama3-8b-8192"
        else:
            raise ValueError("Only Groq provider is implemented")
    
    def generate_response(self, question: str, context: str, chat_history: List[Dict] = None) -> str:
        """Generate response using LLM with context"""
        
        # Create system prompt
        system_prompt = f"""You are a helpful AI assistant that answers questions based on provided document context.
        
Rules:
1. Answer based ONLY on the provided context
2. Include page numbers in citations like [Page X]
3. If the context doesn't contain relevant information, say "I cannot find relevant information in the provided documents"
4. Be concise but thorough

Context from documents:
{context}
"""
        
        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add chat history if provided
        if chat_history:
            messages.extend(chat_history)
        
        # Add current question
        messages.append({"role": "user", "content": question})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM generation error: {e}")
            return "Sorry, I encountered an error generating a response."
