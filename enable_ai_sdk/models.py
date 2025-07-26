"""
Data models for the DeckGen SDK
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional


@dataclass
class Agent:
    """Agent data model"""
    id: str
    name: str
    description: Optional[str]
    agent_type: str
    llm: str
    system_prompt: Optional[str]
    created_at: Optional[str]
    customer_id: Optional[int]
    user_id: Optional[int]
    healing_recommended: bool = False


@dataclass
class AnalyticsResult:
    """Analytics result data model"""
    agent_id: str
    agent_name: str
    recent_issues: List[Dict[str, Any]]
    score_trend: str
    feedback_count: int
    average_score: float
    suggested_actions: List[str]
    last_updated: str


@dataclass
class FeedbackResult:
    """Feedback evaluation result"""
    score: float
    issue: str
    feedback_id: str
    timestamp: str 