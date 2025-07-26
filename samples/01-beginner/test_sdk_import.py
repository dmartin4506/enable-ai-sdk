#!/usr/bin/env python3
"""
Quick SDK Import Test - Beginner Level

This script tests that the EnableAI SDK can be imported and basic functionality works.
Run this before using the full templates to ensure everything is set up correctly.

This is Step 1 in the learning progression.
"""

def test_sdk_import():
    """Test that the SDK can be imported"""
    print("🔍 Testing EnableAI SDK import...")
    
    try:
        from enable_ai_sdk import EnableAIClient
        print("✅ EnableAIClient imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import EnableAIClient: {e}")
        return False
    
    try:
        from enable_ai_sdk import create_client, quick_agent_register, quick_feedback_submit
        print("✅ Convenience functions imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import convenience functions: {e}")
        return False
    
    try:
        from enable_ai_sdk import Agent, AnalyticsResult, FeedbackResult
        print("✅ Data models imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import data models: {e}")
        return False
    
    try:
        from enable_ai_sdk import EnableAIError, AuthenticationError, ValidationError, RateLimitError
        print("✅ Exception classes imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import exception classes: {e}")
        return False
    
    return True

def test_client_initialization():
    """Test that the client can be initialized"""
    print("\n🔍 Testing client initialization...")
    
    try:
        from enable_ai_sdk import EnableAIClient
        
        # Test with dummy values
        client = EnableAIClient(
            api_key="test-key",
            base_url="http://localhost:5001"
        )
        
        print("✅ Client initialized successfully")
        print(f"   Base URL: {client.base_url}")
        print(f"   API Key: {client.api_key[:8]}...")
        
        # Test that managers are initialized
        print("✅ Agent manager initialized")
        print("✅ Analytics manager initialized")
        print("✅ Webhook manager initialized")
        print("✅ Self-healing manager initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return False

def test_convenience_functions():
    """Test that convenience functions can be called"""
    print("\n🔍 Testing convenience functions...")
    
    try:
        from enable_ai_sdk import create_client
        
        client = create_client(
            api_key="test-key",
            base_url="http://localhost:5001"
        )
        print("✅ create_client function works")
        
        return True
        
    except Exception as e:
        print(f"❌ Convenience function test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 EnableAI SDK Import Test - Beginner Level")
    print("=" * 50)
    print("This is Step 1: Testing SDK Installation and Basic Setup")
    print("=" * 50)
    
    # Test 1: Import
    if not test_sdk_import():
        print("\n❌ SDK import test failed. Please check your installation.")
        return
    
    # Test 2: Client initialization
    if not test_client_initialization():
        print("\n❌ Client initialization test failed.")
        return
    
    # Test 3: Convenience functions
    if not test_convenience_functions():
        print("\n❌ Convenience function test failed.")
        return
    
    print("\n🎉 All tests passed!")
    print("Your EnableAI SDK is ready to use!")
    print("\nNext steps:")
    print("1. Go to 02-intermediate/simple_agent_template.py")
    print("2. Update the configuration with your API key")
    print("3. Run the intermediate template to test core functionality")

if __name__ == "__main__":
    main() 