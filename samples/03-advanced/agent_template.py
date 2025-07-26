#!/usr/bin/env python3
"""
Comprehensive EnableAI Agent Template - Advanced Level

A comprehensive template for testing the EnableAI SDK end-to-end with advanced features.
This demonstrates all SDK capabilities including webhooks, interactive testing, and detailed analytics.

This is Step 3 in the learning progression.

Usage:
    1. Set your API keys in the configuration section below
    2. Run: python agent_template.py
    3. Follow the interactive prompts to test different features

Requirements:
    pip install requests
    pip install enable_ai_sdk
"""

import os
import time
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Import your SDK
try:
    from enable_ai_sdk import EnableAIClient, EnableAIError, AuthenticationError, ValidationError, RateLimitError
except ImportError:
    print("❌ Error: enable_ai_sdk not found. Please install it first:")
    print("   pip install enable_ai_sdk")
    exit(1)

# =============================================================================
# CONFIGURATION - UPDATE THESE VALUES
# =============================================================================

# Your EnableAI API credentials
ENABLE_AI_API_KEY = "your-enable-ai-api-key-here"  # Replace with your actual API key
ENABLE_AI_BASE_URL = "https://your-backend.com"    # Replace with your actual backend URL

# Agent configuration
AGENT_NAME = "Advanced Test Customer Support Agent"
AGENT_TYPE = "customer-support"
AGENT_LLM = "claude-3-5-sonnet-20241022"
AGENT_DESCRIPTION = "An advanced test customer support agent for SDK validation"
AGENT_SYSTEM_PROMPT = """You are a helpful customer support agent for a technology company. 
You provide accurate, helpful information about products, services, and policies.
Always be polite, professional, and concise in your responses."""

# Test data for feedback submission
TEST_PROMPTS = [
    "What is your return policy?",
    "How do I reset my password?",
    "What are your business hours?",
    "Do you offer technical support?",
    "What payment methods do you accept?"
]

TEST_RESPONSES = [
    "Our return policy allows returns within 30 days of purchase with original receipt.",
    "You can reset your password by clicking the 'Forgot Password' link on the login page.",
    "Our customer service is available Monday through Friday, 9 AM to 6 PM EST.",
    "Yes, we offer 24/7 technical support via phone, email, and live chat.",
    "We accept all major credit cards, PayPal, and bank transfers."
]

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

def wait_for_user():
    """Wait for user input to continue"""
    input("\nPress Enter to continue...")

def validate_config():
    """Validate the configuration"""
    print_header("Configuration Validation")
    
    if ENABLE_AI_API_KEY == "your-enable-ai-api-key-here":
        print_error("Please update ENABLE_AI_API_KEY with your actual API key")
        return False
    
    if ENABLE_AI_BASE_URL == "https://your-backend.com":
        print_error("Please update ENABLE_AI_BASE_URL with your actual backend URL")
        return False
    
    print_success("Configuration looks good!")
    return True

def test_connection(client: EnableAIClient) -> bool:
    """Test the API connection"""
    print_header("Testing API Connection")
    
    try:
        health = client.health_check()
        print_success(f"API is healthy: {health}")
        return True
    except Exception as e:
        print_error(f"Connection failed: {e}")
        return False

# =============================================================================
# MAIN TEST FUNCTIONS
# =============================================================================

def test_agent_registration(client: EnableAIClient) -> Optional[str]:
    """Test agent registration and return agent ID"""
    print_header("Testing Agent Registration")
    
    try:
        # Register the agent
        agent = client.agents.register(
            name=AGENT_NAME,
            agent_type=AGENT_TYPE,
            llm=AGENT_LLM,
            description=AGENT_DESCRIPTION,
            system_prompt=AGENT_SYSTEM_PROMPT
        )
        
        print_success(f"Agent registered successfully!")
        print(f"   ID: {agent.id}")
        print(f"   Name: {agent.name}")
        print(f"   Type: {agent.agent_type}")
        print(f"   LLM: {agent.llm}")
        print(f"   Created: {agent.created_at}")
        
        return agent.id
        
    except Exception as e:
        print_error(f"Agent registration failed: {e}")
        return None

def test_agent_listing(client: EnableAIClient):
    """Test listing all agents"""
    print_header("Testing Agent Listing")
    
    try:
        agents = client.agents.list()
        
        if not agents:
            print_info("No agents found")
            return
        
        print_success(f"Found {len(agents)} agents:")
        for agent in agents:
            print(f"   - {agent.name} ({agent.agent_type}) - ID: {agent.id}")
            
    except Exception as e:
        print_error(f"Agent listing failed: {e}")

def test_feedback_submission(client: EnableAIClient, agent_id: str):
    """Test feedback submission"""
    print_header("Testing Feedback Submission")
    
    feedback_scores = []
    
    for i, (prompt, response) in enumerate(zip(TEST_PROMPTS, TEST_RESPONSES), 1):
        try:
            feedback = client.analytics.submit_feedback(
                prompt=prompt,
                response=response,
                tool="CustomerFeedback",
                use_case="Customer Support",
                agent_id=agent_id
            )
            
            feedback_scores.append(feedback.score)
            print_success(f"Feedback {i} submitted - Score: {feedback.score}")
            
            if feedback.issue and feedback.issue != "None":
                print(f"   Issue detected: {feedback.issue}")
            
            # Small delay between submissions
            time.sleep(0.5)
            
        except Exception as e:
            print_error(f"Feedback submission {i} failed: {e}")
    
    if feedback_scores:
        avg_score = sum(feedback_scores) / len(feedback_scores)
        print_info(f"Average feedback score: {avg_score:.1f}")

def test_analytics(client: EnableAIClient, agent_id: str):
    """Test analytics and insights"""
    print_header("Testing Analytics & Insights")
    
    try:
        # Get agent insights
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

def test_self_healing(client: EnableAIClient):
    """Test self-healing functionality"""
    print_header("Testing Self-Healing")
    
    try:
        # Run self-healing scan
        scan_results = client.self_healing.scan()
        
        print_success("Self-healing scan completed:")
        print(f"   Total agents scanned: {scan_results.get('total_agents_scanned', 0)}")
        print(f"   Agents flagged: {len(scan_results.get('agents_flagged', []))}")
        
        if scan_results.get('agents_flagged'):
            print("\n   Flagged agents:")
            for agent in scan_results['agents_flagged']:
                print(f"     - {agent.get('name', 'Unknown')}: {agent.get('reason', 'Unknown reason')}")
        
    except Exception as e:
        print_error(f"Self-healing test failed: {e}")

def test_webhook_management(client: EnableAIClient):
    """Test webhook management"""
    print_header("Testing Webhook Management")
    
    try:
        # List existing webhooks
        webhooks = client.webhooks.list()
        print_success(f"Found {len(webhooks)} existing webhooks")
        
        # Create a test webhook
        test_webhook = client.webhooks.create(
            name="SDK Test Webhook",
            url="https://httpbin.org/post",  # Test endpoint
            events=["agent_self_healing_triggered", "feedback_submitted"],
            headers={"X-Test": "SDK-Test"},
            retry_count=2,
            timeout=5,
            is_active=True
        )
        
        print_success("Test webhook created:")
        print(f"   ID: {test_webhook.get('id')}")
        print(f"   Name: {test_webhook.get('name')}")
        print(f"   URL: {test_webhook.get('url')}")
        print(f"   Events: {test_webhook.get('events')}")
        
        # Test the webhook
        test_result = client.webhooks.test(test_webhook['id'])
        print_success(f"Webhook test result: {test_result.get('status', 'Unknown')}")
        
        # Clean up - delete the test webhook
        client.webhooks.delete(test_webhook['id'])
        print_success("Test webhook deleted")
        
    except Exception as e:
        print_error(f"Webhook management test failed: {e}")

def interactive_menu(client: EnableAIClient, agent_id: Optional[str] = None):
    """Interactive menu for testing different features"""
    while True:
        print_header("Interactive Testing Menu")
        print("1. Test agent registration")
        print("2. List all agents")
        print("3. Submit test feedback")
        print("4. Get agent analytics")
        print("5. Test self-healing")
        print("6. Test webhook management")
        print("7. Run full test suite")
        print("8. Exit")
        
        choice = input("\nSelect an option (1-8): ").strip()
        
        if choice == "1":
            agent_id = test_agent_registration(client)
            wait_for_user()
        elif choice == "2":
            test_agent_listing(client)
            wait_for_user()
        elif choice == "3":
            if not agent_id:
                print_error("No agent ID available. Please register an agent first.")
            else:
                test_feedback_submission(client, agent_id)
            wait_for_user()
        elif choice == "4":
            if not agent_id:
                print_error("No agent ID available. Please register an agent first.")
            else:
                test_analytics(client, agent_id)
            wait_for_user()
        elif choice == "5":
            test_self_healing(client)
            wait_for_user()
        elif choice == "6":
            test_webhook_management(client)
            wait_for_user()
        elif choice == "7":
            run_full_test_suite(client)
            wait_for_user()
        elif choice == "8":
            print_success("Goodbye!")
            break
        else:
            print_error("Invalid choice. Please select 1-8.")

def run_full_test_suite(client: EnableAIClient):
    """Run the complete test suite"""
    print_header("Running Full Test Suite")
    
    # Test 1: Agent registration
    agent_id = test_agent_registration(client)
    if not agent_id:
        print_error("Test suite failed at agent registration")
        return
    
    wait_for_user()
    
    # Test 2: Agent listing
    test_agent_listing(client)
    wait_for_user()
    
    # Test 3: Feedback submission
    test_feedback_submission(client, agent_id)
    wait_for_user()
    
    # Test 4: Analytics
    test_analytics(client, agent_id)
    wait_for_user()
    
    # Test 5: Self-healing
    test_self_healing(client)
    wait_for_user()
    
    # Test 6: Webhook management
    test_webhook_management(client)
    
    print_header("Full Test Suite Complete!")
    print_success("All tests completed successfully!")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function"""
    print_header("EnableAI SDK Template Script - Advanced Level")
    print("This is Step 3: Testing Advanced SDK Features")
    print("This script will test your EnableAI SDK end-to-end with advanced features.")
    print("Make sure you've updated the configuration section above!")
    
    # Validate configuration
    if not validate_config():
        print_error("Please fix the configuration issues and try again.")
        return
    
    # Initialize client
    try:
        client = EnableAIClient(
            api_key=ENABLE_AI_API_KEY,
            base_url=ENABLE_AI_BASE_URL
        )
        print_success("Client initialized successfully")
    except Exception as e:
        print_error(f"Failed to initialize client: {e}")
        return
    
    # Test connection
    if not test_connection(client):
        print_error("Cannot proceed without a valid connection.")
        return
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Run full test suite automatically")
    print("2. Use interactive menu")
    
    choice = input("Select option (1-2): ").strip()
    
    if choice == "1":
        run_full_test_suite(client)
    elif choice == "2":
        interactive_menu(client)
    else:
        print_error("Invalid choice. Running full test suite...")
        run_full_test_suite(client)

if __name__ == "__main__":
    main() 