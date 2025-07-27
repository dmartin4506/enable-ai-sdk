# EnableAI Agentic AI Platform SDK

A **drop-in SDK** for automatic agent monitoring and self-healing. Simply wrap your existing AI agent and get automatic performance evaluation, quality scoring, and prompt improvements.

## 🚀 Features

- **Drop-in Integration**: Just import and wrap your agent
- **Automatic Monitoring**: Every interaction gets evaluated
- **Self-Healing**: Automatic improvements when performance degrades
- **Quality Evaluation**: Claude-powered 1-100 scoring
- **Real-time Analytics**: Performance insights and trends
- **Background Monitoring**: Continuous health checking

## 📦 Installation

```bash
# Install the drop-in SDK
pip install enable-ai-sdk

# Or install from local directory
pip install -e .
```

## 🔑 Quick Start (3 Lines!)

```python
from enable_ai_sdk.agent_monitor import create_monitored_agent

# Wrap your existing AI model
monitored_agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model
)

# Use it normally - everything is automatic!
response = monitored_agent.generate_response("What is your return policy?")

# The SDK automatically:
# - Reports performance for evaluation
# - Gets quality scores from Claude
# - Triggers self-healing when needed
# - Applies prompt improvements
```

## 📚 API Reference

### Simple Integration

```python
from enable_ai_sdk.agent_monitor import create_monitored_agent

# Your existing AI model function
def your_ai_model(prompt: str) -> str:
    return "Response from your AI model"

# Create monitored agent (3 lines!)
monitored_agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model
)

# Use it normally
response = monitored_agent.generate_response("Hello!")
```

### Advanced Integration

```python
from enable_ai_sdk.agent_monitor import AgentMonitor
import openai

class MonitoredCustomerSupportAgent(AgentMonitor):
    def _call_ai_model(self, prompt: str, **kwargs) -> str:
        # Your AI model integration here
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

# Create the agent
agent = MonitoredCustomerSupportAgent(
    agent_id="your-agent-id",
    api_key="your-api-key"
)

# Use it - everything is automatic!
response = agent.generate_response("What is your return policy?")
```

### AWS Lambda Integration

```python
import json
from enable_ai_sdk.agent_monitor import create_monitored_agent

# Your AI model function
def my_ai_model(prompt: str) -> str:
    return "Response from your AI model"

# Create monitored agent
agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=my_ai_model
)

def lambda_handler(event, context):
    user_input = event['body']['message']
    response = agent.generate_response(user_input)  # Automatically monitored!
    return {'response': response}
```

## 📊 What Gets Tracked Automatically

### Performance Metrics
- **Quality Score**: 1-100 rating from Claude
- **Response Time**: How long your agent takes
- **Issue Categories**: Hallucination, tone, format, etc.
- **Usage Patterns**: When and how your agent is used

### Self-Healing Triggers
- **Poor Performance**: Average score < 75
- **Critical Issues**: Average score < 60
- **Declining Trends**: Performance getting worse
- **Specific Issues**: Hallucination, tone problems, etc.

### Automatic Actions
- **Prompt Improvements**: AI-generated better prompts
- **Health Monitoring**: Real-time status checking
- **Performance Reporting**: Every interaction evaluated
- **Insight Generation**: AI recommendations

## 🔧 Configuration Options

### Basic Setup
```python
agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model
)
```

### Advanced Configuration
```python
agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    base_url="https://your-backend.com",
    auto_healing=True,      # Enable automatic prompt improvements
    report_async=True       # Report performance asynchronously
)
```

### Custom Agent Class
```python
class MyMonitoredAgent(AgentMonitor):
    def _call_ai_model(self, prompt: str, **kwargs) -> str:
        # Your custom AI model integration
        return your_ai_model.generate(prompt)

agent = MyMonitoredAgent(
    agent_id="your-agent-id",
    api_key="your-api-key"
)
```

## 🎯 Key Benefits

### For Agent Developers
1. **Drop-in Integration**: Just import and wrap your agent
2. **Automatic Monitoring**: Every interaction gets evaluated
3. **Self-Healing**: Automatic improvements when needed
4. **Real-time Insights**: Performance analytics and recommendations

### For Agent Operators
1. **Zero Manual Work**: Everything is automatic
2. **Proactive Alerts**: Get notified when agents need attention
3. **Continuous Improvement**: Agents get better over time
4. **Comprehensive Analytics**: Detailed performance tracking

## 🔄 Complete Workflow

### 1. Register Your Agent
```python
# In your EnableAI console or via API
agent_id = register_agent("My Customer Support Agent")
```

### 2. Wrap Your Agent
```python
from enable_ai_sdk.agent_monitor import create_monitored_agent

# Your existing AI model
def my_ai_model(prompt: str) -> str:
    return your_ai_model.generate(prompt)

# Create monitored agent
agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=my_ai_model
)
```

### 3. Use Normally
```python
# Use it like any other agent
response = agent.generate_response("What is your return policy?")

# Everything is automatic:
# ✅ Performance reported
# ✅ Quality evaluated
# ✅ Self-healing triggered if needed
# ✅ Prompt improvements applied
```

## 📚 Additional Resources

### Manual API Access (Advanced Users)
If you need direct API access for custom integrations, see the [Manual API Reference](#manual-api-reference) section below.

### Examples
- [Basic Integration](examples/basic_usage.py)
- [Flask Integration](examples/flask_integration.py)
- [Real Agent Integration](examples/real_agent_integration.py)

### Documentation
- [Complete API Reference](SDK_README.md)
- [Installation Guide](INSTALLATION_GUIDE.md)
- [Integration Examples](examples/)

## 🔧 Manual API Reference

For advanced users who need direct API access:

### Client Initialization

```python
from enable_ai_sdk import EnableAIClient

# Initialize client
client = EnableAIClient(
    api_key="your-api-key-here",
    base_url="https://your-backend.com"
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
agent = client.agents.get(agent_id="your-agent-id")

# Update agent
updated_agent = client.agents.update(
    agent_id="your-agent-id",
    name="Updated Agent Name",
    description="Updated description"
)

# Delete agent
client.agents.delete(agent_id="your-agent-id")
```

### Analytics & Feedback

```python
# Submit feedback for evaluation
feedback = client.analytics.submit_feedback(
    prompt="What is your return policy?",
    response="Our return policy allows returns within 30 days of purchase.",
    tool="CustomerFeedback",
    use_case="Customer Support",
    agent_id="your-agent-id"
)

print(f"✅ Feedback submitted - Score: {feedback.score}")

# Get agent insights
insights = client.analytics.get_agent_insights(agent_id="your-agent-id")

print(f"✅ Agent insights:")
print(f"   - Trend: {insights.score_trend}")
print(f"   - Average Score: {insights.average_score}")
print(f"   - Recent Issues: {len(insights.recent_issues)}")
print(f"   - Suggested Actions: {len(insights.suggested_actions)}")
```

### Self-Healing

```python
# Run self-healing scan
scan_results = client.self_healing.scan()

print(f"✅ Self-healing scan completed:")
print(f"   - Agents scanned: {scan_results['total_agents_scanned']}")
print(f"   - Agents flagged: {len(scan_results['agents_flagged'])}")

# Get agent healing status
healing_status = client.self_healing.get_agent_healing_status(agent_id="your-agent-id")

# Heal an agent
healing_result = client.self_healing.heal_agent(agent_id="your-agent-id")
```

### Webhook Management

```python
# Create a webhook
webhook = client.webhooks.create(
    name="Agent Monitoring",
    url="https://my-endpoint.com/webhook",
    events=["agent_self_healing_triggered", "feedback_submitted"]
)

print(f"✅ Created webhook: {webhook['name']}")

# List webhooks
webhooks = client.webhooks.list()

# Test webhook
test_result = client.webhooks.test(webhook_id=webhook['id'])

# Delete webhook
client.webhooks.delete(webhook_id=webhook['id'])
```

### Quick Functions

```python
from enable_ai_sdk import quick_agent_register, quick_feedback_submit

# Quick agent registration
agent = quick_agent_register(
    api_key="your-key",
    name="Quick Agent",
    agent_type="customer-support"
)

# Quick feedback submission
feedback = quick_feedback_submit(
    api_key="your-key",
    prompt="What is your return policy?",
    response="Our return policy allows returns within 30 days.",
    tool="CustomerFeedback",
    use_case="Customer Support"
)
```

## 🔧 Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from enable_ai_sdk import EnableAIClient, AuthenticationError, ValidationError, RateLimitError

try:
    client = EnableAIClient(api_key="invalid-key")
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
        api_key="your-api-key",
        base_url="https://your-backend.com"
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
        'name': agent.name
    })

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    feedback = client.analytics.submit_feedback(
        prompt=data['prompt'],
        response=data['response'],
        tool=data['tool'],
        use_case=data['use_case'],
        agent_id=data['agent_id']
    )
    return jsonify({
        'score': feedback.score,
        'feedback_id': feedback.feedback_id
    })

if __name__ == '__main__':
    app.run(debug=True)
```

### Django Integration

```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from enable_ai_sdk import EnableAIClient
import json

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

@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        feedback = client.analytics.submit_feedback(
            prompt=data['prompt'],
            response=data['response'],
            tool=data['tool'],
            use_case=data['use_case'],
            agent_id=data['agent_id']
        )
        return JsonResponse({
            'score': feedback.score,
            'feedback_id': feedback.feedback_id
        })
```

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enable_ai_sdk import EnableAIClient

app = FastAPI()
client = EnableAIClient(api_key=os.getenv('ENABLE_AI_API_KEY'))

class AgentRequest(BaseModel):
    name: str
    agent_type: str
    llm: str

class FeedbackRequest(BaseModel):
    prompt: str
    response: str
    tool: str
    use_case: str
    agent_id: str

@app.post("/register_agent")
async def register_agent(request: AgentRequest):
    try:
        agent = client.agents.register(
            name=request.name,
            agent_type=request.agent_type,
            llm=request.llm
        )
        return {
            'agent_id': agent.id,
            'name': agent.name
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/submit_feedback")
async def submit_feedback(request: FeedbackRequest):
    try:
        feedback = client.analytics.submit_feedback(
            prompt=request.prompt,
            response=request.response,
            tool=request.tool,
            use_case=request.use_case,
            agent_id=request.agent_id
        )
        return {
            'score': feedback.score,
            'feedback_id': feedback.feedback_id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## 🚀 Getting Started

1. **Install the SDK**: `pip install enable-ai-sdk`
2. **Get your API key**: Sign up at [EnableAI](https://enable.ai)
3. **Wrap your agent**: Use the drop-in integration above
4. **Start monitoring**: Everything is automatic!

## 📞 Support

- **Documentation**: [https://docs.enable.ai](https://docs.enable.ai)
- **GitHub Issues**: [https://github.com/enable-ai/sdk/issues](https://github.com/enable-ai/sdk/issues)
- **Email Support**: support@enable.ai

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 