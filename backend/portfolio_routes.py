from firebase_config import db
from flask import Blueprint, jsonify, request

# Create a Blueprint (a mini-app for routes)
portfolio_bp = Blueprint('portfolio', __name__)

# Note: The url_prefix in app.py will handle the "/api/stocks/portfolio" part
@portfolio_bp.route('/<user_id>', methods=['GET'])
def get_portfolio(user_id):
    try:
        # Fetch data from Firestore
        doc_ref = db.collection('users').document(user_id)
        doc = doc_ref.get()
        
        if doc.exists:
            return jsonify({"success": True, "data": doc.to_dict()})
        else:
            return jsonify({"success": False, "error": "User not found"}), 404
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@portfolio_bp.route('/buy', methods=['POST'])
def buy_stock():
    try:
        # 1. Grab the JSON data the frontend sent us
        data = request.json
        user_id = data.get('userId')
        ticker = data.get('ticker').upper()
        shares = int(data.get('shares', 0))
        price = float(data.get('price', 0.0))

        # 2. Basic validation check
        if not all([user_id, ticker, shares, price]):
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        # 3. Get the user's current portfolio from Firestore
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({"success": False, "error": "User not found"}), 404

        user_data = user_doc.to_dict()
        portfolio = user_data.get('portfolio', [])
        
        # 4. Math: Add new shares to existing stock, OR append new stock to list
        stock_found = False
        for item in portfolio:
            if item['ticker'] == ticker:
                item['shares'] += shares
                # (For a hackathon, we skip complex average price math and just update it)
                item['averagePrice'] = price 
                stock_found = True
                break

        if not stock_found:
            portfolio.append({
                "ticker": ticker,
                "shares": shares,
                "averagePrice": price
            })

        # 5. Math: Update the total portfolio value
        total_value = user_data.get('totalPortfolioValue', 0) + (shares * price)

        # 6. Save the updated data BACK to Firestore!
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