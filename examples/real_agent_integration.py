#!/usr/bin/env python3
"""
Real Agent Integration Example

This example demonstrates how to integrate a real AI agent with the EnableAI SDK.
The agent uses actual AI providers (OpenAI/Claude) and submits feedback to EnableAI
for evaluation and monitoring.

This is an advanced example showing real-world usage of the SDK.

Requirements:
    pip install requests openai anthropic
    pip install enable_ai_sdk
"""

import os
import time
from typing import Dict, Any, Optional
from datetime import datetime

# Import the SDK
from enable_ai_sdk import EnableAIClient

# Import AI libraries
try:
    import openai
    from anthropic import Anthropic
except ImportError:
    print("❌ Error: AI libraries not found. Please install them:")
    print("   pip install openai anthropic")
    exit(1)


class RealAgent:
    """A real AI agent that integrates with EnableAI for feedback and monitoring"""
    
    def __init__(self, 
                 enable_ai_client: EnableAIClient,
                 agent_id: str,
                 system_prompt: str,
                 openai_api_key: Optional[str] = None,
                 anthropic_api_key: Optional[str] = None):
        """
        Initialize the real agent
        
        Args:
            enable_ai_client: EnableAI client for feedback submission
            agent_id: The agent ID from EnableAI
            system_prompt: System prompt for the agent
            openai_api_key: OpenAI API key (optional)
            anthropic_api_key: Anthropic API key (optional)
        """
        self.enable_ai_client = enable_ai_client
        self.agent_id = agent_id
        self.system_prompt = system_prompt
        
        # Initialize AI clients
        self.openai_client = None
        self.anthropic_client = None
        
        if openai_api_key:
            openai.api_key = openai_api_key
            self.openai_client = openai
            
        if anthropic_api_key:
            self.anthropic_client = Anthropic(api_key=anthropic_api_key)
    
    def generate_response(self, query: str) -> str:
        """Generate a response using the configured AI provider"""
        try:
            if self.anthropic_client:
                # Use Anthropic Claude
                response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=[
                        {"role": "user", "content": f"{self.system_prompt}\n\nUser: {query}"}
                    ]
                )
                return str(response.content[0])
                
            elif self.openai_client:
                # Use OpenAI GPT
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": query}
                    ],
                    max_tokens=1000
                )
                content = response.choices[0].message.content
                return content if content is not None else "I apologize, but I couldn't generate a response."
                
            else:
                # Fallback to mock response
                return self._generate_mock_response(query)
                
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return self._generate_mock_response(query)
    
    def _generate_mock_response(self, query: str) -> str:
        """Generate a mock response when no AI provider is configured"""
        query_lower = query.lower()
        
        if "return" in query_lower or "refund" in query_lower:
            return "Our return policy allows returns within 30 days of purchase with original receipt."
        elif "password" in query_lower or "reset" in query_lower:
            return "You can reset your password by clicking the 'Forgot Password' link on the login page."
        elif "business hours" in query_lower or "hours" in query_lower:
            return "Our customer service is available Monday through Friday, 9 AM to 6 PM EST."
        elif "support" in query_lower or "help" in query_lower:
            return "Yes, we offer 24/7 technical support via phone, email, and live chat."
        else:
            return "Thank you for contacting us. I'd be happy to help you with your inquiry."
    
    def process_query_with_feedback(self, query: str) -> Dict[str, Any]:
        """
        Process a query and submit feedback to EnableAI
        
        Args:
            query: User query
            
        Returns:
            Dictionary with response and feedback data
        """
        # Generate response
        response = self.generate_response(query)
        
        # Submit feedback to EnableAI
        try:
            feedback = self.enable_ai_client.analytics.submit_feedback(
                prompt=query,
                response=response,
                tool="CustomerFeedback",
                use_case="Customer Support",
                agent_id=self.agent_id
            )
            
            return {
                "query": query,
                "response": response,
                "feedback_score": feedback.score,
                "feedback_issue": feedback.issue,
                "feedback_id": feedback.feedback_id
            }
            
        except Exception as e:
            print(f"❌ Feedback submission failed: {e}")
            return {
                "query": query,
                "response": response,
                "feedback_score": None,
                "feedback_issue": None,
                "feedback_id": None
            }


def main():
    """Main example function"""
    print("🚀 Real Agent Integration Example")
    print("=" * 50)
    
    # Configuration - Update these with your actual values
    ENABLE_AI_API_KEY = os.getenv('ENABLE_AI_API_KEY', 'your-enable-ai-api-key')
    ENABLE_AI_BASE_URL = os.getenv('ENABLE_AI_BASE_URL', 'https://your-backend.com')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', None)  # Optional
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', None)  # Optional
    
    # Agent configuration
    AGENT_NAME = "Customer Support Agent"
    AGENT_TYPE = "customer-support"
    AGENT_LLM = "claude-3-5-sonnet-20241022"
    AGENT_SYSTEM_PROMPT = """You are a helpful customer support agent for a technology company.
Provide accurate, helpful information about products, services, and policies.
Always be polite, professional, and concise in your responses."""
    
    # Test queries
    TEST_QUERIES = [
        "What is your return policy?",
        "How do I reset my password?",
        "What are your business hours?",
        "Do you offer technical support?"
    ]
    
    # Initialize EnableAI client
    try:
        client = EnableAIClient(
            api_key=ENABLE_AI_API_KEY,
            base_url=ENABLE_AI_BASE_URL
        )
        print("✅ EnableAI client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize EnableAI client: {e}")
        return
    
    # Register agent
    try:
        agent = client.agents.register(
            name=AGENT_NAME,
            agent_type=AGENT_TYPE,
            llm=AGENT_LLM,
            description="A real AI agent for customer support",
            system_prompt=AGENT_SYSTEM_PROMPT
        )
        print(f"✅ Agent registered: {agent.name} (ID: {agent.id})")
        agent_id = agent.id
    except Exception as e:
        print(f"❌ Agent registration failed: {e}")
        return
    
    # Initialize real agent
    real_agent = RealAgent(
        enable_ai_client=client,
        agent_id=agent_id,
        system_prompt=AGENT_SYSTEM_PROMPT,
        openai_api_key=OPENAI_API_KEY,
        anthropic_api_key=ANTHROPIC_API_KEY
    )
    
    print(f"✅ Real agent initialized")
    print(f"   Using OpenAI: {real_agent.openai_client is not None}")
    print(f"   Using Anthropic: {real_agent.anthropic_client is not None}")
    
    # Process test queries
    print("\n🤖 Processing test queries...")
    results = []
    
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\n--- Query {i}: {query} ---")
        result = real_agent.process_query_with_feedback(query)
        results.append(result)
        
        print(f"Response: {result['response']}")
        print(f"Feedback Score: {result['feedback_score']}")
        if result['feedback_issue'] and result['feedback_issue'] != "None":
            print(f"Issue: {result['feedback_issue']}")
        
        time.sleep(1)  # Small delay between queries
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Summary")
    print("=" * 50)
    
    successful_feedback = [r for r in results if r['feedback_score'] is not None]
    if successful_feedback:
        avg_score = sum(r['feedback_score'] for r in successful_feedback) / len(successful_feedback)
        print(f"Average feedback score: {avg_score:.1f}")
        print(f"Successful feedback submissions: {len(successful_feedback)}/{len(results)}")
    
    # Get agent analytics
    try:
        insights = client.analytics.get_agent_insights(agent_id)
        print(f"\nAgent Analytics:")
        print(f"  Score Trend: {insights.score_trend}")
        print(f"  Average Score: {insights.average_score}")
        print(f"  Feedback Count: {insights.feedback_count}")
    except Exception as e:
        print(f"❌ Analytics failed: {e}")
    
    print("\n🎉 Real agent integration example completed!")


if __name__ == "__main__":
    main() 