# Sampling-Based Monitoring Guide

A comprehensive guide to using the new sampling-based monitoring feature for cost-effective agent monitoring in production environments.

## 🎯 Overview

The sampling feature allows you to monitor high-volume AI agents cost-effectively by only reporting a percentage of interactions while still maintaining quality insights and self-healing capabilities.

## 🚀 Quick Start

### Basic Sampling Setup

```python
from enable_ai_sdk.agent_monitor import create_sampled_agent

# Create agent with 5% sampling
agent = create_sampled_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    sampling_rate=0.05  # 5% sampling
)

# Use normally - only sampled interactions are reported
response = agent.generate_response("What is your return policy?")
```

### Advanced Sampling Configuration

```python
from enable_ai_sdk.agent_monitor import create_monitored_agent

# Custom sampling configuration
agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    enable_sampling=True,
    sampling_config={
        "strategy": "percentage",
        "rate": 0.1,  # 10% sampling
        "batch_size": 50,  # Send batch every 50 samples
        "max_daily_samples": 500,
        "performance_threshold": 70,  # Sample more when performance is poor
        "sampling_window": "daily"
    }
)
```

## 📊 Sampling Configuration Options

### Basic Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `rate` | float | 0.05 | Sampling rate (0.01 = 1%, 0.1 = 10%) |
| `batch_size` | int | 100 | Interactions per batch |
| `max_daily_samples` | int | 1000 | Maximum samples per day |
| `performance_threshold` | int | 70 | Score threshold for enhanced sampling |
| `sampling_window` | string | "daily" | Reset window for daily limits |

### Advanced Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `strategy` | string | "percentage" | Sampling strategy (percentage) |
| `enhanced_rate_multiplier` | float | 2.0 | Multiplier for enhanced sampling |

## 🎯 Use Cases and Recommendations

### Development and Testing
```python
# Full monitoring for complete visibility
agent = create_monitored_agent(
    agent_id="dev-agent",
    api_key="your-api-key",
    ai_model_func=your_ai_model
    # No sampling - every interaction reported
)
```

### Production (Low Volume)
```python
# 10-20% sampling for cost control
agent = create_sampled_agent(
    agent_id="prod-low-agent",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    sampling_rate=0.15  # 15% sampling
)
```

### Production (High Volume)
```python
# 1-5% sampling for maximum efficiency
agent = create_sampled_agent(
    agent_id="prod-high-agent",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    sampling_rate=0.05  # 5% sampling
)
```

### Critical Agents
```python
# Full monitoring for quality assurance
agent = create_monitored_agent(
    agent_id="critical-agent",
    api_key="your-api-key",
    ai_model_func=your_ai_model
    # No sampling - every interaction reported
)
```

## 📈 Cost Impact Analysis

### API Call Reduction

| Sampling Rate | API Calls | Reduction | Cost Savings |
|---------------|-----------|-----------|--------------|
| 100% (Full) | 1 per interaction | 0% | $0 |
| 20% | 1 per 5 interactions | 80% | 80% |
| 10% | 1 per 10 interactions | 90% | 90% |
| 5% | 1 per 20 interactions | 95% | 95% |
| 1% | 1 per 100 interactions | 99% | 99% |

### Example Scenarios

**High-Volume E-commerce Agent**
- 10,000 interactions/day
- 5% sampling = 500 API calls/day
- 95% cost reduction
- Still provides meaningful insights

**Customer Support Agent**
- 1,000 interactions/day
- 10% sampling = 100 API calls/day
- 90% cost reduction
- Maintains quality monitoring

## 🔧 Monitoring and Statistics

### Get Sampling Statistics

```python
# Get current sampling statistics
stats = agent.get_sampling_stats()
print(f"Daily samples: {stats['daily_sample_count']}")
print(f"Batch queue size: {stats['batch_queue_size']}")
print(f"Sampling rate: {stats['sampling_rate']}")
print(f"Max daily samples: {stats['max_daily_samples']}")
```

### Check Sampling Status

```python
# Check if sampling is enabled
if agent.enable_sampling:
    print("✅ Sampling is enabled")
    stats = agent.get_sampling_stats()
    print(f"📊 Current batch queue: {stats['batch_queue_size']} interactions")
    print(f"📊 Daily samples: {stats['daily_sample_count']}/{stats['max_daily_samples']}")
else:
    print("📊 Full monitoring mode")
```

### Performance-Based Sampling

The SDK automatically increases sampling when performance is poor:

```python
# When average score < 70, sampling rate doubles
# Example: 5% normal rate becomes 10% when performance is poor
agent = create_monitored_agent(
    agent_id="your-agent-id",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    enable_sampling=True,
    sampling_config={
        "rate": 0.05,  # 5% normal sampling
        "performance_threshold": 70,  # Enhanced sampling below this score
        # Enhanced rate = 0.05 * 2 = 10% when performance is poor
    }
)
```

## 🔄 Batch Processing

### How Batching Works

1. **Queue Interactions**: Sampled interactions are queued
2. **Batch Size**: When queue reaches `batch_size`, batch is sent
3. **Efficiency**: Reduces API calls and improves performance
4. **Statistics**: Returns batch processing statistics

### Batch Configuration

```python
# Small batches for real-time monitoring
agent = create_monitored_agent(
    agent_id="real-time-agent",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    enable_sampling=True,
    sampling_config={
        "rate": 0.1,
        "batch_size": 10,  # Send every 10 samples
        "max_daily_samples": 1000
    }
)

# Large batches for efficiency
agent = create_monitored_agent(
    agent_id="efficient-agent",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    enable_sampling=True,
    sampling_config={
        "rate": 0.05,
        "batch_size": 200,  # Send every 200 samples
        "max_daily_samples": 500
    }
)
```

## 🎯 Best Practices

### 1. Choose Appropriate Sampling Rates

```python
# Development: Full monitoring
dev_agent = create_monitored_agent(...)

# Production (low volume): 10-20% sampling
prod_low_agent = create_sampled_agent(
    sampling_rate=0.15  # 15% sampling
)

# Production (high volume): 1-5% sampling
prod_high_agent = create_sampled_agent(
    sampling_rate=0.05  # 5% sampling
)

# Critical agents: Full monitoring
critical_agent = create_monitored_agent(...)
```

### 2. Monitor Sampling Statistics

```python
# Regular monitoring of sampling effectiveness
def check_sampling_stats(agent):
    stats = agent.get_sampling_stats()
    print(f"📊 Sampling Statistics:")
    print(f"   Daily samples: {stats['daily_sample_count']}")
    print(f"   Batch queue: {stats['batch_queue_size']}")
    print(f"   Sampling rate: {stats['sampling_rate']}")
    
    # Alert if approaching daily limit
    if stats['daily_sample_count'] > stats['max_daily_samples'] * 0.8:
        print("⚠️  Approaching daily sample limit")
```

### 3. Adjust Based on Performance

```python
# Start with conservative sampling
agent = create_sampled_agent(
    sampling_rate=0.1  # 10% sampling
)

# Monitor performance and adjust
stats = agent.get_sampling_stats()
if stats['daily_sample_count'] < 50:
    # Increase sampling if not getting enough data
    agent = create_sampled_agent(
        sampling_rate=0.2  # 20% sampling
    )
```

### 4. Use Performance-Based Sampling

```python
# Automatically sample more when performance is poor
agent = create_monitored_agent(
    enable_sampling=True,
    sampling_config={
        "rate": 0.05,  # 5% normal sampling
        "performance_threshold": 70,  # Enhanced sampling below 70
        "enhanced_rate_multiplier": 2.0  # 10% when performance is poor
    }
)
```

## 🔧 Migration from Full Monitoring

### Step 1: Test with Sampling

```python
# Start with a test agent using sampling
test_agent = create_sampled_agent(
    agent_id="test-sampled-agent",
    api_key="your-api-key",
    ai_model_func=your_ai_model,
    sampling_rate=0.2  # 20% sampling for testing
)

# Compare with full monitoring
full_agent = create_monitored_agent(
    agent_id="test-full-agent",
    api_key="your-api-key",
    ai_model_func=your_ai_model
)
```

### Step 2: Monitor Effectiveness

```python
# Check if sampling provides sufficient insights
def compare_monitoring_effectiveness():
    full_stats = full_agent.get_health_status()
    sampled_stats = test_agent.get_health_status()
    
    print(f"Full monitoring score: {full_stats.get('average_score', 0)}")
    print(f"Sampled monitoring score: {sampled_stats.get('average_score', 0)}")
    
    # If scores are similar, sampling is effective
    if abs(full_stats.get('average_score', 0) - sampled_stats.get('average_score', 0)) < 5:
        print("✅ Sampling provides effective monitoring")
    else:
        print("⚠️  Consider increasing sampling rate")
```

### Step 3: Gradual Migration

```python
# Phase 1: Non-critical agents
non_critical_agent = create_sampled_agent(
    sampling_rate=0.1  # 10% sampling
)

# Phase 2: Medium-volume agents
medium_volume_agent = create_sampled_agent(
    sampling_rate=0.05  # 5% sampling
)

# Phase 3: High-volume agents
high_volume_agent = create_sampled_agent(
    sampling_rate=0.02  # 2% sampling
)

# Keep critical agents with full monitoring
critical_agent = create_monitored_agent(...)
```

## 🚨 Troubleshooting

### Common Issues

**1. Not Getting Enough Data**
```python
# Increase sampling rate
agent = create_sampled_agent(
    sampling_rate=0.2  # Increase from 5% to 20%
)
```

**2. Too Many API Calls**
```python
# Decrease sampling rate
agent = create_sampled_agent(
    sampling_rate=0.02  # Decrease from 5% to 2%
)
```

**3. Batch Not Sending**
```python
# Check batch size configuration
agent = create_monitored_agent(
    enable_sampling=True,
    sampling_config={
        "batch_size": 10,  # Smaller batches for testing
        "rate": 0.1
    }
)
```

**4. Daily Limit Reached**
```python
# Increase daily limit
agent = create_monitored_agent(
    enable_sampling=True,
    sampling_config={
        "max_daily_samples": 2000,  # Increase from 1000
        "rate": 0.05
    }
)
```

### Debug Sampling

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check sampling decisions
agent = create_sampled_agent(
    sampling_rate=0.1
)

# Each interaction will show sampling decision
response = agent.generate_response("Test query")
# Logs will show: "📊 Sampling interaction X" or "⏭️  Skipping interaction X"
```

## 📊 Performance Comparison

### Before Sampling (Full Monitoring)
- **API Calls**: 1 per interaction
- **Cost**: 100% of monitoring cost
- **Latency**: Higher due to every interaction
- **Privacy**: Every conversation analyzed

### After Sampling (5% Rate)
- **API Calls**: 1 per 20 interactions
- **Cost**: 5% of monitoring cost (95% savings)
- **Latency**: Lower due to fewer API calls
- **Privacy**: Only 5% of conversations analyzed
- **Insights**: Still meaningful performance data

## 🎯 Conclusion

Sampling-based monitoring provides:

1. **Cost Efficiency**: 95% reduction in API calls
2. **Performance**: Reduced latency and bandwidth
3. **Privacy**: Not every conversation analyzed
4. **Scalability**: Handle more agents with less load
5. **Quality**: Still get meaningful performance insights
6. **Flexibility**: Choose appropriate rates for your use case

The sampling feature is perfect for production deployments where cost control and privacy are important while maintaining quality monitoring and self-healing capabilities. 