#!/usr/bin/env python3
"""
Flask integration example for the EnableAI SDK
"""

from flask import Flask, request, jsonify
from enable_ai_sdk import EnableAIClient
import os


app = Flask(__name__)

# Initialize the SDK client
api_key = os.getenv('ENABLE_AI_API_KEY', 'your-api-key-here')
base_url = os.getenv('ENABLE_AI_BASE_URL', 'https://api.enable.ai')
client = EnableAIClient(api_key=api_key, base_url=base_url)


@app.route('/health', methods=['GET'])
def health_check():
    """Check API health"""
    try:
        health = client.health_check()
        return jsonify({
            'status': 'healthy',
            'api_health': health
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@app.route('/agents', methods=['GET'])
def list_agents():
    """List all agents"""
    try:
        agents = client.agents.list()
        return jsonify({
            'agents': [
                {
                    'id': agent.id,
                    'name': agent.name,
                    'agent_type': agent.agent_type,
                    'llm': agent.llm,
                    'description': agent.description,
                    'created_at': agent.created_at
                }
                for agent in agents
            ]
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/agents', methods=['POST'])
def register_agent():
    """Register a new agent"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'agent_type', 'llm']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Register the agent
        agent = client.agents.register(
            name=data['name'],
            agent_type=data['agent_type'],
            llm=data['llm'],
            description=data.get('description'),
            system_prompt=data.get('system_prompt')
        )
        
        return jsonify({
            'agent_id': agent.id,
            'name': agent.name,
            'agent_type': agent.agent_type,
            'llm': agent.llm,
            'description': agent.description,
            'created_at': agent.created_at,
            'status': 'registered'
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/agents/<agent_id>', methods=['GET'])
def get_agent(agent_id):
    """Get a specific agent"""
    try:
        agent = client.agents.get(agent_id=agent_id)
        return jsonify({
            'id': agent.id,
            'name': agent.name,
            'agent_type': agent.agent_type,
            'llm': agent.llm,
            'description': agent.description,
            'system_prompt': agent.system_prompt,
            'created_at': agent.created_at,
            'customer_id': agent.customer_id,
            'user_id': agent.user_id,
            'healing_recommended': agent.healing_recommended
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/agents/<agent_id>', methods=['PUT'])
def update_agent(agent_id):
    """Update an agent"""
    try:
        data = request.json
        
        # Update the agent
        updated_agent = client.agents.update(agent_id=agent_id, **data)
        
        return jsonify({
            'id': updated_agent.id,
            'name': updated_agent.name,
            'agent_type': updated_agent.agent_type,
            'llm': updated_agent.llm,
            'description': updated_agent.description,
            'system_prompt': updated_agent.system_prompt,
            'status': 'updated'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/agents/<agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    """Delete an agent"""
    try:
        success = client.agents.delete(agent_id=agent_id)
        
        if success:
            return jsonify({
                'message': f'Agent {agent_id} deleted successfully'
            })
        else:
            return jsonify({
                'error': f'Failed to delete agent {agent_id}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback for evaluation"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['prompt', 'response', 'tool', 'use_case']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Submit feedback
        feedback = client.analytics.submit_feedback(
            prompt=data['prompt'],
            response=data['response'],
            tool=data['tool'],
            use_case=data['use_case'],
            agent_id=data.get('agent_id')
        )
        
        return jsonify({
            'feedback_id': feedback.feedback_id,
            'score': feedback.score,
            'issue': feedback.issue,
            'timestamp': feedback.timestamp
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/analytics/<agent_id>', methods=['GET'])
def get_agent_analytics(agent_id):
    """Get analytics for a specific agent"""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        tool = request.args.get('tool')
        use_case = request.args.get('use_case')
        
        # Get analytics
        analytics = client.analytics.get_agent_analytics(
            agent_id=agent_id,
            start_date=start_date,
            end_date=end_date,
            tool=tool,
            use_case=use_case
        )
        
        return jsonify(analytics)
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/analytics/<agent_id>/insights', methods=['GET'])
def get_agent_insights(agent_id):
    """Get insights for a specific agent"""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Get insights
        insights = client.analytics.get_agent_insights(
            agent_id=agent_id,
            start_date=start_date,
            end_date=end_date
        )
        
        return jsonify({
            'agent_id': insights.agent_id,
            'agent_name': insights.agent_name,
            'recent_issues': insights.recent_issues,
            'score_trend': insights.score_trend,
            'feedback_count': insights.feedback_count,
            'average_score': insights.average_score,
            'suggested_actions': insights.suggested_actions,
            'last_updated': insights.last_updated
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/webhooks', methods=['GET'])
def list_webhooks():
    """List all webhooks"""
    try:
        webhooks = client.webhooks.list()
        return jsonify({
            'webhooks': webhooks
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/webhooks', methods=['POST'])
def create_webhook():
    """Create a new webhook"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'url']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Create webhook
        webhook = client.webhooks.create(
            name=data['name'],
            url=data['url'],
            events=data.get('events'),
            headers=data.get('headers'),
            retry_count=data.get('retry_count', 3),
            timeout=data.get('timeout', 10),
            is_active=data.get('is_active', True)
        )
        
        return jsonify(webhook), 201
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/self-healing/scan', methods=['POST'])
def run_self_healing_scan():
    """Run self-healing scan"""
    try:
        customer_id = request.json.get('customer_id') if request.json else None
        
        scan_results = client.self_healing.scan(customer_id=customer_id)
        
        return jsonify(scan_results)
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("🚀 Starting Flask server with EnableAI SDK integration...")
    print("📝 Available endpoints:")
    print("   GET  /health                    - Check API health")
    print("   GET  /agents                    - List all agents")
    print("   POST /agents                    - Register new agent")
    print("   GET  /agents/<id>              - Get specific agent")
    print("   PUT  /agents/<id>              - Update agent")
    print("   DELETE /agents/<id>            - Delete agent")
    print("   POST /feedback                  - Submit feedback")
    print("   GET  /analytics/<id>           - Get agent analytics")
    print("   GET  /analytics/<id>/insights  - Get agent insights")
    print("   GET  /webhooks                 - List webhooks")
    print("   POST /webhooks                 - Create webhook")
    print("   POST /self-healing/scan        - Run self-healing scan")
    print("\n💡 Set environment variables:")
    print("   ENABLE_AI_API_KEY=your-api-key")
    print("   ENABLE_AI_BASE_URL=https://api.enable.ai")
    print("\n🌐 Server starting on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 