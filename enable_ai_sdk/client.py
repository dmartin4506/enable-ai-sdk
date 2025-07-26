"""
Main client for EnableAI Agentic AI Platform
"""

import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

from .models import Agent, AnalyticsResult, FeedbackResult
from .exceptions import EnableAIError, AuthenticationError, ValidationError, RateLimitError


class EnableAIClient:
    """Main client for EnableAI Agentic AI Platform"""
    
    def __init__(self, api_key: str, base_url: str = "http://localhost:5001"):
        """
        Initialize the client
        
        Args:
            api_key: Your API key
            base_url: Base URL of the EnableAI backend
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        
        # Initialize session with headers
        self.session = requests.Session()
        self.session.headers.update({
            'X-Api-Key': api_key,
            'Content-Type': 'application/json'
        })
        
        # Initialize managers
        self.agents = AgentManager(self)
        self.analytics = AnalyticsManager(self)
        self.webhooks = WebhookManager(self)
        self.self_healing = SelfHealingManager(self)
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make an authenticated request to the API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests
            
        Returns:
            API response as dictionary
            
        Raises:
            AuthenticationError: If authentication fails
            ValidationError: If request validation fails
            RateLimitError: If rate limits are exceeded
            EnableAIError: For other API errors
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Handle different response types
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key or authentication failed")
            elif response.status_code == 400:
                try:
                    error_data = response.json()
                    raise ValidationError(f"Validation error: {error_data.get('error', 'Unknown error')}")
                except:
                    raise ValidationError(f"Validation error: {response.text}")
            elif response.status_code == 402:
                try:
                    error_data = response.json()
                    raise EnableAIError(f"Payment required: {error_data.get('error', 'Unknown error')}")
                except:
                    raise EnableAIError(f"Payment required: {response.text}")
            elif response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            elif response.status_code >= 400:
                try:
                    error_data = response.json()
                    raise EnableAIError(f"API error {response.status_code}: {error_data.get('error', 'Unknown error')}")
                except:
                    raise EnableAIError(f"API error {response.status_code}: {response.text}")
            
            # Handle empty responses
            if response.status_code == 204 or not response.text:
                return {}
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise EnableAIError(f"Network error: {str(e)}")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check API health
        
        Returns:
            Health status
        """
        return self._make_request('GET', '/health')


class AgentManager:
    """Manage AI agents"""
    
    def __init__(self, client: EnableAIClient):
        self.client = client
    
    def register(self, name: str, agent_type: str, llm: str, 
                 description: Optional[str] = None, 
                 system_prompt: Optional[str] = None) -> Agent:
        """
        Register a new agent
        
        Args:
            name: Agent name
            agent_type: Type of agent (customer-support, sales-assistant, etc.)
            llm: LLM model to use
            description: Optional agent description
            system_prompt: Optional system prompt
            
        Returns:
            Registered agent
        """
        data = {
            'agent_name': name,
            'agent_type': agent_type,
            'llm': llm
        }
        
        if description:
            data['description'] = description
        if system_prompt:
            data['system_prompt'] = system_prompt
        
        response = self.client._make_request('POST', '/agent/register', json=data)
        
        return Agent(
            id=response['agent_id'],
            name=response.get('agent_name', name),  # Fallback to input name if not in response
            description=description,
            agent_type=agent_type,
            llm=llm,
            system_prompt=system_prompt,
            created_at=response.get('created_at'),
            customer_id=response.get('customer_id'),
            user_id=response.get('user_id'),
            healing_recommended=False
        )
    
    def list(self) -> List[Agent]:
        """
        List all agents
        
        Returns:
            List of agents
        """
        response = self.client._make_request('GET', '/user/agents')
        
        agents = []
        if isinstance(response, list):
            for agent_data in response:
                if isinstance(agent_data, dict):
                    agents.append(Agent(
                        id=agent_data.get('agent_id', ''),
                        name=agent_data.get('agent_name', ''),
                        description=agent_data.get('description'),
                        agent_type=agent_data.get('agent_type', ''),
                        llm=agent_data.get('llm', ''),
                        system_prompt=agent_data.get('system_prompt'),
                        created_at=agent_data.get('created_at'),
                        customer_id=agent_data.get('customer_id'),
                        user_id=agent_data.get('user_id'),
                        healing_recommended=agent_data.get('healing_recommended', False)
                    ))
        
        return agents
    
    def get(self, agent_id: str) -> Agent:
        """
        Get agent by ID
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Agent data
        """
        # Note: Individual agent GET endpoint doesn't exist
        # This method is kept for API compatibility but will raise an error
        raise EnableAIError("Individual agent retrieval not supported. Use list() to get all agents.")
    
    def update(self, agent_id: str, **kwargs) -> Agent:
        """
        Update agent
        
        Args:
            agent_id: Agent ID
            **kwargs: Fields to update
            
        Returns:
            Updated agent
        """
        response = self.client._make_request('PUT', f'/agent/{agent_id}', json=kwargs)
        
        return Agent(
            id=response['agent_id'],
            name=response['agent_name'],
            description=response.get('description'),
            agent_type=response['agent_type'],
            llm=response['llm'],
            system_prompt=response.get('system_prompt'),
            created_at=response.get('created_at'),
            customer_id=response.get('customer_id'),
            user_id=response.get('user_id'),
            healing_recommended=response.get('healing_recommended', False)
        )
    
    def delete(self, agent_id: str) -> bool:
        """
        Delete agent
        
        Args:
            agent_id: Agent ID
            
        Returns:
            True if successful
        """
        self.client._make_request('DELETE', f'/agent/{agent_id}')
        return True
    
    def get_prompt_history(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Get prompt revision history for an agent
        
        Args:
            agent_id: Agent ID
            
        Returns:
            List of prompt revisions
        """
        response = self.client._make_request('GET', f'/agent/{agent_id}/prompt/history')
        if isinstance(response, list):
            return response
        return []


class AnalyticsManager:
    """Manage analytics and feedback"""
    
    def __init__(self, client: EnableAIClient):
        self.client = client
    
    def get_agent_insights(self, agent_id: str, start_date: Optional[str] = None,
                          end_date: Optional[str] = None) -> AnalyticsResult:
        """
        Get agent insights and analytics
        
        Args:
            agent_id: Agent ID
            start_date: Optional start date (YYYY-MM-DD)
            end_date: Optional end date (YYYY-MM-DD)
            
        Returns:
            Agent insights
        """
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        
        params['agent_id'] = agent_id
        response = self.client._make_request('GET', '/agent/feedback/insights', params=params)
        
        return AnalyticsResult(
            agent_id=response['agent_id'],
            agent_name=response['agent_name'],
            recent_issues=response.get('recent_issues', []),
            score_trend=response.get('score_trend', 'stable'),
            feedback_count=response.get('feedback_count', 0),
            average_score=response.get('average_score', 0.0),
            suggested_actions=response.get('suggested_actions', []),
            last_updated=response.get('last_updated', '')
        )
    
    def get_agent_analytics(self, agent_id: str, start_date: Optional[str] = None,
                           end_date: Optional[str] = None, tool: Optional[str] = None,
                           use_case: Optional[str] = None) -> Dict[str, Any]:
        """
        Get detailed agent analytics
        
        Args:
            agent_id: Agent ID
            start_date: Optional start date (YYYY-MM-DD)
            end_date: Optional end date (YYYY-MM-DD)
            tool: Optional tool filter
            use_case: Optional use case filter
            
        Returns:
            Detailed analytics data
        """
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        if tool:
            params['tool'] = tool
        if use_case:
            params['use_case'] = use_case
        
        params['agent_id'] = agent_id
        return self.client._make_request('GET', '/feedback/agent/analytics', params=params)
    
    def submit_feedback(self, prompt: str, response: str, tool: str,
                       use_case: str, user_id: Optional[str] = None,
                       agent_id: Optional[str] = None) -> FeedbackResult:
        """
        Submit feedback for evaluation
        
        Args:
            prompt: User prompt
            response: AI response
            tool: Tool used (e.g., CustomerFeedback)
            use_case: Use case (e.g., Customer Support)
            user_id: Optional user ID
            agent_id: Optional agent ID
            
        Returns:
            Feedback evaluation result
        """
        data = {
            'prompt': prompt,
            'response': response,
            'tool': tool,
            'use_case': use_case
        }
        
        if user_id:
            data['user_id'] = user_id
        if agent_id:
            data['agent_id'] = agent_id
        
        response_data = self.client._make_request('POST', '/feedback/customer', json=data)
        
        return FeedbackResult(
            score=response_data['score'],
            issue=response_data['issue'],
            feedback_id=response_data.get('feedback_log_id', 'unknown'),
            timestamp=response_data.get('timestamp', datetime.now().isoformat())
        )


class WebhookManager:
    """Manage webhooks"""
    
    def __init__(self, client: EnableAIClient):
        self.client = client
    
    def list(self) -> List[Dict[str, Any]]:
        """
        List all webhooks
        
        Returns:
            List of webhooks
        """
        response = self.client._make_request('GET', '/user/webhooks')
        if isinstance(response, list):
            return response
        return []
    
    def create(self, name: str, url: str, events: Optional[List[str]] = None,
               headers: Optional[Dict[str, str]] = None, retry_count: int = 3,
               timeout: int = 10, is_active: bool = True) -> Dict[str, Any]:
        """
        Create a new webhook
        
        Args:
            name: Webhook name
            url: Webhook URL
            events: List of events to listen for
            headers: Optional headers
            retry_count: Number of retries
            timeout: Timeout in seconds
            is_active: Whether webhook is active
            
        Returns:
            Created webhook
        """
        data = {
            'name': name,
            'url': url,
            'retry_count': retry_count,
            'timeout': timeout,
            'is_active': is_active
        }
        
        if events:
            data['events'] = events
        if headers:
            data['headers'] = headers
        
        return self.client._make_request('POST', '/user/webhooks', json=data)
    
    def update(self, webhook_id: int, **kwargs) -> Dict[str, Any]:
        """
        Update webhook
        
        Args:
            webhook_id: Webhook ID
            **kwargs: Fields to update
            
        Returns:
            Updated webhook
        """
        return self.client._make_request('PUT', f'/user/webhooks/{webhook_id}', json=kwargs)
    
    def delete(self, webhook_id: int) -> bool:
        """
        Delete webhook
        
        Args:
            webhook_id: Webhook ID
            
        Returns:
            True if successful
        """
        self.client._make_request('DELETE', f'/user/webhooks/{webhook_id}')
        return True
    
    def test(self, webhook_id: int) -> Dict[str, Any]:
        """
        Test webhook
        
        Args:
            webhook_id: Webhook ID
            
        Returns:
            Test result
        """
        return self.client._make_request('POST', f'/user/webhooks/{webhook_id}/test')
    
    def get_history(self, webhook_id: int) -> List[Dict[str, Any]]:
        """
        Get webhook delivery history
        
        Args:
            webhook_id: Webhook ID
            
        Returns:
            Delivery history
        """
        response = self.client._make_request('GET', f'/user/webhooks/{webhook_id}/history')
        if isinstance(response, list):
            return response
        return []


class SelfHealingManager:
    """Manage agent self-healing"""
    
    def __init__(self, client: EnableAIClient):
        self.client = client
    
    def scan(self, customer_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Trigger self-healing scan
        
        Args:
            customer_id: Optional customer ID to scan
            
        Returns:
            Scan results
        """
        data = {}
        if customer_id:
            data['customer_id'] = customer_id
        
        return self.client._make_request('POST', '/self-healing/scan', json=data)
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """
        Get agent healing status
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Agent status
        """
        return self.client._make_request('GET', f'/self-healing/agent/{agent_id}/status')
    
    def heal_agent(self, agent_id: str, strategy: str = 'auto',
                   start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Trigger agent healing
        
        Args:
            agent_id: Agent ID
            strategy: Healing strategy (auto, manual)
            start_date: Optional start date for analysis
            end_date: Optional end date for analysis
            
        Returns:
            Healing result
        """
        data = {
            'strategy': strategy
        }
        
        if start_date:
            data['start_date'] = start_date
        if end_date:
            data['end_date'] = end_date
        
        return self.client._make_request('POST', f'/agent/self_heal', json=data)


# Convenience Functions
def create_client(api_key: str, base_url: str = "http://localhost:5001") -> EnableAIClient:
    """
    Create an EnableAI client
    
    Args:
        api_key: Your API key
        base_url: Base URL of the EnableAI backend
        
    Returns:
        EnableAIClient instance
    """
    return EnableAIClient(api_key, base_url)


def quick_agent_register(api_key: str, name: str, agent_type: str = "customer-support",
                        llm: str = "claude-3-5-sonnet-20241022", base_url: str = "http://localhost:5001") -> Agent:
    """
    Quick agent registration
    
    Args:
        api_key: Your API key
        name: Agent name
        agent_type: Agent type
        llm: LLM model
        base_url: Base URL
        
    Returns:
        Registered agent
    """
    client = create_client(api_key, base_url)
    return client.agents.register(name=name, agent_type=agent_type, llm=llm)


def quick_feedback_submit(api_key: str, prompt: str, response: str, tool: str = "CustomerFeedback",
                         use_case: str = "General", base_url: str = "http://localhost:5001") -> FeedbackResult:
    """
    Quick feedback submission
    
    Args:
        api_key: Your API key
        prompt: User prompt
        response: AI response
        tool: Tool used
        use_case: Use case
        base_url: Base URL
        
    Returns:
        Feedback result
    """
    client = create_client(api_key, base_url)
    return client.analytics.submit_feedback(
        prompt=prompt,
        response=response,
        tool=tool,
        use_case=use_case
    ) 