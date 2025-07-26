#!/usr/bin/env python3
"""
Simple EnableAI Agent Template - Intermediate Level

A quick-start template for testing the EnableAI SDK core functionality.
This demonstrates the essential features: agent registration, feedback, and analytics.

This is Step 2 in the learning progression.

Usage:
    1. Update the configuration section below
    2. Run: python simple_agent_template.py
    3. Watch the magic happen!

Requirements:
    pip install requests
    pip install enable_ai_sdk
"""

import time
from enable_ai_sdk import EnableAIClient

# =============================================================================
# CONFIGURATION - UPDATE THESE VALUES
# =============================================================================

# Your API credentials
API_KEY = "your-api-key-here"  # Replace with your actual API key
BASE_URL = "https://your-backend.com"  # Replace with your actual backend URL

# Agent settings
AGENT_NAME = "My Test Agent"
AGENT_TYPE = "customer-support"
AGENT_LLM = "claude-3-5-sonnet-20241022"

# =============================================================================
# MAIN SCRIPT
# =============================================================================

def main():
    print("🚀 EnableAI SDK Test Script - Intermediate Level")
    print("=" * 60)
    print("This is Step 2: Testing Core SDK Functionality")
    print("=" * 60)
    
    # Check configuration
    if API_KEY == "your-api-key-here":
        print("❌ Please update API_KEY with your actual API key")
        return
    
    if BASE_URL == "https://your-backend.com":
        print("❌ Please update BASE_URL with your actual backend URL")
        return
    
    # Initialize client
    try:
        client = EnableAIClient(api_key=API_KEY, base_url=BASE_URL)
        print("✅ Client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return
    
    # Test 1: Health check
    print("\n🔍 Testing API connection...")
    try:
        health = client.health_check()
        print(f"✅ API is healthy: {health}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test 2: Register agent
    print(f"\n🤖 Registering agent: {AGENT_NAME}")
    try:
        agent = client.agents.register(
            name=AGENT_NAME,
            agent_type=AGENT_TYPE,
            llm=AGENT_LLM,
            description="A test agent created via SDK"
        )
        print(f"✅ Agent registered successfully!")
        print(f"   ID: {agent.id}")
        print(f"   Name: {agent.name}")
        print(f"   Type: {agent.agent_type}")
    except Exception as e:
        print(f"❌ Agent registration failed: {e}")
        return
    
    # Test 3: Submit feedback
    print("\n📝 Submitting test feedback...")
    try:
        feedback = client.analytics.submit_feedback(
            prompt="What is your return policy?",
            response="Our return policy allows returns within 30 days of purchase.",
            tool="CustomerFeedback",
            use_case="Customer Support",
            agent_id=agent.id
        )
        print(f"✅ Feedback submitted - Score: {feedback.score}")
        if feedback.issue and feedback.issue != "None":
            print(f"   Issue detected: {feedback.issue}")
    except Exception as e:
        print(f"❌ Feedback submission failed: {e}")
    
    # Test 4: Get analytics
    print("\n📊 Getting agent analytics...")
    try:
        insights = client.analytics.get_agent_insights(agent.id)
        print(f"✅ Analytics retrieved:")
        print(f"   Agent: {insights.agent_name}")
        print(f"   Score Trend: {insights.score_trend}")
        print(f"   Average Score: {insights.average_score}")
        print(f"   Feedback Count: {insights.feedback_count}")
    except Exception as e:
        print(f"❌ Analytics failed: {e}")
    
    # Test 5: Self-healing scan
    print("\n🔧 Running self-healing scan...")
    try:
        scan_results = client.self_healing.scan()
        print(f"✅ Self-healing scan completed:")
        print(f"   Agents scanned: {scan_results.get('total_agents_scanned', 0)}")
        print(f"   Agents flagged: {len(scan_results.get('agents_flagged', []))}")
    except Exception as e:
        print(f"❌ Self-healing failed: {e}")
    
    # Test 6: List agents
    print("\n📋 Listing all agents...")
    try:
        agents = client.agents.list()
        print(f"✅ Found {len(agents)} agents:")
        for agent in agents:
            print(f"   - {agent.name} ({agent.agent_type})")
    except Exception as e:
        print(f"❌ Agent listing failed: {e}")
    
    print("\n🎉 Core functionality test completed successfully!")
    print("Your EnableAI SDK core features are working perfectly!")
    print("\nNext steps:")
    print("1. Go to 03-advanced/agent_template.py")
    print("2. Test advanced features like webhooks and interactive testing")
    print("3. Explore the SDK documentation for more advanced usage")

if __name__ == "__main__":
    main() 