# 🩹 Self-Healing Walkthrough: From Zero to Hero

This comprehensive guide explains how the EnableAI SDK's self-healing feature works and how to use it effectively.

## 🎯 Overview

The self-healing feature automatically improves your AI agents when their performance degrades. It uses a **two-step process** to prevent errors and ensure reliable improvements.

## 🚀 Beginner Walkthrough: From Zero to Hero

### Step 1: Understanding the Problem

**The Issue**: Self-healing requires agents to be "flagged" before they can be healed. Without proper flagging, you get 400 errors.

**The Solution**: The SDK now handles this automatically with a two-step process.

### Step 2: Basic Setup

```python
import openai
import os
from enable_ai_sdk import create_monitored_agent

# Your existing AI model
def my_ai_agent(prompt: str) -> str:
    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Create monitored agent (3 lines!)
monitored_agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=my_ai_agent
)

# Use it normally - everything is automatic!
response = monitored_agent.generate_response("What is your return policy?")
```

### Step 3: What Happens Behind the Scenes

When you use the monitored agent, the SDK automatically:

1. **Reports Performance**: Every interaction is sent for evaluation
2. **Gets Quality Scores**: Claude evaluates the response (1-100 scale)
3. **Checks Health**: Monitors agent performance over time
4. **Triggers Scan**: If performance is poor, runs a self-healing scan
5. **Flags Agent**: If needed, flags the agent for healing
6. **Applies Improvements**: Generates and applies better prompts

### Step 4: Understanding the Two-Step Process

#### Step 4a: Performance Scan
```python
# The SDK automatically does this:
scan_response = requests.post(
    "https://api.weenable.ai/self-healing/scan",
    headers={"x-api-key": "your-api-key"},
    json={}
)

# This identifies agents that need healing
# and flags them with healing_recommended=True
```

#### Step 4b: Prompt Improvement
```python
# Only flagged agents can be healed:
healing_response = requests.post(
    "https://api.weenable.ai/agent/self_heal",
    headers={"x-api-key": "your-api-key"},
    json={
        "agent_id": "your-agent-id",
        "strategy": "auto"  # or "suggest"
    }
)

# This generates improved prompts using Claude
# and applies them automatically
```

### Step 5: Error Prevention

The SDK prevents common errors:

- **400 Errors**: Handles validation automatically
- **Missing Flags**: Ensures agents are flagged before healing
- **Network Issues**: Graceful fallback if healing fails
- **Invalid Data**: Validates all inputs before processing

## 🔧 Advanced Walkthrough: Customization and Control

### Advanced Configuration

```python
from enable_ai_sdk.agent_monitor import AgentMonitor

class CustomMonitoredAgent(AgentMonitor):
    def __init__(self, agent_id: str, api_key: str, **kwargs):
        super().__init__(
            agent_id=agent_id,
            api_key=api_key,
            auto_healing=True,  # Enable automatic healing
            report_async=True,   # Report performance asynchronously
            system_prompt="You are a helpful customer service assistant."
        )
    
    def _call_ai_model(self, prompt: str, **kwargs) -> str:
        # Your custom AI model logic here
        return "Your AI response"

# Create the agent
agent = CustomMonitoredAgent(
    agent_id="your-agent-id",
    api_key="your-api-key"
)
```

### Manual Self-Healing Control

```python
# Check agent health
health = agent.get_health_status()
print(f"Status: {health.get('status')}")
print(f"Average Score: {health.get('average_score')}")

# Get analytics
analytics = agent.get_analytics()
print(f"Recent Issues: {analytics.get('recent_issues')}")

# Get insights
insights = agent.get_insights()
print(f"Suggested Actions: {insights.get('suggested_actions')}")
```

### Webhook Integration

```python
from enable_ai_sdk import EnableAIClient

client = EnableAIClient(api_key="your-api-key")

# Create webhook for self-healing notifications
webhook = client.webhooks.create(
    name="Self-Healing Alerts",
    url="https://your-endpoint.com/webhook",
    events=["agent_self_healing_triggered"]
)

print(f"✅ Webhook created: {webhook['name']}")
```

## 📊 Monitoring and Debugging

### Health Check Script

```python
import requests

def check_agent_health(agent_id: str, api_key: str):
    """Check if your agent is working properly"""
    
    headers = {"x-api-key": api_key}
    
    # Check health status
    health_response = requests.get(
        f"https://api.weenable.ai/agent/external/health?agent_id={agent_id}",
        headers=headers
    )
    
    if health_response.status_code == 200:
        health_data = health_response.json()
        print(f"✅ Health check successful:")
        print(f"   Status: {health_data.get('status')}")
        print(f"   Average Score: {health_data.get('average_score')}")
        print(f"   Total Interactions: {health_data.get('total_interactions')}")
        
        # Check if agent needs healing
        if health_data.get('status') in ['warning', 'critical']:
            print("⚠️  Agent needs healing!")
        else:
            print("✅ Agent is healthy!")
    else:
        print(f"❌ Health check failed: {health_response.status_code}")

# Use it
check_agent_health("your-agent-id", "your-api-key")
```

### Debug Self-Healing

```python
def debug_self_healing(agent_id: str, api_key: str):
    """Debug self-healing issues"""
    
    headers = {"x-api-key": api_key}
    
    # Step 1: Check if agent is flagged for healing
    agents_response = requests.get(
        "https://api.weenable.ai/user/agents",
        headers=headers
    )
    
    if agents_response.status_code == 200:
        agents = agents_response.json().get('agents', [])
        for agent in agents:
            if agent.get('id') == agent_id:
                healing_recommended = agent.get('healing_recommended', False)
                print(f"Agent flagged for healing: {healing_recommended}")
                
                if not healing_recommended:
                    print("🔄 Agent not flagged. Triggering scan...")
                    
                    # Trigger scan
                    scan_response = requests.post(
                        "https://api.weenable.ai/self-healing/scan",
                        headers=headers,
                        json={}
                    )
                    
                    if scan_response.status_code == 200:
                        print("✅ Scan completed. Agent should now be flagged.")
                    else:
                        print(f"❌ Scan failed: {scan_response.status_code}")
                break

# Use it
debug_self_healing("your-agent-id", "your-api-key")
```

## 🚨 Common Issues and Solutions

### Issue 1: 400 Error on Self-Healing

**Problem**: `ERROR:enable_ai_sdk.agent_monitor:Failed to trigger self-healing: 400`

**Solution**: The SDK now handles this automatically. The error occurs when trying to heal an agent that isn't flagged. The updated SDK:

1. Triggers a scan first
2. Flags the agent if needed
3. Only then attempts healing

### Issue 2: Agent Not Getting Better

**Problem**: Agent performance isn't improving despite self-healing

**Solution**: 
1. Check if the agent has enough feedback data (minimum 3 interactions)
2. Verify the agent is actually flagged for healing
3. Check the quality scores to see if improvements are being applied

### Issue 3: Self-Healing Not Triggering

**Problem**: Self-healing never seems to activate

**Solution**:
1. Ensure your agent has poor performance (score < 75)
2. Check that you have enough interactions (minimum 3)
3. Verify your API key has the correct permissions

## 📈 Best Practices

### 1. Start Simple
```python
# Begin with the basic drop-in integration
monitored_agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model
)
```

### 2. Monitor Performance
```python
# Regularly check your agent's health
health = monitored_agent.get_health_status()
if health.get('status') == 'critical':
    print("⚠️  Agent needs attention!")
```

### 3. Use Webhooks
```python
# Set up notifications for self-healing events
webhook = client.webhooks.create(
    name="Healing Alerts",
    url="https://your-endpoint.com/webhook",
    events=["agent_self_healing_triggered"]
)
```

### 4. Test Thoroughly
```python
# Test with various scenarios
test_prompts = [
    "What is your return policy?",
    "How do I reset my password?",
    "What are your business hours?",
    "Can I get a refund?",
    "Do you offer technical support?"
]

for prompt in test_prompts:
    response = monitored_agent.generate_response(prompt)
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")
    print("---")
```

## 🎉 Success Metrics

When self-healing is working properly, you should see:

- ✅ **No 400 errors** in your logs
- ✅ **Automatic scan triggers** when performance is poor
- ✅ **Agent flagging** for agents that need healing
- ✅ **Prompt improvements** being applied
- ✅ **Improving quality scores** over time
- ✅ **Webhook notifications** when healing occurs

## 🔗 Resources

- [GitHub Repository](https://github.com/dmartin4506/enable-ai-sdk)
- [API Documentation](https://docs.enable.ai)
- [Support](mailto:support@enable.ai)

---

**Remember**: The SDK now handles all the complexity automatically. Just wrap your agent and let it do its magic! 🪄 