#this file is for the AI teammate route that generates the perfect system prompt based on the dynamic data we have about a stock. It will be called by the frontend when the user clicks on a stock to get detailed insights.


from flask import Blueprint, jsonify
from shariah_filter import check_shariah_compliance
from finnhub_service import get_live_price

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/context/<ticker>', methods=['GET'])
def get_ai_context(ticker):
    try:
        # 1. Get the dynamic data
        compliance_data = check_shariah_compliance(ticker)
        price = get_live_price(ticker)
        
        # 2. Extract the specific variables
        is_halal = compliance_data.get("isHalal", False)
        reason = compliance_data.get("reason", "Unknown")
        
        # 3. Build the perfect prompt for your AI teammate
        ai_context_prompt = f"""
        You are an Islamic Finance AI Assistant. 
        The user is asking about the stock {ticker.upper()}. 
        Current Price: ${price}.
        Shariah Compliant: {'Yes' if is_halal else 'No'}.
        Algorithmic Reason: {reason}
        
        Please explain in 2 short sentences why this stock is {'allowed' if is_halal else 'not allowed'} 
        based on our algorithmic screening and standard Shariah principles.
        """
        
        return jsonify({
            "success": True,
            "data": {
                "ticker": ticker.upper(),
                "system_prompt": ai_context_prompt
            }
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500