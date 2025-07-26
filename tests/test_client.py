"""
Tests for the EnableAI SDK client
"""

import pytest
from unittest.mock import Mock, patch
from enable_ai_sdk import EnableAIClient, AuthenticationError, ValidationError, RateLimitError


class TestEnableAIClient:
    """Test cases for EnableAIClient"""
    
    def test_client_initialization(self):
        """Test client initialization"""
        client = EnableAIClient(api_key="test-key", base_url="https://test.com")
        assert client.api_key == "test-key"
        assert client.base_url == "https://test.com"
        assert "X-Api-Key" in client.session.headers
        assert client.session.headers["X-Api-Key"] == "test-key"
    
    def test_client_initialization_default_url(self):
        """Test client initialization with default URL"""
        client = EnableAIClient(api_key="test-key")
        assert client.base_url == "http://localhost:5001"
    
    def test_health_check(self):
        """Test health check method"""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"status": "healthy"}
            mock_request.return_value = mock_response
            
            client = EnableAIClient(api_key="test-key")
            result = client.health_check()
            
            assert result == {"status": "healthy"}
            mock_request.assert_called_once_with("GET", "http://localhost:5001/health")
    
    def test_authentication_error(self):
        """Test authentication error handling"""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_request.return_value = mock_response
            
            client = EnableAIClient(api_key="invalid-key")
            
            with pytest.raises(AuthenticationError):
                client.health_check()
    
    def test_validation_error(self):
        """Test validation error handling"""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 400
            mock_response.json.return_value = {"error": "Invalid request"}
            mock_request.return_value = mock_response
            
            client = EnableAIClient(api_key="test-key")
            
            with pytest.raises(ValidationError):
                client.health_check()
    
    def test_rate_limit_error(self):
        """Test rate limit error handling"""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 429
            mock_request.return_value = mock_response
            
            client = EnableAIClient(api_key="test-key")
            
            with pytest.raises(RateLimitError):
                client.health_check()


class TestAgentManager:
    """Test cases for AgentManager"""
    
    def test_agent_manager_initialization(self):
        """Test agent manager initialization"""
        client = EnableAIClient(api_key="test-key")
        assert hasattr(client.agents, '_client')
        assert client.agents._client == client
    
    def test_register_agent(self):
        """Test agent registration"""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "id": "agent-123",
                "name": "Test Agent",
                "agent_type": "customer-support",
                "llm": "claude-3-5-sonnet-20241022",
                "description": "A test agent",
                "system_prompt": None,
                "created_at": "2024-01-01T00:00:00Z",
                "customer_id": None,
                "user_id": None,
                "healing_recommended": False
            }
            mock_request.return_value = mock_response
            
            client = EnableAIClient(api_key="test-key")
            agent = client.agents.register(
                name="Test Agent",
                agent_type="customer-support",
                llm="claude-3-5-sonnet-20241022",
                description="A test agent"
            )
            
            assert agent.id == "agent-123"
            assert agent.name == "Test Agent"
            assert agent.agent_type == "customer-support"
            assert agent.llm == "claude-3-5-sonnet-20241022"
            assert agent.description == "A test agent"


class TestAnalyticsManager:
    """Test cases for AnalyticsManager"""
    
    def test_analytics_manager_initialization(self):
        """Test analytics manager initialization"""
        client = EnableAIClient(api_key="test-key")
        assert hasattr(client.analytics, '_client')
        assert client.analytics._client == client
    
    def test_submit_feedback(self):
        """Test feedback submission"""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "score": 85.0,
                "issue": "None",
                "feedback_id": "feedback-123",
                "timestamp": "2024-01-01T00:00:00Z"
            }
            mock_request.return_value = mock_response
            
            client = EnableAIClient(api_key="test-key")
            feedback = client.analytics.submit_feedback(
                prompt="What is your return policy?",
                response="Our return policy allows returns within 30 days.",
                tool="CustomerFeedback",
                use_case="Customer Support"
            )
            
            assert feedback.score == 85.0
            assert feedback.issue == "None"
            assert feedback.feedback_id == "feedback-123"


class TestWebhookManager:
    """Test cases for WebhookManager"""
    
    def test_webhook_manager_initialization(self):
        """Test webhook manager initialization"""
        client = EnableAIClient(api_key="test-key")
        assert hasattr(client.webhooks, '_client')
        assert client.webhooks._client == client
    
    def test_list_webhooks(self):
        """Test webhook listing"""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = [
                {
                    "id": 1,
                    "name": "Test Webhook",
                    "url": "https://test.com/webhook",
                    "events": ["feedback_submitted"],
                    "is_active": True
                }
            ]
            mock_request.return_value = mock_response
            
            client = EnableAIClient(api_key="test-key")
            webhooks = client.webhooks.list()
            
            assert len(webhooks) == 1
            assert webhooks[0]["name"] == "Test Webhook"
            assert webhooks[0]["url"] == "https://test.com/webhook"


class TestSelfHealingManager:
    """Test cases for SelfHealingManager"""
    
    def test_self_healing_manager_initialization(self):
        """Test self-healing manager initialization"""
        client = EnableAIClient(api_key="test-key")
        assert hasattr(client.self_healing, '_client')
        assert client.self_healing._client == client
    
    def test_scan(self):
        """Test self-healing scan"""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "total_agents_scanned": 5,
                "agents_flagged": [
                    {"id": "agent-1", "name": "Agent 1", "issues": ["hallucination"]}
                ],
                "scan_timestamp": "2024-01-01T00:00:00Z"
            }
            mock_request.return_value = mock_response
            
            client = EnableAIClient(api_key="test-key")
            scan_results = client.self_healing.scan()
            
            assert scan_results["total_agents_scanned"] == 5
            assert len(scan_results["agents_flagged"]) == 1
            assert scan_results["agents_flagged"][0]["id"] == "agent-1" 