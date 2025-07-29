#!/usr/bin/env python3
"""
EnableAI Agent Monitor - Drop-in SDK for Agent Performance Monitoring

This module provides automatic performance monitoring and self-healing capabilities
for any AI agent. Simply import and wrap your agent to get:

- Automatic performance reporting
- Quality evaluation using Claude
- Self-healing with prompt improvements
- Performance analytics and insights
- Optional sampling-based monitoring for production use

Usage:
    from enable_ai_sdk.agent_monitor import AgentMonitor
    
    # Full monitoring (default)
    monitored_agent = AgentMonitor(
        agent_id="your-agent-id",
        api_key="your-api-key",
        base_url="https://your-backend.com"
    )
    
    # Sampling-based monitoring (new feature)
    sampled_agent = AgentMonitor(
        agent_id="your-agent-id",
        api_key="your-api-key",
        base_url="https://your-backend.com",
        enable_sampling=True,
        sampling_config={
            "strategy": "percentage",
            "rate": 0.05,  # 5% of interactions
            "batch_size": 100,
            "max_daily_samples": 1000
        }
    )
    
    # Use it like a normal agent
    response = monitored_agent.generate_response("What is your return policy?")
    
    # The SDK automatically:
    # - Reports the interaction for evaluation (or samples based on config)
    # - Gets quality scores and insights
    # - Triggers self-healing if needed
    # - Applies prompt improvements automatically
"""

import requests
import json
import time
import threading
import random
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_default_sampling_config():
    """Get default sampling configuration"""
    return {
        "strategy": "percentage",
        "rate": 0.05,  # 5% of interactions
        "batch_size": 100,
        "max_daily_samples": 1000,
        "performance_threshold": 70,
        "sampling_window": "daily"
    }

class SamplingManager:
    """Manages sampling logic and batch processing"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.batch_queue = []
        self.daily_sample_count = 0
        self.last_batch_time = None
        self.last_reset_date = datetime.now().date()
        
    def should_sample(self, interaction_data: Dict[str, Any]) -> bool:
        """Determine if this interaction should be sampled"""
        
        # Reset daily counter if it's a new day
        current_date = datetime.now().date()
        if current_date != self.last_reset_date:
            self.daily_sample_count = 0
            self.last_reset_date = current_date
        
        # Check if we've hit daily limits
        if self.daily_sample_count >= self.config.get("max_daily_samples", 1000):
            return False
        
        # Performance-based sampling
        if hasattr(self, 'average_score') and self.average_score < self.config.get("performance_threshold", 70):
            # Sample more when performance is poor
            enhanced_rate = self.config.get("rate", 0.05) * 2
            should_sample = random.random() < enhanced_rate
        else:
            # Regular sampling
            should_sample = random.random() < self.config.get("rate", 0.05)
        
        if should_sample:
            self.daily_sample_count += 1
            
        return should_sample
    
    def add_to_batch(self, interaction_data: Dict[str, Any]):
        """Add interaction to batch queue"""
        self.batch_queue.append(interaction_data)
        
        # Send batch if we've reached the batch size
        if len(self.batch_queue) >= self.config.get("batch_size", 100):
            return True  # Signal to send batch
        
        return False
    
    def get_batch(self) -> List[Dict[str, Any]]:
        """Get current batch and clear queue"""
        batch = self.batch_queue.copy()
        self.batch_queue.clear()
        return batch
    
    def get_stats(self) -> Dict[str, Any]:
        """Get sampling statistics"""
        return {
            "daily_sample_count": self.daily_sample_count,
            "batch_queue_size": len(self.batch_queue),
            "max_daily_samples": self.config.get("max_daily_samples", 1000),
            "sampling_rate": self.config.get("rate", 0.05)
        }

class AgentMonitor:
    """
    Drop-in agent monitor that automatically reports performance and handles self-healing
    """
    
    def __init__(self, 
                 agent_id: str,
                 api_key: str,
                 base_url: str = "https://api.weenable.ai",
                 auto_healing: bool = True,
                 report_async: bool = True,
                 system_prompt: Optional[str] = None,
                 enable_sampling: bool = False,
                 sampling_config: Optional[Dict[str, Any]] = None):
        """
        Initialize the agent monitor
        
        Args:
            agent_id: Your agent's ID from EnableAI platform
            api_key: Your EnableAI API key
            base_url: EnableAI backend URL (defaults to production)
            auto_healing: Whether to automatically apply prompt improvements
            report_async: Whether to report performance asynchronously
            system_prompt: Current system prompt (will be updated by self-healing)
            enable_sampling: Whether to use sampling-based monitoring (new feature)
            sampling_config: Configuration for sampling (only used if enable_sampling=True)
        """
        self.agent_id = agent_id
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.auto_healing = auto_healing
        self.report_async = report_async
        self.system_prompt = system_prompt
        self.enable_sampling = enable_sampling
        
        # Initialize sampling manager if sampling is enabled
        if self.enable_sampling:
            config = sampling_config or get_default_sampling_config()
            self.sampling_manager = SamplingManager(config)
            logger.info(f"Sampling enabled with config: {config}")
        else:
            self.sampling_manager = None
        
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
        
        logger.info(f"AgentMonitor initialized for agent {agent_id} (sampling: {enable_sampling})")
        
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
        
        # Handle performance reporting based on sampling configuration
        if self.enable_sampling:
            self._handle_sampled_reporting(prompt, response, response_time_ms)
        else:
            # Original behavior - report every interaction
            if self.report_async:
                # Queue for async reporting
                self._queue_performance_report(prompt, response, response_time_ms)
            else:
                # Report immediately
                self._report_performance(prompt, response, response_time_ms)
        
        # Check for self-healing periodically
        self._check_self_healing()
        
        return response
    
    def _handle_sampled_reporting(self, prompt: str, response: str, response_time_ms: int):
        """Handle performance reporting with sampling"""
        interaction_data = {
            "agent_id": self.agent_id,
            "prompt": prompt,
            "response": response,
            "response_time_ms": response_time_ms,
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "source": "agent-monitor-sdk-sampling",
                "interaction_count": self.interaction_count,
                "average_score": self.average_score
            }
        }
        
        # Check if this interaction should be sampled
        if self.sampling_manager.should_sample(interaction_data):
            logger.info(f"📊 Sampling interaction {self.interaction_count + 1}")
            
            # Add to batch
            should_send_batch = self.sampling_manager.add_to_batch(interaction_data)
            
            if should_send_batch:
                self._send_batch()
        else:
            logger.debug(f"⏭️  Skipping interaction {self.interaction_count + 1} (not sampled)")
        
        self.interaction_count += 1
    
    def _send_batch(self):
        """Send batched interactions to the backend"""
        try:
            batch = self.sampling_manager.get_batch()
            if not batch:
                return
            
            logger.info(f"📦 Sending batch of {len(batch)} interactions")
            
            # Send batch to backend
            api_response = self.session.post(
                f"{self.base_url}/agent/external/performance/batch",
                json={"interactions": batch},
                timeout=30
            )
            
            if api_response.status_code == 201:
                result = api_response.json()
                logger.info(f"✅ Batch sent successfully - {len(batch)} interactions processed")
                
                # Update average score if provided
                if result.get('average_score'):
                    self.average_score = result['average_score']
            else:
                logger.error(f"❌ Failed to send batch: {api_response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Error sending batch: {e}")
    
    def get_sampling_stats(self) -> Dict[str, Any]:
        """Get sampling statistics"""
        if not self.enable_sampling:
            return {"error": "Sampling not enabled"}
        
        return self.sampling_manager.get_stats()
    
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
        
        # Start async reporting
        threading.Thread(target=report_async, daemon=True).start()
    
    def _check_self_healing(self):
        """Check if self-healing is needed"""
        # Only check every 10 interactions to avoid too many API calls
        if self.interaction_count % 10 == 0:
            current_time = time.time()
            
            # Check every 5 minutes
            if (not self.last_healing_check or 
                current_time - self.last_healing_check > 300):
                
                self.last_healing_check = current_time
                self._trigger_self_healing()
    
    def _trigger_self_healing(self):
        """Trigger self-healing for the agent"""
        try:
            # Step 1: First trigger a self-healing scan to flag the agent
            scan_response = self.session.post(
                f"{self.base_url}/self-healing/scan",
                json={},
                timeout=30
            )
            
            if scan_response.status_code != 200:
                logger.error(f"Failed to trigger self-healing scan: {scan_response.status_code}")
                return False
            
            scan_data = scan_response.json()
            logger.info(f"Self-healing scan completed: {scan_data.get('total_agents_scanned')} agents scanned")
            
            # Check if our agent was flagged
            agent_flagged = False
            for agent in scan_data.get('agents_flagged', []):
                if agent.get('agent_id') == self.agent_id:
                    agent_flagged = True
                    logger.info(f"Agent flagged for healing: {agent.get('analysis', {}).get('reason')}")
                    break
            
            if not agent_flagged:
                logger.info("Agent not flagged for healing - performance may be acceptable")
                return False
            
            # Step 2: Now trigger the actual healing
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
                    # For auto strategy, the prompt was updated in the database
                    # We need to fetch the updated prompt from the agent endpoint
                    try:
                        agent_response = self.session.get(
                            f"{self.base_url}/agent/{self.agent_id}/prompt",
                            timeout=10
                        )
                        
                        if agent_response.status_code == 200:
                            agent_data = agent_response.json()
                            new_prompt = agent_data.get('system_prompt')
                            if new_prompt:
                                self.system_prompt = new_prompt
                                logger.info("System prompt updated via self-healing (auto strategy)")
                                return True
                        else:
                            logger.error(f"Failed to fetch updated prompt: {agent_response.status_code}")
                    except Exception as e:
                        logger.error(f"Error fetching updated prompt: {e}")
                
                elif result.get('suggested_prompt') and not self.auto_healing:
                    # For suggest strategy, we get the suggested prompt in the response
                    new_prompt = result.get('suggested_prompt')
                    if new_prompt:
                        self.system_prompt = new_prompt
                        logger.info("System prompt updated via self-healing (suggest strategy)")
                
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
                 base_url: str = "https://api.weenable.ai",
                 enable_sampling: bool = False,
                 sampling_config: Optional[Dict[str, Any]] = None,
                 **kwargs):
        """
        Initialize with a simple AI model function
        
        Args:
            agent_id: Your agent's ID
            api_key: Your EnableAI API key
            ai_model_func: Function that takes a prompt and returns a response
            base_url: EnableAI backend URL
            enable_sampling: Whether to use sampling-based monitoring
            sampling_config: Configuration for sampling
            **kwargs: Additional arguments for AgentMonitor
        """
        super().__init__(agent_id, api_key, base_url, enable_sampling=enable_sampling, sampling_config=sampling_config, **kwargs)
        self.ai_model_func = ai_model_func
    
    def _call_ai_model(self, prompt: str, **kwargs) -> str:
        """Call the provided AI model function"""
        return self.ai_model_func(prompt)


# Convenience function for quick setup
def create_monitored_agent(agent_id: str, 
                          api_key: str, 
                          ai_model_func: Callable[[str], str],
                          base_url: str = "https://api.weenable.ai",
                          enable_sampling: bool = False,
                          sampling_config: Optional[Dict[str, Any]] = None,
                          **kwargs) -> SimpleAgentMonitor:
    """
    Create a monitored agent with minimal setup
    
    Args:
        agent_id: Your agent's ID
        api_key: Your EnableAI API key
        ai_model_func: Function that takes a prompt and returns a response
        base_url: EnableAI backend URL
        enable_sampling: Whether to use sampling-based monitoring (new feature)
        sampling_config: Configuration for sampling (only used if enable_sampling=True)
        **kwargs: Additional arguments for AgentMonitor
        
    Returns:
        Monitored agent instance
    """
    return SimpleAgentMonitor(
        agent_id=agent_id,
        api_key=api_key,
        ai_model_func=ai_model_func,
        base_url=base_url,
        enable_sampling=enable_sampling,
        sampling_config=sampling_config,
        **kwargs
    )

# Convenience function for sampling-based monitoring
def create_sampled_agent(agent_id: str,
                        api_key: str,
                        ai_model_func: Callable[[str], str],
                        sampling_rate: float = 0.05,
                        base_url: str = "https://api.weenable.ai",
                        **kwargs) -> SimpleAgentMonitor:
    """
    Create a sampling-based monitored agent
    
    Args:
        agent_id: Your agent's ID
        api_key: Your EnableAI API key
        ai_model_func: Function that takes a prompt and returns a response
        sampling_rate: Percentage of interactions to sample (0.05 = 5%)
        base_url: EnableAI backend URL
        **kwargs: Additional arguments for AgentMonitor
        
    Returns:
        Monitored agent instance with sampling enabled
    """
    sampling_config = {
        "strategy": "percentage",
        "rate": sampling_rate,
        "batch_size": 100,
        "max_daily_samples": 1000,
        "performance_threshold": 70,
        "sampling_window": "daily"
    }
    
    return create_monitored_agent(
        agent_id=agent_id,
        api_key=api_key,
        ai_model_func=ai_model_func,
        base_url=base_url,
        enable_sampling=True,
        sampling_config=sampling_config,
        **kwargs
    ) 