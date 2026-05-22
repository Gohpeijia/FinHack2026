from firebase_config import db
from flask import Blueprint, jsonify, request, g # <-- Import 'g' from flask!
from security import require_auth 

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/my-portfolio', methods=['GET'])
@require_auth 
def get_portfolio():
    try:
        # Grab the secure ID from the 'g' object
        secure_user_id = g.uid 
        
        doc_ref = db.collection('users').document(secure_user_id)
        doc = doc_ref.get()
        
        if doc.exists:
            return jsonify({"success": True, "data": doc.to_dict()})
        else:
            return jsonify({"success": False, "error": "User not found"}), 404
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@portfolio_bp.route('/buy', methods=['POST'])
@require_auth
def buy_stock():
    try:
        data = request.json
        secure_user_id = g.uid 
        
        ticker = data.get('ticker', '').upper()
        
        # Safely attempt to parse numbers to avoid 500 errors if user sends letters
        try:
            shares = int(data.get('shares', 0))
            price = float(data.get('price', 0.0))
        except ValueError:
            return jsonify({"success": False, "error": "Shares and price must be valid numbers"}), 400

        # UPGRADE: Strict Validation Hardening
        if not ticker or shares <= 0 or price <= 0:
            return jsonify({"success": False, "error": "Invalid trade values. Shares and price must be greater than zero."}), 400

        user_ref = db.collection('users').document(secure_user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({"success": False, "error": "User not found"}), 404

        user_data = user_doc.to_dict()
        portfolio = user_data.get('portfolio', [])
        
        stock_found = False
        for item in portfolio:
            if item['ticker'] == ticker:
                item['shares'] += shares
                item['averagePrice'] = price 
                stock_found = True
                break

        if not stock_found:
            portfolio.append({
                "ticker": ticker,
                "shares": shares,
                "averagePrice": price
            })

        # UPGRADE: Recalculate total value from scratch to prevent math drift!
        total_value = 0
        for item in portfolio:
            total_value += (item["shares"] * item["averagePrice"])

        user_ref.update({
            "portfolio": portfolio,
            "totalPortfolioValue": total_value
        })

        return jsonify({
            "success": True, 
            "message": f"Successfully bought {shares} shares of {ticker}!"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500