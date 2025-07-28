"""
EnableAI Agentic AI Platform SDK

A comprehensive Python SDK for the EnableAI Agentic AI Platform.
Provides easy-to-use interfaces for agent management, analytics, self-healing, and webhooks.

Usage:
    from enable_ai_sdk import EnableAIClient
    
    # Initialize client
    client = EnableAIClient(api_key="your-api-key", base_url="https://your-backend.com")
    
    # Register an agent
    agent = client.agents.register(
        name="My Agent",
        agent_type="customer-support",
        llm="claude-3-5-sonnet-20241022"
    )
    
    # Get agent analytics
    analytics = client.analytics.get_agent_insights(agent.id)
    
    # Submit feedback
    feedback = client.analytics.submit_feedback(
        prompt="What is your return policy?",
        response="Our return policy allows returns within 30 days.",
        tool="CustomerFeedback",
        use_case="Customer Support",
        agent_id=agent.id
    )
    
    # Trigger self-healing scan
    scan_results = client.self_healing.scan()
    
    # Manage webhooks
    webhooks = client.webhooks.list()
    
    # Use agent monitoring (drop-in solution)
    from enable_ai_sdk import create_monitored_agent
    
    def my_ai_function(prompt):
        # Your AI logic here
        return "AI response"
    
    monitored_agent = create_monitored_agent(
        agent_id=agent.id,
        api_key="your-api-key",
        ai_model_func=my_ai_function,
        base_url="https://your-backend.com"
    )
    
    # Use the monitored agent
    response = monitored_agent.generate_response("What is your return policy?")
"""

from .client import (
    EnableAIClient,
    create_client,
    quick_agent_register,
    quick_feedback_submit
)

from .models import (
    Agent,
    AnalyticsResult,
    FeedbackResult
)

from .exceptions import (
    EnableAIError,
    AuthenticationError,
    ValidationError,
    RateLimitError
)

from .agent_monitor import (
    AgentMonitor,
    SimpleAgentMonitor,
    create_monitored_agent
)

__version__ = "1.0.0"
__author__ = "EnableAI Team"
__email__ = "support@enable.ai"

__all__ = [
    # Main client
    "EnableAIClient",
    "create_client",
    "quick_agent_register",
    "quick_feedback_submit",
    
    # Data models
    "Agent",
    "AnalyticsResult", 
    "FeedbackResult",
    
    # Exceptions
    "EnableAIError",
    "AuthenticationError",
    "ValidationError",
    "RateLimitError",
    
    # Agent monitoring
    "AgentMonitor",
    "SimpleAgentMonitor", 
    "create_monitored_agent",
] 