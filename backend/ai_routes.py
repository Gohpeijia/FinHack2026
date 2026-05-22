from flask import Blueprint, request, jsonify, g
from aiagent.ai_agent import AIAgent
from firebase_config import db      # <-- Import your database
from security import require_auth   # <-- Ensure only logged-in users can chat
from datetime import datetime       # <-- To timestamp the messages

ai_bp = Blueprint('ai', __name__)
agent = AIAgent()

@ai_bp.route('/chat', methods=['POST'])
@require_auth  # Protect the route!
def chat_with_agent():
    try:
        data = request.json
        user_message = data.get('message')
        ticker = data.get('ticker') 
        
        # 1. Identify the user securely
        secure_user_id = g.uid
        
        if not user_message:
            return jsonify({"success": False, "error": "Message is required."}), 400

        print(f"🤖 [API] Processing message: {user_message}")
        
        # 2. Feed it into your teammate's AI pipeline!
        result = agent.process(user_input=user_message, ticker=ticker)

        if result.get("status") == "ERROR":
            return jsonify({"success": False, "error": result["final_advice"]}), 503

        # 3. SAVE TO FIRESTORE DATABASE
        # We grab the user's document
        user_ref = db.collection('users').document(secure_user_id)
        user_doc = user_ref.get()
        
        # Get existing history, or start a new empty list
        chat_history = []
        if user_doc.exists:
            user_data = user_doc.to_dict()
            chat_history = user_data.get('chat_history', [])

        # Append the new conversation pair
        now = datetime.now().isoformat()
        chat_history.append({"role": "user", "content": user_message, "timestamp": now})
        chat_history.append({"role": "ai", "content": result['final_advice'], "timestamp": now})

        # Save it back to the cloud!
        # Using merge=True ensures we don't accidentally delete their portfolio data
        user_ref.set({"chat_history": chat_history}, merge=True)

        # 4. Send the result back to React
        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:
        print(f"❌ [API Error] {str(e)}")
        return jsonify({"success": False, "error": "Internal server error."}), 500