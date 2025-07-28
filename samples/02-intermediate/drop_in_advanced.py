#!/usr/bin/env python3
"""
EnableAI Drop-in SDK Integration - Intermediate Level

This sample demonstrates advanced drop-in integration with real AI models,
configuration options, and production-ready features.

Usage:
    python drop_in_advanced.py
"""

import os
import time
import json
from enable_ai_sdk.agent_monitor import create_monitored_agent, AgentMonitor

def main():
    """Main function demonstrating advanced drop-in integration"""
    
    print("🚀 EnableAI Drop-in SDK Integration - Intermediate Level")
    print("=" * 65)
    print("Advanced drop-in integration with real AI models and configuration")
    print("=" * 65)
    print()
    
    # Configuration
    api_key = os.getenv('ENABLE_AI_API_KEY', 'your-api-key-here')
    agent_id = os.getenv('ENABLE_AI_AGENT_ID', 'your-agent-id-here')
    base_url = os.getenv('ENABLE_AI_BASE_URL', 'https://api.weenable.ai')
    
    print(f"🔧 Configuration:")
    print(f"   API Key: {api_key[:20]}..." if len(api_key) > 20 else f"   API Key: {api_key}")
    print(f"   Agent ID: {agent_id}")
    print(f"   Base URL: {base_url}")
    print()
    
    # Method 1: Simple drop-in with configuration
    print("📝 Method 1: Simple drop-in with advanced configuration")
    print("-" * 60)
    
    def customer_support_ai(prompt: str) -> str:
        """Simulated customer support AI model"""
        # This could be OpenAI, Claude, or any AI model
        responses = {
            "return policy": "Our return policy allows returns within 30 days of purchase with original receipt.",
            "password reset": "To reset your password, go to our website and click 'Forgot Password'.",
            "business hours": "We're open Monday-Friday 9AM-6PM and Saturday 10AM-4PM.",
            "shipping": "Standard shipping takes 3-5 business days. Express shipping is available.",
            "warranty": "All products come with a 1-year manufacturer warranty."
        }
        
        prompt_lower = prompt.lower()
        for key, response in responses.items():
            if key in prompt_lower:
                return response
        
        return "I'm sorry, I don't have information about that. Please contact our support team."
    
    try:
        # Create monitored agent with advanced configuration
        monitored_agent = create_monitored_agent(
            agent_id=agent_id,
            api_key=api_key,
            ai_model_func=customer_support_ai,
            base_url=base_url
        )
        print("✅ Advanced monitored agent created successfully!")
        print("   - Automatic monitoring enabled")
        print("   - Self-healing with two-step process enabled")
        print("   - Performance tracking enabled")
        print("   - Error prevention and validation enabled")
        print()
    except Exception as e:
        print(f"❌ Error creating monitored agent: {e}")
        return
    
    # Test the monitored agent
    print("🧪 Testing the monitored agent")
    print("-" * 60)
    
    test_cases = [
        "What is your return policy?",
        "How do I reset my password?",
        "What are your business hours?",
        "How long does shipping take?",
        "What warranty do you offer?"
    ]
    
    for i, prompt in enumerate(test_cases, 1):
        print(f"📤 Test {i}: '{prompt}'")
        
        try:
            start_time = time.time()
            response = monitored_agent.generate_response(prompt)
            end_time = time.time()
            
            print(f"📥 Response: '{response}'")
            print(f"⏱️  Response time: {end_time - start_time:.2f}s")
            print("✅ Automatically monitored and evaluated!")
            print("   - Performance reported for evaluation")
            print("   - Quality scored by Claude")
            print("   - Self-healing scan triggered if needed")
            print("   - Agent flagged for healing if performance is poor")
            print("   - Prompt improvements applied automatically")
            print()
            
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print()
    
    # Method 2: Custom agent class for more control
    print("📝 Method 2: Custom agent class for advanced control")
    print("-" * 60)
    
    class MonitoredCustomerSupportAgent(AgentMonitor):
        """Custom monitored agent with advanced features"""
        
        def __init__(self, agent_id: str, api_key: str, **kwargs):
            super().__init__(agent_id, api_key, **kwargs)
            self.conversation_history = []
            self.response_count = 0
        
        def _call_ai_model(self, prompt: str, **kwargs) -> str:
            """Custom AI model integration"""
            # This is where you'd integrate with OpenAI, Claude, etc.
            # For this example, we'll use the same simulated model
            
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": prompt})
            
            # Simulate AI model call
            response = customer_support_ai(prompt)
            
            # Add response to history
            self.conversation_history.append({"role": "assistant", "content": response})
            self.response_count += 1
            
            return response
        
        def get_stats(self):
            """Get custom statistics"""
            return {
                "total_responses": self.response_count,
                "conversation_length": len(self.conversation_history),
                "last_response_time": getattr(self, '_last_response_time', None)
            }
    
    try:
        # Create custom monitored agent
        custom_agent = MonitoredCustomerSupportAgent(
            agent_id=agent_id,
            api_key=api_key,
            base_url=base_url
        )
        print("✅ Custom monitored agent created successfully!")
        print("   - Custom AI model integration")
        print("   - Conversation history tracking")
        print("   - Custom statistics")
        print()
    except Exception as e:
        print(f"❌ Error creating custom agent: {e}")
        return
    
    # Test the custom agent
    print("🧪 Testing the custom agent")
    print("-" * 60)
    
    for i, prompt in enumerate(test_cases[:3], 1):
        print(f"📤 Test {i}: '{prompt}'")
        
        try:
            response = custom_agent.generate_response(prompt)
            print(f"📥 Response: '{response}'")
            
            # Get custom stats
            stats = custom_agent.get_stats()
            print(f"📊 Stats: {stats['total_responses']} responses, {stats['conversation_length']} messages")
            print("✅ Automatically monitored with custom features!")
            print()
            
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print()
    
    # Method 3: AWS Lambda integration
    print("📝 Method 3: AWS Lambda integration example")
    print("-" * 60)
    
    lambda_code = '''
import json
from enable_ai_sdk.agent_monitor import create_monitored_agent

# Your AI model function
def my_ai_model(prompt: str) -> str:
    # Your AI model integration here
    return "Response from your AI model"

# Create monitored agent (outside handler for reuse)
agent = create_monitored_agent(
    agent_id=os.getenv('AGENT_ID'),
    api_key=os.getenv('ENABLE_AI_API_KEY'),
    ai_model_func=my_ai_model,
    base_url=os.getenv('ENABLE_AI_BASE_URL')
)

def lambda_handler(event, context):
    user_input = event['body']['message']
    response = agent.generate_response(user_input)  # Automatically monitored!
    return {
        'statusCode': 200,
        'body': json.dumps({'response': response})
    }
'''
    
    print("🔧 AWS Lambda Integration:")
    print(lambda_code)
    print("✅ Automatically monitored in serverless environment!")
    print()
    
    # Method 4: Production configuration
    print("📝 Method 4: Production configuration")
    print("-" * 60)
    
    production_config = {
        "auto_healing": True,
        "report_async": True,
        "timeout": 30,
        "retry_count": 3,
        "base_url": "https://api.weenable.ai",
        "log_level": "INFO",
        "rate_limit": 100,  # requests per minute
        "batch_size": 10,    # batch reporting
        "health_check_interval": 300  # seconds
    }
    
    print("🔧 Production Configuration:")
    for key, value in production_config.items():
        print(f"   {key}: {value}")
    print()
    
    # What gets tracked automatically
    print("🔍 What gets tracked automatically")
    print("-" * 60)
    print("Performance Metrics:")
    print("   • Quality Score (1-100 rating from Claude)")
    print("   • Response Time (how long your agent takes)")
    print("   • Issue Categories (hallucination, tone, format, etc.)")
    print("   • Usage Patterns (when and how your agent is used)")
    print()
    print("Self-Healing Triggers:")
    print("   • Poor Performance (average score < 75)")
    print("   • Critical Issues (average score < 60)")
    print("   • Declining Trends (performance getting worse)")
    print("   • Specific Issues (hallucination, tone problems, etc.)")
    print()
    print("Automatic Actions:")
    print("   • Prompt Improvements (AI-generated better prompts)")
    print("   • Health Monitoring (real-time status checking)")
    print("   • Performance Reporting (every interaction evaluated)")
    print("   • Insight Generation (AI recommendations)")
    print()
    
    # Benefits summary
    print("🎯 Key Benefits")
    print("-" * 60)
    print("For Agent Developers:")
    print("   • Drop-in integration - just import and wrap")
    print("   • Automatic monitoring - every interaction evaluated")
    print("   • Self-healing - automatic improvements when needed")
    print("   • Real-time insights - performance analytics")
    print()
    print("For Agent Operators:")
    print("   • Zero manual work - everything is automatic")
    print("   • Proactive alerts - notified when agents need attention")
    print("   • Continuous improvement - agents get better over time")
    print("   • Comprehensive analytics - detailed performance tracking")
    print()
    
    # Next steps
    print("🚀 Next Steps")
    print("-" * 60)
    print("1. Replace the simulated AI model with your actual AI model")
    print("2. Configure production settings (timeout, retries, etc.)")
    print("3. Set up environment variables for API keys")
    print("4. Deploy to production")
    print("5. Monitor performance in the EnableAI console")
    print()
    print("📚 For advanced features, see:")
    print("   • 03-advanced/agent_template.py - All SDK features")
    print("   • 03-advanced/real_agent_template.py - Real AI model integration")
    print()
    print("🎉 Your agent is now production-ready with automatic monitoring!")

if __name__ == "__main__":
    main() 