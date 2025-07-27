# EnableAI SDK Samples

Welcome to the EnableAI SDK samples! This directory contains progressive examples that will help you learn and test the SDK functionality step by step.

## 🎯 Learning Progression

The samples are organized in a progressive learning path:

### 📚 Step 1: Beginner (01-beginner)
**Goal**: Learn the drop-in integration approach
- **File**: `drop_in_integration.py` - **NEW!** Drop-in SDK integration (3 lines!)
- **File**: `test_sdk_import.py` - Verify SDK installation and basic setup
- **What it tests**: Drop-in integration, SDK import, client initialization, basic connectivity
- **Time**: ~3 minutes
- **Prerequisites**: None (just install the SDK)

### 🚀 Step 2: Intermediate (02-intermediate)
**Goal**: Test advanced drop-in integration and core SDK functionality
- **File**: `drop_in_advanced.py` - **NEW!** Advanced drop-in integration with real AI models
- **File**: `simple_agent_template.py` - Core SDK functionality
- **What it tests**: Advanced drop-in integration, agent registration, feedback submission, analytics, self-healing
- **Time**: ~8 minutes
- **Prerequisites**: API key and backend URL

### 🔧 Step 3: Advanced (03-advanced)
**Goal**: Test all SDK features with interactive options
- **File**: `agent_template.py` - **What it tests**: Everything + webhooks, interactive testing, detailed analytics
- **File**: `real_agent_template.py` - **What it tests**: Real AI agents with OpenAI/Claude + EnableAI integration
- **Time**: ~15-20 minutes
- **Prerequisites**: API key and backend URL

## 🚀 Quick Start

### Prerequisites
```bash
pip install requests
pip install enable-ai-sdk
```

### Step 1: Test Drop-in Integration (Recommended)
```bash
cd samples/01-beginner
python drop_in_integration.py
```

### Step 2: Test Advanced Drop-in Integration
```bash
cd ../02-intermediate
# Edit drop_in_advanced.py to add your API key
python drop_in_advanced.py
```

### Step 3: Test Core Features
```bash
cd ../02-intermediate
# Edit simple_agent_template.py to add your API key
python simple_agent_template.py
```

### Step 4: Test Advanced Features
```bash
cd ../03-advanced
# Edit agent_template.py to add your API key
python agent_template.py
```

### Step 5: Test Real AI Agents (Optional)
```bash
cd ../03-advanced
# Edit real_agent_template.py to add your API keys
python real_agent_template.py
```

## 📁 Sample Details

### 01-beginner/drop_in_integration.py - **NEW!**
**Purpose**: Learn the drop-in integration approach - just import and wrap your agent!

**What it does**:
- ✅ Demonstrates 3-line drop-in integration
- ✅ Shows how to wrap your existing AI model
- ✅ Explains what happens automatically
- ✅ Covers key benefits and next steps

**Expected output**:
```
🚀 EnableAI Drop-in SDK Integration - Beginner Level
============================================================
This is the simplest way to integrate your AI agent!
Just import and wrap your agent - everything else is automatic!
============================================================

📝 Step 1: Define your existing AI model function
✅ Your AI model function defined

🚀 Step 2: Create monitored agent (3 lines!)
✅ Monitored agent created successfully!

🎯 Step 3: Use it normally - everything is automatic!
📤 Test 1: Sending prompt: 'What is your return policy?'
📥 Response: 'Response to: What is your return policy?'
✅ Interaction automatically monitored!

🎉 That's it! Your agent is now automatically monitored!
```

### 02-intermediate/drop_in_advanced.py - **NEW!**
**Purpose**: Advanced drop-in integration with real AI models and production features

**What it does**:
- ✅ Advanced configuration options
- ✅ Custom agent class implementation
- ✅ AWS Lambda integration example
- ✅ Production configuration settings
- ✅ Real AI model integration patterns

**Expected output**:
```
🚀 EnableAI Drop-in SDK Integration - Intermediate Level
============================================================
Advanced drop-in integration with real AI models and configuration
============================================================

📝 Method 1: Simple drop-in with advanced configuration
✅ Advanced monitored agent created successfully!
   - Auto-healing enabled
   - Async reporting enabled
   - Timeout and retry configured

🧪 Testing the monitored agent
📤 Test 1: 'What is your return policy?'
📥 Response: 'Our return policy allows returns within 30 days...'
⏱️  Response time: 0.05s
✅ Automatically monitored and evaluated!

🎉 Your agent is now production-ready with automatic monitoring!
```

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
✅ Agent insights retrieved:
   - Trend: improving
   - Average Score: 78.5
   - Recent Issues: 2
   - Suggested Actions: 3

🔧 Running self-healing scan...
✅ Self-healing scan completed:
   - Agents scanned: 1
   - Agents flagged: 0

🎉 All core functionality tests passed!
```

### 03-advanced/agent_template.py
**Purpose**: Test all SDK features with interactive options

**What it does**:
- ✅ All core functionality
- ✅ Webhook management
- ✅ Interactive testing options
- ✅ Detailed analytics
- ✅ Advanced configuration
- ✅ Error handling

**Expected output**:
```
🚀 EnableAI SDK Advanced Test Script
============================================================
This is Step 3: Testing All SDK Features
============================================================

🔧 Configuration Options:
   - Auto-healing: Enabled
   - Async reporting: Enabled
   - Webhook notifications: Enabled
   - Detailed analytics: Enabled

🤖 Agent Management:
✅ Agent registered: Advanced Test Agent
✅ Agent updated with new description
✅ Agent analytics retrieved

🔗 Webhook Management:
✅ Webhook created: Test Webhook
✅ Webhook tested successfully
✅ Webhook history retrieved

📊 Advanced Analytics:
✅ Detailed performance metrics
✅ Trend analysis
✅ Issue categorization
✅ Suggested improvements

🎉 All advanced features tested successfully!
```

### 03-advanced/real_agent_template.py
**Purpose**: Test with actual AI agents using real AI providers

**What it does**:
- ✅ Real OpenAI/Claude integration
- ✅ Production-ready agent setup
- ✅ Advanced monitoring features
- ✅ Real-time performance tracking
- ✅ Comprehensive testing suite

**Expected output**:
```
🚀 EnableAI Real Agent Integration Test
============================================================
This is Step 4: Testing with Real AI Models
============================================================

🔧 Real AI Model Integration:
✅ OpenAI client initialized
✅ Claude client initialized
✅ Agent models configured

🤖 Real Agent Testing:
📤 Test 1: Customer support query
📥 OpenAI Response: "Our return policy allows..."
📊 Quality Score: 87.5
✅ Automatically monitored!

📤 Test 2: Technical support query
📥 Claude Response: "To reset your password..."
📊 Quality Score: 92.0
✅ Automatically monitored!

📊 Performance Summary:
   - Total interactions: 10
   - Average quality score: 89.2
   - Response time average: 1.2s
   - Issues detected: 0

🎉 Real agent integration successful!
```

## 🎯 Key Learning Points

### Drop-in Integration (Recommended Approach)
1. **Just import and wrap**: `create_monitored_agent()` in 3 lines
2. **Everything automatic**: No manual monitoring required
3. **Production ready**: Works with any AI model
4. **Zero configuration**: Defaults work for most use cases

### Manual API Access (Advanced Users)
1. **Direct control**: Full API access for custom integrations
2. **Advanced features**: Webhooks, detailed analytics, custom workflows
3. **Production deployment**: Enterprise-grade monitoring and management
4. **Custom integrations**: Build your own monitoring systems

## 🚀 Getting Started

### For Most Users (Recommended)
1. **Start with drop-in integration**: `01-beginner/drop_in_integration.py`
2. **Test advanced features**: `02-intermediate/drop_in_advanced.py`
3. **Deploy to production**: Use the patterns shown in the samples

### For Advanced Users
1. **Test core functionality**: `02-intermediate/simple_agent_template.py`
2. **Explore all features**: `03-advanced/agent_template.py`
3. **Real AI integration**: `03-advanced/real_agent_template.py`

## 📚 Additional Resources

- **Main Documentation**: [README.md](../README.md)
- **API Reference**: [SDK_README.md](../SDK_README.md)
- **Installation Guide**: [INSTALLATION_GUIDE.md](../INSTALLATION_GUIDE.md)
- **Drop-in Guide**: [DROP_IN_SDK_SUMMARY.md](../DROP_IN_SDK_SUMMARY.md)

## 🆘 Troubleshooting

### Common Issues
1. **Import errors**: Make sure SDK is installed: `pip install enable-ai-sdk`
2. **API key errors**: Check your API key and agent ID
3. **Connection errors**: Verify your base URL and network connectivity
4. **Rate limiting**: Add delays between requests in testing

### Getting Help
- Check the error messages for specific guidance
- Review the configuration in each sample
- Test with the beginner samples first
- Contact support if issues persist

## 🎉 Success!

Once you've completed the samples, you'll have:
- ✅ Working drop-in integration
- ✅ Automatic agent monitoring
- ✅ Production-ready configuration
- ✅ Real-time performance tracking
- ✅ Self-healing capabilities

Your AI agents are now automatically monitored and continuously improving! 🚀 