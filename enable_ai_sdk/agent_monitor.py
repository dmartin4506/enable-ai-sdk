#!/usr/bin/env python3
"""
EnableAI Agent Monitor - Drop-in SDK for Agent Performance Monitoring

This module provides automatic performance monitoring and self-healing capabilities
for any AI agent. Simply import and wrap your agent to get:

- Automatic performance reporting
- Quality evaluation using Claude
- Self-healing with prompt improvements
- Performance analytics and insights

Usage:
    from enable_ai_sdk.agent_monitor import AgentMonitor
    
    # Wrap your existing agent
    monitored_agent = AgentMonitor(
        agent_id="your-agent-id",
        api_key="your-api-key",
        base_url="https://your-backend.com"
    )
    
    # Use it like a normal agent
    response = monitored_agent.generate_response("What is your return policy?")
    
    # The SDK automatically:
    # - Reports the interaction for evaluation
    # - Gets quality scores and insights
    # - Triggers self-healing if needed
    # - Applies prompt improvements automatically
"""

import requests
import json
import time
import threading
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentMonitor:
    """
    Drop-in agent monitor that automatically reports performance and handles self-healing
    """
    
    def __init__(self, 
                 agent_id: str,
                 api_key: str,
                 base_url: str = "http://localhost:5001",
                 auto_healing: bool = True,
                 report_async: bool = True,
                 system_prompt: Optional[str] = None):
        """
        Initialize the agent monitor
        
        Args:
            agent_id: Your agent's ID from EnableAI platform
            api_key: Your EnableAI API key
            base_url: EnableAI backend URL
            auto_healing: Whether to automatically apply prompt improvements
            report_async: Whether to report performance asynchronously
            system_prompt: Current system prompt (will be updated by self-healing)
        """
        self.agent_id = agent_id
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.auto_healing = auto_healing
        self.report_async = report_async
        self.system_prompt = system_prompt
        self.session = requests.Session()
        self.session.headers.update({
            'x-api-key': api_key,
            'Content-Type': 'application/json'
        })
        
        # Performance tracking
        self.interaction_count = 0
        self.average_score = 0.0
        self.last_health_check = None
        
        # Self-healing state
        self.healing_recommended = False
        self.last_healing_check = None
        
        # Background monitoring
        self.monitoring_thread = None
        self._stop_monitoring = False
        
        logger.info(f"AgentMonitor initialized for agent {agent_id}")
        
        # Start background monitoring if async reporting is enabled
        if self.report_async:
            self._start_background_monitoring()
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Generate a response and automatically report performance
        
        This is the main method your agent should call instead of directly
        calling your AI model. It automatically handles performance reporting
        and self-healing.
        
        Args:
            prompt: User prompt
            **kwargs: Additional arguments for your AI model
            
        Returns:
            Generated response
        """
        start_time = time.time()
        
        # Generate response using your AI model
        response = self._call_ai_model(prompt, **kwargs)
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        # Report performance
        if self.report_async:
            # Queue for async reporting
            self._queue_performance_report(prompt, response, response_time_ms)
        else:
            # Report immediately
            self._report_performance(prompt, response, response_time_ms)
        
        # Check for self-healing periodically
        self._check_self_healing()
        
        return response
    
    def _call_ai_model(self, prompt: str, **kwargs) -> str:
        """
        Call your AI model to generate a response
        
        Override this method to integrate with your specific AI model
        """
        # Default implementation - override in your agent
        raise NotImplementedError(
            "Override _call_ai_model() to integrate with your AI model. "
            "Example:\n"
            "def _call_ai_model(self, prompt: str, **kwargs) -> str:\n"
            "    response = your_ai_model.generate(prompt)\n"
            "    return response"
        )
    
    def _report_performance(self, prompt: str, response: str, response_time_ms: int) -> bool:
        """Report performance to EnableAI platform"""
        try:
            payload = {
                "agent_id": self.agent_id,
                "prompt": prompt,
                "response": response,
                "response_time_ms": response_time_ms,
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "source": "agent-monitor-sdk",
                    "interaction_count": self.interaction_count,
                    "average_score": self.average_score
                }
            }
            
            api_response = self.session.post(
                f"{self.base_url}/agent/external/performance",
                json=payload,
                timeout=10
            )
            
            if api_response.status_code == 201:
                result = api_response.json()
                self.interaction_count += 1
                
                # Update average score
                if result.get('quality_score'):
                    score = result['quality_score']
                    if self.average_score == 0:
                        self.average_score = score
                    else:
                        self.average_score = (self.average_score + score) / 2
                
                logger.info(f"Performance reported - Score: {result.get('quality_score', 'N/A')}, "
                          f"Issue: {result.get('main_issue', 'None')}")
                return True
            else:
                logger.error(f"Failed to report performance: {api_response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error reporting performance: {e}")
            return False
    
    def _queue_performance_report(self, prompt: str, response: str, response_time_ms: int):
        """Queue performance report for async processing"""
        # Simple async implementation - in production, use a proper queue
        def report_async():
            self._report_performance(prompt, response, response_time_ms)
        
        thread = threading.Thread(target=report_async)
        thread.daemon = True
        thread.start()
    
    def _check_self_healing(self):
        """Check if agent needs self-healing"""
        # Check every 10 interactions or every 5 minutes
        if (self.interaction_count % 10 == 0 or 
            (self.last_healing_check and 
             time.time() - self.last_healing_check > 300)):
            
            try:
                health_response = self.session.get(
                    f"{self.base_url}/agent/external/health?agent_id={self.agent_id}",
                    timeout=10
                )
                
                if health_response.status_code == 200:
                    health_data = health_response.json()
                    
                    if health_data.get('status') in ['warning', 'critical']:
                        logger.warning(f"Agent needs healing - Status: {health_data['status']}")
                        self._trigger_self_healing()
                
                self.last_healing_check = time.time()
                
            except Exception as e:
                logger.error(f"Error checking self-healing: {e}")
    
    def _trigger_self_healing(self):
        """Trigger self-healing for the agent"""
        try:
            healing_response = self.session.post(
                f"{self.base_url}/agent/self_heal",
                json={
                    "agent_id": self.agent_id,
                    "strategy": "auto" if self.auto_healing else "suggest"
                },
                timeout=30
            )
            
            if healing_response.status_code == 200:
                result = healing_response.json()
                logger.info(f"Self-healing triggered: {result.get('message', 'Unknown')}")
                
                if result.get('prompt_updated') and self.auto_healing:
                    # Update the system prompt
                    new_prompt = result.get('suggested_prompt')
                    if new_prompt:
                        self.system_prompt = new_prompt
                        logger.info("System prompt updated via self-healing")
                
                return True
            else:
                logger.error(f"Failed to trigger self-healing: {healing_response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error triggering self-healing: {e}")
            return False
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get current health status of the agent"""
        try:
            response = self.session.get(
                f"{self.base_url}/agent/external/health?agent_id={self.agent_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get health status: {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"Error getting health status: {e}")
            return {}
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics for the agent"""
        try:
            response = self.session.get(
                f"{self.base_url}/feedback/agent/analytics?agent_id={self.agent_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get analytics: {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"Error getting analytics: {e}")
            return {}
    
    def get_insights(self) -> Dict[str, Any]:
        """Get AI-generated insights for the agent"""
        try:
            response = self.session.get(
                f"{self.base_url}/agent/feedback/insights?agent_id={self.agent_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get insights: {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"Error getting insights: {e}")
            return {}
    
    def _start_background_monitoring(self):
        """Start background monitoring thread"""
        def monitor_loop():
            while not self._stop_monitoring:
                try:
                    # Check health every 5 minutes
                    self._check_self_healing()
                    time.sleep(300)  # 5 minutes
                except Exception as e:
                    logger.error(f"Error in background monitoring: {e}")
                    time.sleep(60)  # Wait 1 minute on error
        
        self.monitoring_thread = threading.Thread(target=monitor_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        logger.info("Background monitoring started")
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self._stop_monitoring = True
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Background monitoring stopped")
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.stop_monitoring()


class SimpleAgentMonitor(AgentMonitor):
    """
    Simple agent monitor with basic AI model integration
    """
    
    def __init__(self, 
                 agent_id: str,
                 api_key: str,
                 ai_model_func: Callable[[str], str],
                 base_url: str = "http://localhost:5001",
                 **kwargs):
        """
        Initialize with a simple AI model function
        
        Args:
            agent_id: Your agent's ID
            api_key: Your EnableAI API key
            ai_model_func: Function that takes a prompt and returns a response
            base_url: EnableAI backend URL
            **kwargs: Additional arguments for AgentMonitor
        """
        super().__init__(agent_id, api_key, base_url, **kwargs)
        self.ai_model_func = ai_model_func
    
    def _call_ai_model(self, prompt: str, **kwargs) -> str:
        """Call the provided AI model function"""
        return self.ai_model_func(prompt)


# Convenience function for quick setup
def create_monitored_agent(agent_id: str, 
                          api_key: str, 
                          ai_model_func: Callable[[str], str],
                          base_url: str = "http://localhost:5001",
                          **kwargs) -> SimpleAgentMonitor:
    """
    Create a monitored agent with minimal setup
    
    Args:
        agent_id: Your agent's ID
        api_key: Your EnableAI API key
        ai_model_func: Function that takes a prompt and returns a response
        base_url: EnableAI backend URL
        **kwargs: Additional arguments for AgentMonitor
        
    Returns:
        Monitored agent instance
    """
    return SimpleAgentMonitor(
        agent_id=agent_id,
        api_key=api_key,
        ai_model_func=ai_model_func,
        base_url=base_url,
        **kwargs
    ) 