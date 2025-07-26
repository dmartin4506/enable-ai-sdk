# Changelog

All notable changes to the EnableAI SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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