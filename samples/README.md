# EnableAI SDK Samples

Welcome to the EnableAI SDK samples! This directory contains progressive examples that will help you learn and test the SDK functionality step by step.

## 🎯 Learning Progression

The samples are organized in a progressive learning path:

### 📚 Step 1: Beginner (01-beginner)
**Goal**: Verify SDK installation and basic setup
- **File**: `test_sdk_import.py`
- **What it tests**: SDK import, client initialization, basic connectivity
- **Time**: ~2 minutes
- **Prerequisites**: None (just install the SDK)

### 🚀 Step 2: Intermediate (02-intermediate)
**Goal**: Test core SDK functionality
- **File**: `simple_agent_template.py`
- **What it tests**: Agent registration, feedback submission, analytics, self-healing
- **Time**: ~5 minutes
- **Prerequisites**: API key and backend URL

### 🔧 Step 3: Advanced (03-advanced)
**Goal**: Test all SDK features with interactive options
- **File**: `agent_template.py`
- **What it tests**: Everything + webhooks, interactive testing, detailed analytics
- **Time**: ~10-15 minutes
- **Prerequisites**: API key and backend URL

## 🚀 Quick Start

### Prerequisites
```bash
pip install requests
pip install enable_ai_sdk
```

### Step 1: Test SDK Installation
```bash
cd samples/01-beginner
python test_sdk_import.py
```

### Step 2: Test Core Features
```bash
cd ../02-intermediate
# Edit simple_agent_template.py to add your API key
python simple_agent_template.py
```

### Step 3: Test Advanced Features
```bash
cd ../03-advanced
# Edit agent_template.py to add your API key
python agent_template.py
```

## 📁 Sample Details

### 01-beginner/test_sdk_import.py
**Purpose**: Verify your SDK installation and basic functionality

**What it does**:
- ✅ Tests SDK import
- ✅ Tests client initialization
- ✅ Tests convenience functions
- ✅ Validates basic setup

**Expected output**:
```
🚀 EnableAI SDK Import Test - Beginner Level
==================================================
This is Step 1: Testing SDK Installation and Basic Setup
==================================================
🔍 Testing EnableAI SDK import...
✅ EnableAIClient imported successfully
✅ Convenience functions imported successfully
✅ Data models imported successfully
✅ Exception classes imported successfully

🔍 Testing client initialization...
✅ Client initialized successfully
✅ Agent manager initialized
✅ Analytics manager initialized
✅ Webhook manager initialized
✅ Self-healing manager initialized

🎉 All tests passed!
Your EnableAI SDK is ready to use!
```

### 02-intermediate/simple_agent_template.py
**Purpose**: Test core SDK functionality with a real API

**What it does**:
- ✅ API connection and health check
- ✅ Agent registration
- ✅ Feedback submission
- ✅ Analytics retrieval
- ✅ Self-healing scan
- ✅ Agent listing

**Expected output**:
```
🚀 EnableAI SDK Test Script - Intermediate Level
============================================================
This is Step 2: Testing Core SDK Functionality
============================================================
✅ Client initialized

🔍 Testing API connection...
✅ API is healthy: {'status': 'healthy'}

🤖 Registering agent: My Test Agent
✅ Agent registered successfully!
   ID: agent-uuid-123
   Name: My Test Agent
   Type: customer-support

📝 Submitting test feedback...
✅ Feedback submitted - Score: 85.0

📊 Getting agent analytics...
✅ Analytics retrieved:
   Agent: My Test Agent
   Score Trend: improving
   Average Score: 85.0
   Feedback Count: 1

🎉 Core functionality test completed successfully!
```

### 03-advanced/agent_template.py
**Purpose**: Comprehensive testing with interactive features

**What it does**:
- ✅ Everything from intermediate level
- ✅ Interactive menu for selective testing
- ✅ Webhook management (create, test, delete)
- ✅ Detailed analytics with issues and suggestions
- ✅ Full test suite with user interaction
- ✅ Advanced error handling

**Features**:
- **Interactive Menu**: Test features one by one
- **Webhook Testing**: Create and test webhooks
- **Detailed Analytics**: Comprehensive performance insights
- **Error Handling**: Robust error reporting
- **Customizable**: Easy to modify test data

## 🔧 Configuration

### Required Configuration
Both intermediate and advanced samples require:

```python
# Your API credentials
API_KEY = "your-actual-api-key-here"
BASE_URL = "https://your-actual-backend.com"
```

### Optional Configuration
Advanced sample also supports:

```python
# Agent settings
AGENT_NAME = "My Custom Agent"
AGENT_TYPE = "customer-support"  # or "sales-assistant", "technical-support"
AGENT_LLM = "claude-3-5-sonnet-20241022"

# Test data customization
TEST_PROMPTS = ["Your custom prompts..."]
TEST_RESPONSES = ["Your custom responses..."]
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Error**
   ```bash
   pip install enable_ai_sdk
   ```

2. **Authentication Error**
   - Check your API key is correct
   - Ensure the API key has proper permissions

3. **Connection Error**
   - Verify your backend URL is correct
   - Check that your backend is running

4. **Configuration Error**
   - Make sure you've updated the placeholder values
   - Check that all required fields are provided

### Debug Mode
For detailed error information, add this to any sample:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Expected Results

### Successful Test Results
When everything works correctly, you should see:

- ✅ All import tests pass
- ✅ Client initializes successfully
- ✅ API health check passes
- ✅ Agent registration succeeds
- ✅ Feedback submission works
- ✅ Analytics are retrieved
- ✅ Self-healing scan completes
- ✅ Agent listing works

### What Each Test Validates

| Test | What it validates |
|------|-------------------|
| Import | SDK installation and basic imports |
| Client Init | SDK client setup and configuration |
| Health Check | API connectivity and authentication |
| Agent Registration | Agent creation and management |
| Feedback | Response evaluation and scoring |
| Analytics | Performance insights and trends |
| Self-Healing | Agent monitoring and health checks |
| Webhooks | Real-time notification system |

## 🎯 Next Steps

After completing the samples:

1. **Explore the SDK documentation** for detailed API reference
2. **Check the examples directory** for integration examples
3. **Review the tests directory** for comprehensive test cases
4. **Integrate the SDK** into your own applications
5. **Set up webhooks** for production monitoring
6. **Implement self-healing** for automated agent management

## 📞 Support

If you encounter issues:

1. Check the error messages for specific details
2. Verify your configuration is correct
3. Test with the beginner sample first
4. Check the SDK documentation
5. Review the troubleshooting section above
6. Contact support if issues persist

---

**Happy testing! 🚀**

*Start with the beginner sample and work your way up to master all SDK features.* 