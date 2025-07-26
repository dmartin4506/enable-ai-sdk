#!/usr/bin/env python3
"""
Basic usage example for the EnableAI SDK
"""

from enable_ai_sdk import EnableAIClient
import os
import time


def main():
    """Basic example demonstrating SDK usage"""
    
    # Initialize client
    # In production, use environment variables for API keys
    api_key = os.getenv('ENABLE_AI_API_KEY', 'your-api-key-here')
    base_url = os.getenv('ENABLE_AI_BASE_URL', 'https://api.enable.ai')
    
    client = EnableAIClient(api_key=api_key, base_url=base_url)
    
    print("🚀 EnableAI SDK Basic Example")
    print("=" * 40)
    
    try:
        # Check API health
        health = client.health_check()
        print(f"✅ API Health: {health}")
        
        # Register an agent
        print("\n📝 Registering agent...")
        agent = client.agents.register(
            name="Customer Support Agent",
            agent_type="customer-support",
            llm="claude-3-5-sonnet-20241022",
            description="A helpful customer support agent"
        )
        
        print(f"✅ Registered agent: {agent.name} (ID: {agent.id})")
        
        # Submit some feedback
        print("\n📊 Submitting feedback...")
        feedback = client.analytics.submit_feedback(
            prompt="What is your return policy?",
            response="Our return policy allows returns within 30 days of purchase.",
            tool="CustomerFeedback",
            use_case="Customer Support",
            agent_id=agent.id
        )
        
        print(f"✅ Feedback submitted - Score: {feedback.score}")
        print(f"   Issue: {feedback.issue}")
        
        # Wait a moment for processing
        print("\n⏳ Waiting for processing...")
        time.sleep(2)
        
        # Get agent insights
        print("\n📈 Getting agent insights...")
        insights = client.analytics.get_agent_insights(agent.id)
        
        print(f"✅ Agent insights:")
        print(f"   - Agent: {insights.agent_name}")
        print(f"   - Trend: {insights.score_trend}")
        print(f"   - Average Score: {insights.average_score}")
        print(f"   - Recent Issues: {len(insights.recent_issues)}")
        print(f"   - Suggested Actions: {len(insights.suggested_actions)}")
        
        # Create a webhook for notifications
        print("\n🔗 Creating webhook...")
        webhook = client.webhooks.create(
            name="Agent Monitoring",
            url="https://my-endpoint.com/webhook",
            events=["agent_self_healing_triggered", "feedback_submitted"]
        )
        
        print(f"✅ Created webhook: {webhook['name']}")
        
        # Run self-healing scan
        print("\n🔍 Running self-healing scan...")
        scan_results = client.self_healing.scan()
        
        print(f"✅ Self-healing scan completed:")
        print(f"   - Agents scanned: {scan_results.get('total_agents_scanned', 0)}")
        print(f"   - Agents flagged: {len(scan_results.get('agents_flagged', []))}")
        
        # List all agents
        print("\n📋 Listing all agents...")
        agents = client.agents.list()
        
        print(f"✅ Found {len(agents)} agents:")
        for agent in agents:
            print(f"   - {agent.name} ({agent.agent_type}) - ID: {agent.id}")
        
        print("\n🎉 Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure you have:")
        print("   - Valid API key set in ENABLE_AI_API_KEY environment variable")
        print("   - Correct base URL set in ENABLE_AI_BASE_URL environment variable")
        print("   - Network connectivity to the API")


if __name__ == "__main__":
    main() 