# EnableAI Agentic AI Platform SDK

A comprehensive Python SDK for the EnableAI Agentic AI Platform, providing easy-to-use interfaces for agent management, analytics, self-healing, and webhooks.

## 🚀 Features

- **Agent Management**: Register, update, and manage AI agents
- **Analytics & Insights**: Get detailed analytics and performance insights
- **Self-Healing**: Monitor and automatically heal underperforming agents
- **Webhook Management**: Configure real-time notifications
- **Feedback System**: Submit and evaluate AI responses

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/dmartin4506/enable-ai-sdk.git
cd enable-ai-sdk

# Install the package
pip install -e .

# Or install directly from PyPI (when published)
pip install enable-ai-sdk
```

## 🔑 Quick Start

### Option 1: Progressive Samples (Recommended)
Start with our progressive samples to learn the SDK step by step:

```bash
# Step 1: Test SDK installation
cd samples/01-beginner
python test_sdk_import.py

# Step 2: Test core functionality
cd ../02-intermediate
# Edit simple_agent_template.py to add your API key
python simple_agent_template.py

# Step 3: Test advanced features
cd ../03-advanced
# Edit agent_template.py to add your API key
python agent_template.py
```

### Option 2: Direct Usage
```python
import os
from enable_ai_sdk import EnableAIClient

# Initialize client
client = EnableAIClient(
    api_key=os.getenv('ENABLE_AI_API_KEY'),  # Use environment variable
    base_url=os.getenv('ENABLE_AI_BASE_URL', 'https://api.enable.ai')
)

# Register an agent
agent = client.agents.register(
    name="My Customer Support Agent",
    agent_type="customer-support",
    llm="claude-3-5-sonnet-20241022",
    description="A helpful customer support agent"
)

print(f"✅ Registered agent: {agent.name} (ID: {agent.id})")
```

## 📚 Samples & Examples

### Progressive Learning Samples
We provide a structured learning path with progressive samples:

- **📚 Beginner (01-beginner)**: Test SDK installation and basic setup
- **🚀 Intermediate (02-intermediate)**: Test core functionality (agents, feedback, analytics)
- **🔧 Advanced (03-advanced)**: Test all features with interactive options

See [samples/README.md](samples/README.md) for detailed instructions.

### Integration Examples
Check the [examples/](examples/) directory for:
- `basic_usage.py` - Basic SDK usage examples
- `flask_integration.py` - Flask web application integration

## 📚 API Reference

### Client Initialization

```python
import os
from enable_ai_sdk import EnableAIClient, create_client

# Method 1: Direct initialization
client = EnableAIClient(
    api_key=os.getenv('ENABLE_AI_API_KEY'),
    base_url=os.getenv('ENABLE_AI_BASE_URL', 'https://api.enable.ai')
)

# Method 2: Using convenience function
client = create_client(
    api_key=os.getenv('ENABLE_AI_API_KEY'),
    base_url=os.getenv('ENABLE_AI_BASE_URL', 'https://api.enable.ai')
)
```

### Agent Management

```python
# Register a new agent
agent = client.agents.register(
    name="Sales Assistant",
    agent_type="sales-assistant",
    llm="claude-3-5-sonnet-20241022",
    description="A sales assistant agent",
    system_prompt="You are a helpful sales assistant..."
)

# List all agents
agents = client.agents.list()
for agent in agents:
    print(f"- {agent.name} ({agent.agent_type})")

# Get specific agent
agent = client.agents.get(agent_id="agent-uuid")

# Update agent
updated_agent = client.agents.update(
    agent_id="agent-uuid",
    name="Updated Agent Name",
    description="New description"
)

# Delete agent
client.agents.delete(agent_id="agent-uuid")

# Get prompt history
history = client.agents.get_prompt_history(agent_id="agent-uuid")
```

### Analytics & Insights

```python
# Get agent insights
insights = client.analytics.get_agent_insights(
    agent_id="agent-uuid",
    start_date="2024-01-01T00:00:00Z",
    end_date="2024-01-31T23:59:59Z"
)

print(f"Agent: {insights.agent_name}")
print(f"Score Trend: {insights.score_trend}")
print(f"Average Score: {insights.average_score}")
print(f"Recent Issues: {insights.recent_issues}")

# Get detailed analytics
analytics = client.analytics.get_agent_analytics(
    agent_id="agent-uuid",
    start_date="2024-01-01T00:00:00Z",
    end_date="2024-01-31T23:59:59Z",
    tool="CustomerFeedback",
    use_case="Customer Support"
)

# Submit feedback for evaluation
feedback = client.analytics.submit_feedback(
    prompt="What is your return policy?",
    response="Our return policy allows returns within 30 days.",
    tool="CustomerFeedback",
    use_case="Customer Support",
    agent_id="agent-uuid"
)

print(f"Feedback Score: {feedback.score}")
print(f"Issue: {feedback.issue}")
```

### Self-Healing Management

```python
# Run self-healing scan
scan_results = client.self_healing.scan()

# Get agent healing status
status = client.self_healing.get_agent_status(agent_id="agent-uuid")

# Heal an agent
healing_result = client.self_healing.heal_agent(
    agent_id="agent-uuid",
    strategy="auto",  # or "suggest"
    start_date="2024-01-01T00:00:00Z",
    end_date="2024-01-31T23:59:59Z"
)
```

### Webhook Management

```python
# List all webhooks
webhooks = client.webhooks.list()

# Create a new webhook
webhook = client.webhooks.create(
    name="My Webhook",
    url="https://my-endpoint.com/webhook",
    events=["agent_self_healing_triggered", "feedback_submitted"],
    headers={"Authorization": "Bearer token"},
    retry_count=3,
    timeout=10,
    is_active=True
)

# Update webhook
updated_webhook = client.webhooks.update(
    webhook_id=123,
    name="Updated Webhook Name",
    is_active=False
)

# Test webhook
test_result = client.webhooks.test(webhook_id=123)

# Get webhook history
history = client.webhooks.get_history(webhook_id=123)

# Delete webhook
client.webhooks.delete(webhook_id=123)
```

## 🛠️ Convenience Functions

For quick operations, you can use the convenience functions:

```python
import os
from enable_ai_sdk import quick_agent_register, quick_feedback_submit

# Quick agent registration
agent = quick_agent_register(
    api_key=os.getenv('ENABLE_AI_API_KEY'),
    name="Quick Agent",
    agent_type="customer-support"
)

# Quick feedback submission
feedback = quick_feedback_submit(
    api_key=os.getenv('ENABLE_AI_API_KEY'),
    prompt="What is your return policy?",
    response="Our return policy allows returns within 30 days.",
    tool="CustomerFeedback",
    use_case="Customer Support"
)
```

## 🔧 Error Handling

The SDK provides specific exception types for different error scenarios:

```python
import os
from enable_ai_sdk import EnableAIClient, AuthenticationError, ValidationError, RateLimitError

try:
    client = EnableAIClient(api_key=os.getenv('ENABLE_AI_API_KEY'))
    agent = client.agents.register(name="Test", agent_type="test", llm="test")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except ValidationError as e:
    print(f"Validation error: {e}")
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 📊 Data Models

The SDK uses dataclasses for structured data:

```python
from enable_ai_sdk import Agent, AnalyticsResult, FeedbackResult

# Agent model
agent = Agent(
    id="uuid",
    name="My Agent",
    description="A helpful agent",
    agent_type="customer-support",
    llm="claude-3-5-sonnet-20241022",
    system_prompt="You are a helpful assistant...",
    created_at="2024-01-01T00:00:00Z",
    customer_id=123,
    user_id=456,
    healing_recommended=False
)

# Analytics result model
analytics = AnalyticsResult(
    agent_id="uuid",
    agent_name="My Agent",
    recent_issues=[{"issue": "Hallucination", "count": 5}],
    score_trend="improving",
    feedback_count=42,
    average_score=78.5,
    suggested_actions=["Add more context", "Improve grounding"],
    last_updated="2024-01-01T00:00:00Z"
)

# Feedback result model
feedback = FeedbackResult(
    score=85.0,
    issue="None",
    feedback_id="uuid",
    timestamp="2024-01-01T00:00:00Z"
)
```

## 🔍 Health Check

```python
# Check API health
health = client.health_check()
print(f"API Status: {health}")
```

## 📝 Complete Example

```python
from enable_ai_sdk import EnableAIClient
import time

def main():
    # Initialize client
    client = EnableAIClient(
        api_key=os.getenv('ENABLE_AI_API_KEY'),
        base_url=os.getenv('ENABLE_AI_BASE_URL', 'https://api.enable.ai')
    )
    
    # Register an agent
    agent = client.agents.register(
        name="Customer Support Agent",
        agent_type="customer-support",
        llm="claude-3-5-sonnet-20241022",
        description="A helpful customer support agent"
    )
    
    print(f"✅ Registered agent: {agent.name}")
    
    # Submit some feedback
    feedback = client.analytics.submit_feedback(
        prompt="What is your return policy?",
        response="Our return policy allows returns within 30 days of purchase.",
        tool="CustomerFeedback",
        use_case="Customer Support",
        agent_id=agent.id
    )
    
    print(f"✅ Feedback submitted - Score: {feedback.score}")
    
    # Wait a moment for processing
    time.sleep(2)
    
    # Get agent insights
    insights = client.analytics.get_agent_insights(agent.id)
    
    print(f"✅ Agent insights:")
    print(f"   - Trend: {insights.score_trend}")
    print(f"   - Average Score: {insights.average_score}")
    print(f"   - Recent Issues: {len(insights.recent_issues)}")
    print(f"   - Suggested Actions: {len(insights.suggested_actions)}")
    
    # Create a webhook for notifications
    webhook = client.webhooks.create(
        name="Agent Monitoring",
        url="https://my-endpoint.com/webhook",
        events=["agent_self_healing_triggered", "feedback_submitted"]
    )
    
    print(f"✅ Created webhook: {webhook['name']}")
    
    # Run self-healing scan
    scan_results = client.self_healing.scan()
    
    print(f"✅ Self-healing scan completed:")
    print(f"   - Agents scanned: {scan_results['total_agents_scanned']}")
    print(f"   - Agents flagged: {len(scan_results['agents_flagged'])}")

if __name__ == "__main__":
    main()
```

## 🔗 Integration Examples

### Flask Integration

```python
from flask import Flask, request, jsonify
from enable_ai_sdk import EnableAIClient

app = Flask(__name__)
client = EnableAIClient(api_key=os.getenv('ENABLE_AI_API_KEY'))

@app.route('/register_agent', methods=['POST'])
def register_agent():
    data = request.json
    agent = client.agents.register(
        name=data['name'],
        agent_type=data['agent_type'],
        llm=data['llm']
    )
    return jsonify({
        'agent_id': agent.id,
        'name': agent.name,
        'status': 'registered'
    })

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    feedback = client.analytics.submit_feedback(
        prompt=data['prompt'],
        response=data['response'],
        tool=data['tool'],
        use_case=data['use_case']
    )
    return jsonify({
        'score': feedback.score,
        'issue': feedback.issue
    })
```

### Django Integration

```python
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from enable_ai_sdk import EnableAIClient

client = EnableAIClient(api_key=os.getenv('ENABLE_AI_API_KEY'))

@csrf_exempt
def register_agent(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        agent = client.agents.register(
            name=data['name'],
            agent_type=data['agent_type'],
            llm=data['llm']
        )
        return JsonResponse({
            'agent_id': agent.id,
            'name': agent.name
        })
```

## 🔒 Security Best Practices

**Important**: The SDK is designed to be secure, but users are responsible for implementing proper security practices in their applications.

### 1. **Secure API Key Management** ⚠️
Never hardcode API keys in your source code. Always use environment variables:

```python
import os
from enable_ai_sdk import EnableAIClient

# ✅ SECURE: Use environment variables
client = EnableAIClient(
    api_key=os.getenv('ENABLE_AI_API_KEY'),
    base_url=os.getenv('ENABLE_AI_BASE_URL', 'https://api.enable.ai')
)

# ❌ INSECURE: Never do this
client = EnableAIClient(
    api_key="sk-1234567890abcdef",  # Don't hardcode!
    base_url="https://api.enable.ai"
)
```

### 2. **Use HTTPS in Production** ⚠️
Always use HTTPS URLs in production environments:

```python
# ✅ SECURE: Use HTTPS
client = EnableAIClient(
    api_key=os.getenv('ENABLE_AI_API_KEY'),
    base_url="https://api.enable.ai"  # HTTPS for production
)

# ❌ INSECURE: Don't use HTTP in production
client = EnableAIClient(
    api_key=os.getenv('ENABLE_AI_API_KEY'),
    base_url="http://localhost:5001"  # Only for development
)
```

### 3. **Implement Proper Error Handling** ⚠️
Handle errors gracefully without exposing sensitive information:

```python
import logging
from enable_ai_sdk import EnableAIClient, EnableAIError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_api_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except EnableAIError as e:
        logger.error(f"EnableAI API error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None

# Usage
client = EnableAIClient(api_key=os.getenv('ENABLE_AI_API_KEY'))
agent = safe_api_call(client.agents.register, "Test Agent", "customer-support", "claude-3-5-sonnet-20241022")
```

## 🚀 Production Considerations

### Environment Variables

### Error Handling

```python
import logging
from enable_ai_sdk import EnableAIClient, EnableAIError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_api_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except EnableAIError as e:
        logger.error(f"EnableAI API error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None

# Usage
client = EnableAIClient(api_key=os.getenv('ENABLE_AI_API_KEY'))
agent = safe_api_call(client.agents.register, "Test Agent", "customer-support", "claude-3-5-sonnet-20241022")
```

### Rate Limiting

```python
import time
from enable_ai_sdk import EnableAIClient, RateLimitError

def api_call_with_retry(client, func, *args, **kwargs):
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                continue
            raise
        except Exception as e:
            raise e

# Usage
client = EnableAIClient(api_key=os.getenv('ENABLE_AI_API_KEY'))
agent = api_call_with_retry(client, client.agents.register, "Test Agent", "customer-support", "claude-3-5-sonnet-20241022")
```

## 📞 Support

For support and questions:

- **Documentation**: [https://www.weenable.ai](https://www.weenable.ai)
- **API Reference**: [https://www.weenable.ai](https://www.weenable.ai)
- **GitHub Issues**: [https://github.com/dmartin4506/enable-ai-sdk/issues](https://github.com/dmartin4506/enable-ai-sdk/issues)
- **Email**: support@weenable.ai

## 📄 License

This SDK is licensed under the MIT License. See the LICENSE file for details. 