#!/usr/bin/env python3
"""
EnableAI Drop-in SDK Integration - Beginner Level

This sample demonstrates the simplest way to integrate your AI agent with EnableAI:
Just import and wrap your agent - everything else is automatic!

Usage:
    python drop_in_integration.py
"""

import os
import time
from enable_ai_sdk.agent_monitor import create_monitored_agent

def main():
    """Main function demonstrating drop-in integration"""
    
    print("🚀 EnableAI Drop-in SDK Integration - Beginner Level")
    print("=" * 60)
    print("This is the simplest way to integrate your AI agent!")
    print("Just import and wrap your agent - everything else is automatic!")
    print("=" * 60)
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
    
    # Step 1: Your existing AI model function
    print("📝 Step 1: Define your existing AI model function")
    print("-" * 50)
    
    def your_ai_model(prompt: str) -> str:
        """Your existing AI model - this could be OpenAI, Claude, or any AI model"""
        # This is where your existing AI model logic goes
        # For this example, we'll simulate a simple response
        return f"Response to: {prompt}"
    
    print("✅ Your AI model function defined")
    print("   This could be OpenAI, Claude, or any AI model you're using")
    print()
    
    # Step 2: Create monitored agent (3 lines!)
    print("🚀 Step 2: Create monitored agent (3 lines!)")
    print("-" * 50)
    
    try:
        monitored_agent = create_monitored_agent(
            agent_id=agent_id,
            api_key=api_key,
            ai_model_func=your_ai_model,
            base_url=base_url
        )
        print("✅ Monitored agent created successfully!")
        print("   This wraps your existing AI model with automatic monitoring")
        print()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Please install the SDK: pip install enable-ai-sdk")
        return
    except Exception as e:
        print(f"❌ Error creating monitored agent: {e}")
        print("   Please check your API key and agent ID")
        return
    
    # Step 3: Use it normally - everything is automatic!
    print("🎯 Step 3: Use it normally - everything is automatic!")
    print("-" * 50)
    
    test_prompts = [
        "What is your return policy?",
        "How do I reset my password?",
        "What are your business hours?"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"📤 Test {i}: Sending prompt: '{prompt}'")
        
        try:
            # Use it like any other agent - everything is automatic!
            response = monitored_agent.generate_response(prompt)
            
            print(f"📥 Response: '{response}'")
            print("✅ Interaction automatically monitored!")
            print("   - Performance reported for evaluation")
            print("   - Quality scored by Claude")
            print("   - Self-healing scan triggered if needed")
            print("   - Agent flagged for healing if performance is poor")
            print("   - Prompt improvements applied automatically")
            print()
            
            # Small delay between requests
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error during interaction: {e}")
            print()
    
    # Step 4: What happens automatically
    print("🔍 Step 4: What happens automatically")
    print("-" * 50)
    print("Every time you call generate_response(), the SDK automatically:")
    print("✅ Reports the interaction for performance evaluation")
    print("✅ Gets quality scores from Claude (1-100 rating)")
    print("✅ Tracks response times and usage patterns")
    print("✅ Identifies issues (hallucination, tone, format, etc.)")
    print("✅ Triggers self-healing when performance degrades")
    print("✅ Applies prompt improvements automatically")
    print("✅ Provides real-time analytics and insights")
    print()
    
    # Step 5: Benefits
    print("🎯 Step 5: Key Benefits")
    print("-" * 50)
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
    
    # Step 6: Next steps
    print("🚀 Step 6: Next Steps")
    print("-" * 50)
    print("1. Replace your_ai_model() with your actual AI model")
    print("2. Set up your API key and agent ID")
    print("3. Deploy to production")
    print("4. Monitor performance in the EnableAI console")
    print()
    print("🎉 That's it! Your agent is now automatically monitored!")
    print("   No manual work required - everything happens in the background.")
    print()
    print("📚 For more advanced features, see:")
    print("   • 02-intermediate/simple_agent_template.py - Core functionality")
    print("   • 03-advanced/agent_template.py - Advanced features")
    print("   • 03-advanced/real_agent_template.py - Real AI model integration")

if __name__ == "__main__":
    main() 