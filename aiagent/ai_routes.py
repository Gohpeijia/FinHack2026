from flask import Blueprint, request, jsonify
from ai_agent import AIAgent

# Create the blueprint for your AI routes
ai_bp = Blueprint('ai', __name__)

# Initialize your AI Agent globally so it's ready when the server starts
agent = AIAgent()

@ai_bp.route('/chat', methods=['POST'])
def chat_with_agent():
    try:
        # 1. Get the message and ticker from the React frontend
        data = request.json
        user_message = data.get('message')
        ticker = data.get('ticker') # This is optional!
        
        if not user_message:
            return jsonify({"success": False, "error": "Message is required."}), 400

        # 2. Feed it into your teammate's AI pipeline!
        print(f"🤖 [API] Processing message: {user_message}")
        result = agent.process(user_input=user_message, ticker=ticker)

        # 3. If the agent crashed (all API keys failed)
        if result.get("status") == "ERROR":
            return jsonify({
                "success": False, 
                "error": result["final_advice"]
            }), 503

        # 4. If successful, send the beautiful data back to React!
        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:
        print(f"❌ [API Error] {str(e)}")
        return jsonify({"success": False, "error": "Internal server error."}), 500