# Changelog

All notable changes to the EnableAI SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-07-27

### Added
- **Drop-in SDK Integration**: New `create_monitored_agent()` function for automatic agent monitoring
- **AgentMonitor Class**: Advanced class for custom agent monitoring with automatic self-healing
- **3-Line Integration**: Simplified approach with "Just import and wrap your agent - everything else is automatic!"
- **Automatic Monitoring**: Background performance tracking, quality scoring, and issue detection
- **Self-Healing**: Automatic prompt improvements when agent performance degrades
- **New Sample Files**: `drop_in_integration.py` and `drop_in_advanced.py` with progressive learning
- **Updated Documentation**: Restructured READMEs to emphasize drop-in approach as primary integration method
- **AWS Lambda Integration**: Example showing serverless deployment with drop-in SDK

### Changed
- **Primary Integration Method**: Shifted from manual API approach to drop-in SDK approach
- **Documentation Structure**: Prioritized drop-in integration guide over manual API reference
- **Learning Path**: Updated samples to emphasize progressive learning from beginner to advanced
- **Core Message**: Updated all documentation to reflect "everything is automatic" philosophy

### Features
- Automatic performance reporting and quality scoring
- Background monitoring with minimal configuration
- Custom agent classes with conversation history tracking
- Production-ready configuration options
- Comprehensive error handling for network issues
- Type hints and documentation for all new features

## [Unreleased]

### Added
- Initial SDK release
- Agent management functionality
- Analytics and insights
- Self-healing capabilities
- Webhook management
- Feedback system
- Comprehensive error handling
- Type hints and documentation

## [1.0.0] - 2024-01-01

### Added
- Initial release of EnableAI SDK
- `EnableAIClient` class for main client functionality
- `AgentManager` for agent registration, listing, updating, and deletion
- `AnalyticsManager` for analytics and feedback submission
- `WebhookManager` for webhook creation and management
- `SelfHealingManager` for self-healing scans and agent healing
- Data models: `Agent`, `AnalyticsResult`, `FeedbackResult`
- Custom exceptions: `EnableAIError`, `AuthenticationError`, `ValidationError`, `RateLimitError`
- Convenience functions: `create_client`, `quick_agent_register`, `quick_feedback_submit`
- Comprehensive documentation and examples
- MIT license

### Features
- Agent registration with customizable parameters
- Real-time analytics and performance insights
- Feedback submission and evaluation
- Self-healing agent monitoring
- Webhook configuration for notifications
- Health check functionality
- Error handling with specific exception types
- Type hints for better development experience

### Documentation
- Complete API reference
- Installation instructions
- Usage examples
- Integration guides for Flask and Django
- Production considerations
- Error handling best practices 