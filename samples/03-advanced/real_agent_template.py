#!/usr/bin/env python3
"""
Real Agent Template - Advanced Level

This sample demonstrates how to create a real AI agent that integrates with the EnableAI SDK.
The agent can actually respond to user queries and submit feedback for evaluation.

This is an enhanced version of the advanced template with real AI capabilities.

Features:
- Real AI agent using OpenAI/Claude API
- Integration with EnableAI SDK for feedback
- Real-time response evaluation
- Agent performance monitoring
- Customizable agent behavior

Requirements:
    pip install requests openai anthropic
    pip install enable_ai_sdk
"""

import os
import time
import json
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime

# Import your SDK
try:
    from enable_ai_sdk import EnableAIClient, EnableAIError, AuthenticationError, ValidationError, RateLimitError
except ImportError:
    print("❌ Error: enable_ai_sdk not found. Please install it first:")
    print("   pip install enable_ai_sdk")
    exit(1)

# Import AI libraries
try:
    import openai
    from anthropic import Anthropic
except ImportError:
    print("❌ Error: AI libraries not found. Please install them:")
    print("   pip install openai anthropic")
    exit(1)

# =============================================================================
# CONFIGURATION - UPDATE THESE VALUES
# =============================================================================

# EnableAI API credentials
ENABLE_AI_API_KEY = "your-enable-ai-api-key-here"
ENABLE_AI_BASE_URL = "https://your-backend.com"

# AI Provider credentials (choose one)
OPENAI_API_KEY = "your-openai-api-key-here"  # Optional
ANTHROPIC_API_KEY = "your-anthropic-api-key-here"  # Optional

# Agent configuration
AGENT_NAME = "Real Customer Support Agent"
AGENT_TYPE = "customer-support"
AGENT_LLM = "claude-3-5-sonnet-20241022"
AGENT_DESCRIPTION = "A real AI agent for customer support with EnableAI integration"

# Agent system prompt
AGENT_SYSTEM_PROMPT = """You are a helpful customer support agent for a technology company called TechCorp.

Your role is to:
1. Provide accurate, helpful information about products and services
2. Help customers with technical issues
3. Process returns and refunds
4. Answer questions about policies and procedures
5. Be polite, professional, and concise

Company Information:
- TechCorp offers software solutions for businesses
- Business hours: Monday-Friday, 9 AM to 6 PM EST
- Return policy: 30 days with original receipt
- Support: 24/7 via phone, email, and live chat
- Payment methods: All major credit cards, PayPal, bank transfers

Always be helpful, accurate, and professional in your responses."""

# Test queries for the agent
TEST_QUERIES = [
    "What is your return policy?",
    "How do I reset my password?",
    "What are your business hours?",
    "Do you offer technical support?",
    "What payment methods do you accept?",
    "I need help with my software installation",
    "Can I get a refund for my purchase?",
    "What's your phone number for support?"
]

# =============================================================================
# REAL AGENT CLASS
# =============================================================================

class RealAgent:
    """A real AI agent that can respond to queries and integrate with EnableAI"""
    
    def __init__(self, 
                 enable_ai_client: EnableAIClient,
                 agent_id: str,
                 system_prompt: str,
                 use_openai: bool = False,
                 use_anthropic: bool = True):
        """
        Initialize the real agent
        
        Args:
            enable_ai_client: EnableAI client for feedback submission
            agent_id: The agent ID from EnableAI
            system_prompt: System prompt for the agent
            use_openai: Whether to use OpenAI API
            use_anthropic: Whether to use Anthropic API
        """
        self.enable_ai_client = enable_ai_client
        self.agent_id = agent_id
        self.system_prompt = system_prompt
        self.use_openai = use_openai
        self.use_anthropic = use_anthropic
        
        # Initialize AI clients
        if use_openai and OPENAI_API_KEY != "your-openai-api-key-here":
            openai.api_key = OPENAI_API_KEY
            self.openai_client = openai
        else:
            self.openai_client = None
            
        if use_anthropic and ANTHROPIC_API_KEY != "your-anthropic-api-key-here":
            self.anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
        else:
            self.anthropic_client = None
    
    def generate_response(self, query: str) -> str:
        """
        Generate a response using the AI provider
        
        Args:
            query: User query
            
        Returns:
            Generated response
        """
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
                # Handle response content
                try:
                    return str(response.content[0])
                except Exception:
                    return "I apologize, but I couldn't generate a response."
                
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
        """Generate a mock response when AI providers are not configured"""
        query_lower = query.lower()
        
        if "return" in query_lower or "refund" in query_lower:
            return "Our return policy allows returns within 30 days of purchase with original receipt. You can initiate a return through your account dashboard or contact our support team."
        elif "password" in query_lower or "reset" in query_lower:
            return "You can reset your password by clicking the 'Forgot Password' link on the login page. You'll receive an email with reset instructions."
        elif "business hours" in query_lower or "hours" in query_lower:
            return "Our customer service is available Monday through Friday, 9 AM to 6 PM EST. For urgent issues, we offer 24/7 support via phone."
        elif "support" in query_lower or "help" in query_lower:
            return "Yes, we offer 24/7 technical support via phone, email, and live chat. You can reach us at 1-800-TECHCORP or support@techcorp.com."
        elif "payment" in query_lower or "pay" in query_lower:
            return "We accept all major credit cards, PayPal, and bank transfers. All payments are processed securely through our payment partners."
        elif "phone" in query_lower or "number" in query_lower:
            return "You can reach our support team at 1-800-TECHCORP (1-800-832-4267) for immediate assistance."
        else:
            return "Thank you for contacting TechCorp support. I'd be happy to help you with your inquiry. Could you please provide more details about your specific question or issue?"
    
    def process_query_with_feedback(self, query: str) -> Dict[str, Any]:
        """
        Process a query and submit feedback to EnableAI
        
        Args:
            query: User query
            
        Returns:
            Dictionary with response and feedback data
        """
        print(f"\n🤖 Processing query: {query}")
        
        # Generate response
        response = self.generate_response(query)
        print(f"📝 Generated response: {response}")
        
        # Submit feedback to EnableAI
        try:
            feedback = self.enable_ai_client.analytics.submit_feedback(
                prompt=query,
                response=response,
                tool="CustomerFeedback",
                use_case="Customer Support",
                agent_id=self.agent_id
            )
            
            print(f"✅ Feedback submitted - Score: {feedback.score}")
            if feedback.issue and feedback.issue != "None":
                print(f"   Issue detected: {feedback.issue}")
            
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

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def print_header(title: str):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_success(message: str):
    """Print a success message"""
    print(f"✅ {message}")

def print_error(message: str):
    """Print an error message"""
    print(f"❌ {message}")

def print_info(message: str):
    """Print an info message"""
    print(f"ℹ️  {message}")

def validate_config():
    """Validate the configuration"""
    print_header("Configuration Validation")
    
    if ENABLE_AI_API_KEY == "your-enable-ai-api-key-here":
        print_error("Please update ENABLE_AI_API_KEY with your actual API key")
        return False
    
    if ENABLE_AI_BASE_URL == "https://your-backend.com":
        print_error("Please update ENABLE_AI_BASE_URL with your actual backend URL")
        return False
    
    # Check AI provider configuration
    ai_providers_configured = 0
    if OPENAI_API_KEY != "your-openai-api-key-here":
        ai_providers_configured += 1
        print_success("OpenAI API key configured")
    
    if ANTHROPIC_API_KEY != "your-anthropic-api-key-here":
        ai_providers_configured += 1
        print_success("Anthropic API key configured")
    
    if ai_providers_configured == 0:
        print_info("No AI providers configured - will use mock responses")
    else:
        print_success(f"{ai_providers_configured} AI provider(s) configured")
    
    print_success("Configuration looks good!")
    return True

# =============================================================================
# MAIN FUNCTIONS
# =============================================================================

def test_real_agent_interaction(client: EnableAIClient, agent_id: str):
    """Test real agent interaction with EnableAI feedback"""
    print_header("Testing Real Agent Interaction")
    
    # Initialize the real agent
    agent = RealAgent(
        enable_ai_client=client,
        agent_id=agent_id,
        system_prompt=AGENT_SYSTEM_PROMPT,
        use_openai=OPENAI_API_KEY != "your-openai-api-key-here",
        use_anthropic=ANTHROPIC_API_KEY != "your-anthropic-api-key-here"
    )
    
    print_success("Real agent initialized")
    print(f"   Agent ID: {agent_id}")
    print(f"   Using OpenAI: {agent.use_openai}")
    print(f"   Using Anthropic: {agent.use_anthropic}")
    
    # Process test queries
    results = []
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\n--- Query {i}/{len(TEST_QUERIES)} ---")
        result = agent.process_query_with_feedback(query)
        results.append(result)
        
        # Small delay between queries
        time.sleep(1)
    
    # Summary
    print_header("Interaction Summary")
    successful_feedback = [r for r in results if r['feedback_score'] is not None]
    
    if successful_feedback:
        avg_score = sum(r['feedback_score'] for r in successful_feedback) / len(successful_feedback)
        print_success(f"Average feedback score: {avg_score:.1f}")
        print_success(f"Successful feedback submissions: {len(successful_feedback)}/{len(results)}")
        
        # Show issues if any
        issues = [r for r in successful_feedback if r['feedback_issue'] and r['feedback_issue'] != "None"]
        if issues:
            print_info(f"Detected issues: {len(issues)}")
            for issue in issues:
                print(f"   - {issue['feedback_issue']}")
    
    return results

def test_agent_analytics(client: EnableAIClient, agent_id: str):
    """Test agent analytics after real interactions"""
    print_header("Testing Agent Analytics")
    
    try:
        insights = client.analytics.get_agent_insights(agent_id)
        
        print_success("Agent insights retrieved:")
        print(f"   Agent: {insights.agent_name}")
        print(f"   Score Trend: {insights.score_trend}")
        print(f"   Average Score: {insights.average_score}")
        print(f"   Feedback Count: {insights.feedback_count}")
        print(f"   Recent Issues: {len(insights.recent_issues)}")
        print(f"   Suggested Actions: {len(insights.suggested_actions)}")
        
        if insights.recent_issues:
            print("\n   Recent Issues:")
            for issue in insights.recent_issues:
                print(f"     - {issue.get('issue', 'Unknown')}: {issue.get('count', 0)} occurrences")
        
        if insights.suggested_actions:
            print("\n   Suggested Actions:")
            for action in insights.suggested_actions:
                print(f"     - {action}")
        
    except Exception as e:
        print_error(f"Analytics failed: {e}")

def interactive_agent_mode(client: EnableAIClient, agent_id: str):
    """Interactive mode for testing the real agent"""
    print_header("Interactive Agent Mode")
    print("You can now chat with the real agent! Type 'quit' to exit.")
    
    agent = RealAgent(
        enable_ai_client=client,
        agent_id=agent_id,
        system_prompt=AGENT_SYSTEM_PROMPT,
        use_openai=OPENAI_API_KEY != "your-openai-api-key-here",
        use_anthropic=ANTHROPIC_API_KEY != "your-anthropic-api-key-here"
    )
    
    while True:
        try:
            query = input("\n🤖 You: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query:
                continue
            
            result = agent.process_query_with_feedback(query)
            
            print(f"📊 Feedback Score: {result['feedback_score']}")
            if result['feedback_issue'] and result['feedback_issue'] != "None":
                print(f"⚠️  Issue: {result['feedback_issue']}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function"""
    print_header("Real Agent Template - Advanced Level")
    print("This demonstrates a real AI agent with EnableAI integration")
    print("Make sure you've updated the configuration section above!")
    
    # Validate configuration
    if not validate_config():
        print_error("Please fix the configuration issues and try again.")
        return
    
    # Initialize EnableAI client
    try:
        client = EnableAIClient(
            api_key=ENABLE_AI_API_KEY,
            base_url=ENABLE_AI_BASE_URL
        )
        print_success("EnableAI client initialized")
    except Exception as e:
        print_error(f"Failed to initialize EnableAI client: {e}")
        return
    
    # Test connection
    try:
        health = client.health_check()
        print_success(f"EnableAI API is healthy: {health}")
    except Exception as e:
        print_error(f"EnableAI connection failed: {e}")
        return
    
    # Register agent
    try:
        agent = client.agents.register(
            name=AGENT_NAME,
            agent_type=AGENT_TYPE,
            llm=AGENT_LLM,
            description=AGENT_DESCRIPTION,
            system_prompt=AGENT_SYSTEM_PROMPT
        )
        print_success(f"Agent registered: {agent.name} (ID: {agent.id})")
        agent_id = agent.id
    except Exception as e:
        print_error(f"Agent registration failed: {e}")
        return
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Run automated test queries")
    print("2. Interactive chat mode")
    print("3. Both")
    
    choice = input("Select option (1-3): ").strip()
    
    if choice == "1":
        # Run automated tests
        test_real_agent_interaction(client, agent_id)
        test_agent_analytics(client, agent_id)
        
    elif choice == "2":
        # Interactive mode
        interactive_agent_mode(client, agent_id)
        
    elif choice == "3":
        # Both
        test_real_agent_interaction(client, agent_id)
        test_agent_analytics(client, agent_id)
        print("\n" + "="*60)
        interactive_agent_mode(client, agent_id)
        
    else:
        print_error("Invalid choice. Running automated tests...")
        test_real_agent_interaction(client, agent_id)
        test_agent_analytics(client, agent_id)
    
    print_header("Real Agent Test Complete!")
    print_success("Your real agent is working with EnableAI integration!")

if __name__ == "__main__":
    main() 