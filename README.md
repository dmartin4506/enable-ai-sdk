# EnableAI Agentic AI Platform SDK

A **drop-in SDK** for automatic agent monitoring and self-healing. Simply wrap your existing AI agent and get automatic performance evaluation, quality scoring, and prompt improvements.

## 🚀 Features

- **Drop-in Integration**: Just import and wrap your agent
- **Automatic Monitoring**: Every interaction gets evaluated
- **Sampling-Based Monitoring**: Optional cost-effective monitoring for production
- **Self-Healing**: Two-step process (scan + heal) for reliable improvements
- **Quality Evaluation**: Claude-powered 1-100 scoring
- **Real-time Analytics**: Performance insights and trends
- **Background Monitoring**: Continuous health checking
- **Error Prevention**: Automatic handling of self-healing validation
- **Batch Processing**: Efficient batch reporting for high-volume agents

## 📦 Installation

```bash
# Install the drop-in SDK
pip install enable-ai-sdk

# Or install from local directory
pip install -e .
```

## 🔑 Quick Start (3 Lines!)

### Full Monitoring (Default)
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
# - Triggers self-healing scan when needed
# - Flags agents for healing if performance is poor
# - Applies prompt improvements automatically
# - Handles all validation and error prevention
```

### Sampling-Based Monitoring (New!)
```python
from enable_ai_sdk.agent_monitor import create_sampled_agent

# Only 5% of interactions are reported (cost-effective for production)
sampled_agent = create_sampled_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    sampling_rate=0.05  # 5% sampling
)

# Use it normally - only sampled interactions are reported!
response = sampled_agent.generate_response("What is your return policy?")

# Benefits:
# - 95% reduction in API calls
# - Cost-effective for high-volume agents
# - Still provides meaningful performance insights
# - Perfect for production deployments
```

## 📊 Sampling-Based Monitoring

The new sampling feature allows you to monitor high-volume agents cost-effectively by only reporting a percentage of interactions.

### Why Use Sampling?

- **Cost Control**: 95% reduction in API calls with 5% sampling
- **Privacy**: Not every conversation is analyzed
- **Performance**: Reduced latency and bandwidth
- **Scalability**: Handle more agents with less load
- **Quality**: Still get meaningful performance insights

### Sampling Configuration

```python
# Quick setup with 5% sampling
agent = create_sampled_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    sampling_rate=0.05  # 5% sampling
)

# Advanced configuration
agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    enable_sampling=True,
    sampling_config={
        "strategy": "percentage",
        "rate": 0.1,  # 10% sampling
        "batch_size": 50,  # Send batch every 50 samples
        "max_daily_samples": 500,
        "performance_threshold": 70,  # Sample more when performance is poor
        "sampling_window": "daily"
    }
)
```

### Sampling Statistics

```python
# Get sampling statistics
stats = agent.get_sampling_stats()
print(f"Daily samples: {stats['daily_sample_count']}")
print(f"Batch queue size: {stats['batch_queue_size']}")
print(f"Sampling rate: {stats['sampling_rate']}")
```

### Use Cases

| Use Case | Recommended Sampling | Benefits |
|----------|-------------------|----------|
| **Development/Testing** | Full monitoring (100%) | Complete visibility |
| **Production (Low Volume)** | 10-20% sampling | Cost control |
| **Production (High Volume)** | 1-5% sampling | Maximum efficiency |
| **Critical Agents** | Full monitoring | Quality assurance |

## 🩹 Self-Healing Process

The SDK implements a robust two-step self-healing process to prevent errors and ensure reliable improvements:

### Step 1: Performance Scan
- Automatically detects when agents need healing (status: warning/critical)
- Triggers a self-healing scan to flag underperforming agents
- Validates that agents meet healing criteria before proceeding

### Step 2: Prompt Improvement
- Only flagged agents can be healed (prevents 400 errors)
- Generates improved system prompts using Claude
- Applies changes automatically or suggests improvements

### Error Prevention
- **No more 400 errors**: SDK handles all validation automatically
- **Smart detection**: Only heals agents that actually need improvement
- **Graceful fallback**: Continues working even if healing fails

```python
# The SDK handles everything automatically:
monitored_agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model
)

# Self-healing happens in the background:
# 1. Detects poor performance
# 2. Triggers scan to flag agent
# 3. Applies prompt improvements
# 4. No errors or manual intervention needed!
```

## 📚 API Reference

### Simple Integration

```python
from enable_ai_sdk.agent_monitor import create_monitored_agent, create_sampled_agent

# Your existing AI model function
def your_ai_model(prompt: str) -> str:
    return "Response from your AI model"

# Full monitoring (default)
monitored_agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model
)

# Sampling-based monitoring (new!)
sampled_agent = create_sampled_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    sampling_rate=0.05  # 5% sampling
)

# Use them normally
response1 = monitored_agent.generate_response("Hello!")
response2 = sampled_agent.generate_response("Hello!")
```

### Advanced Integration

```python
from enable_ai_sdk.agent_monitor import AgentMonitor
import openai

class MonitoredCustomerSupportAgent(AgentMonitor):
    def _call_ai_model(self, prompt: str, **kwargs) -> str:
        # Your AI model integration here
        client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = client.chat.completions.create(
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
from enable_ai_sdk.agent_monitor import create_monitored_agent, create_sampled_agent

# Your AI model function
def my_ai_model(prompt: str) -> str:
    return "Response from your AI model"

# Create monitored agent (full monitoring)
agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=my_ai_model
)

# Or use sampling for cost-effective production
sampled_agent = create_sampled_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=my_ai_model,
    sampling_rate=0.05  # 5% sampling
)

def lambda_handler(event, context):
    user_input = event['body']['message']
    response = agent.generate_response(user_input)  # Automatically monitored!
    return {'response': response}
```

### Sampling Statistics and Monitoring

```python
# Get sampling statistics
stats = sampled_agent.get_sampling_stats()
print(f"Daily samples: {stats['daily_sample_count']}")
print(f"Batch queue size: {stats['batch_queue_size']}")
print(f"Sampling rate: {stats['sampling_rate']}")
print(f"Max daily samples: {stats['max_daily_samples']}")

# Check if sampling is enabled
if sampled_agent.enable_sampling:
    print("✅ Sampling is enabled")
    print(f"📊 Current batch queue: {stats['batch_queue_size']} interactions")
else:
    print("📊 Full monitoring mode")
```

## 📊 What Gets Tracked Automatically

### Performance Metrics
- **Quality Score**: 1-100 rating from Claude
- **Response Time**: How long your agent takes
- **Issue Categories**: Hallucination, tone, format, etc.
- **Usage Patterns**: When and how your agent is used
- **Sampling Statistics**: Daily counts, batch queues, sampling rates

### Cost Impact Comparison

| Monitoring Type | API Calls | Cost Reduction | Use Case |
|----------------|-----------|----------------|----------|
| **Full Monitoring** | 1 per interaction | 0% | Development, testing, critical agents |
| **10% Sampling** | 1 per 10 interactions | 90% | Production (low volume) |
| **5% Sampling** | 1 per 20 interactions | 95% | Production (high volume) |
| **1% Sampling** | 1 per 100 interactions | 99% | High-volume production |

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

### Basic Setup (Full Monitoring)
```python
agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model
)
```

### Sampling-Based Monitoring
```python
# Quick sampling setup
agent = create_sampled_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    sampling_rate=0.05  # 5% sampling
)

# Advanced sampling configuration
agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    enable_sampling=True,
    sampling_config={
        "strategy": "percentage",
        "rate": 0.1,  # 10% sampling
        "batch_size": 50,  # Send batch every 50 samples
        "max_daily_samples": 500,
        "performance_threshold": 70,  # Sample more when performance is poor
        "sampling_window": "daily"
    }
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
    report_async=True,      # Report performance asynchronously
    enable_sampling=True,   # Enable sampling-based monitoring
    sampling_config={...}   # Custom sampling configuration
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
3. **Sampling Options**: Choose between full monitoring or cost-effective sampling
4. **Self-Healing**: Automatic improvements when needed
5. **Real-time Insights**: Performance analytics and recommendations

### For Agent Operators
1. **Zero Manual Work**: Everything is automatic
2. **Cost Control**: 95% reduction in API calls with sampling
3. **Proactive Alerts**: Get notified when agents need attention
4. **Continuous Improvement**: Agents get better over time
5. **Comprehensive Analytics**: Detailed performance tracking
6. **Production Ready**: Sampling perfect for high-volume deployments

### For High-Volume Production
1. **Cost Efficiency**: Only pay for sampled interactions
2. **Privacy**: Not every conversation analyzed
3. **Performance**: Reduced latency and bandwidth
4. **Scalability**: Handle more agents with less load
5. **Quality**: Still get meaningful performance insights

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
# ✅ Performance reported (or sampled based on configuration)
# ✅ Quality evaluated
# ✅ Self-healing triggered if needed
# ✅ Prompt improvements applied
# ✅ Batch processing for efficiency (if sampling enabled)
```

### 4. Choose Your Monitoring Strategy

```python
# For development/testing - full monitoring
dev_agent = create_monitored_agent(
    agent_id="dev-agent",
    api_key="your-api-key",
    ai_model_func=your_ai_model
)

# For production (low volume) - 10% sampling
prod_low_agent = create_sampled_agent(
    agent_id="prod-low-agent",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    sampling_rate=0.1  # 10% sampling
)

# For production (high volume) - 5% sampling
prod_high_agent = create_sampled_agent(
    agent_id="prod-high-agent",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    sampling_rate=0.05  # 5% sampling
)

# For critical agents - full monitoring
critical_agent = create_monitored_agent(
    agent_id="critical-agent",
    api_key="your-api-key",
    ai_model_func=your_ai_model
)
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
2. **Get your API key**: Sign up at [WeEnable.AI](https://www.weenable.ai)
3. **Choose your monitoring strategy**:
   - **Full monitoring**: For development and critical agents
   - **Sampling**: For cost-effective production deployment
4. **Wrap your agent**: Use the drop-in integration above
5. **Start monitoring**: Everything is automatic!

## 🔄 Migration Guide

### From Full Monitoring to Sampling

```python
# Old code (still works!)
agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model
)

# New code with sampling (optional)
sampled_agent = create_sampled_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    sampling_rate=0.05  # 5% sampling
)

# Or enable sampling on existing agent
agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    enable_sampling=True,
    sampling_config={
        "rate": 0.05,
        "batch_size": 100,
        "max_daily_samples": 1000
    }
)
```

### Backward Compatibility

- ✅ **Existing code works unchanged**
- ✅ **No breaking changes**
- ✅ **Sampling is optional**
- ✅ **Easy migration path**

## 📞 Support

- **Self-Healing Walkthrough**: [SELF_HEALING_WALKTHROUGH.md](SELF_HEALING_WALKTHROUGH.md) - Complete guide to self-healing
- **Documentation**: [https://docs.enable.ai](https://docs.enable.ai)
- **GitHub Issues**: [https://github.com/enable-ai/sdk/issues](https://github.com/enable-ai/sdk/issues)
- **Email Support**: support@enable.ai

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 