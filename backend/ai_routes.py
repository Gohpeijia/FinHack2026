from flask import Blueprint, request, jsonify, g
from ai_agent import AIAgent
from firebase_config import db      
from security import require_auth   
from datetime import datetime       

ai_bp = Blueprint('ai', __name__)
agent = AIAgent()

@ai_bp.route('/chat', methods=['POST'])
@require_auth 
def chat_with_agent():
    try:
        data = request.json
        
        # Check for both 'message' and 'text' depending on how your frontend named it
        user_message = data.get('message') or data.get('text') 
        ticker = data.get('ticker') 
        
        # 1. CATCH THE NEW FRONTEND VARIABLE
        page_context = data.get('pageContext', 'Unknown Page') 
        
        secure_user_id = g.uid
        
        if not user_message:
            return jsonify({"success": False, "error": "Message is required."}), 400

        print(f"🤖 [API] Processing message: {user_message} on page: {page_context}")
        
        user_ref = db.collection('users').document(secure_user_id)
        user_doc = user_ref.get()
        
        chat_history = []
        preferences = {}
        if user_doc.exists:
            user_data = user_doc.to_dict()
            chat_history = user_data.get('chat_history', [])
            preferences = user_data.get('preference', {})

        # 2. PASS PAGE CONTEXT TO THE AI AGENT
        result = agent.process(
            user_input=user_message, 
            ticker=ticker, 
            chat_history=chat_history,
            page_context=page_context,
            preferences=preferences
        )

        if result.get("status") == "ERROR":
            return jsonify({"success": False, "error": result["final_advice"]}), 503

        now = datetime.now().isoformat()
        chat_history.append({"role": "user", "content": user_message, "timestamp": now})
        chat_history.append({"role": "ai", "content": result['final_advice'], "timestamp": now})

        user_ref.set({"chat_history": chat_history}, merge=True)

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:
        print(f"❌ [API Error] {str(e)}")
        return jsonify({"success": False, "error": "Internal server error."}), 500