import os
import requests
from flask import Blueprint, jsonify, request
from security import require_auth
from shariah_filter import check_shariah_compliance
from finnhub_service import get_live_price

# Create the blueprint for market data
market_bp = Blueprint('market', __name__)

@market_bp.route('/details/<ticker>', methods=['GET'])
@require_auth
def get_stock_details(ticker):
    try:
        # 1. Check Shariah compliance
        is_halal = check_shariah_compliance(ticker)
        
        # 2. Fetch the live price from Finnhub
        price = get_live_price(ticker)
        
        # Handle cases where the stock ticker is invalid or Finnhub fails
        if price is None:
            return jsonify({
                "success": False, 
                "error": f"Could not fetch price for {ticker.upper()}. Check the ticker symbol."
            }), 404
            
        # 3. Package and return the data!
        return jsonify({
            "success": True,
            "data": {
                "ticker": ticker.upper(),
                "price": price,
                "isHalal": is_halal["isHalal"],  # Extract the True/False status
                "complianceReason": is_halal["reason"] # NEW: Show the math to the user!
            }
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@market_bp.route('/all', methods=['GET'])
@require_auth
def get_dynamic_halal_stocks():
    try:
        api_key = os.getenv('FINNHUB_API_KEY')
        
        limit = int(request.args.get('limit', 15))
        symbols_url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={api_key}"
        symbols_response = requests.get(symbols_url)
        all_symbols = symbols_response.json()

        #dynamic stocks limit
        demo_batch = all_symbols[:limit]
        
        compliant_stocks = []

        for stock in demo_batch:
            ticker = stock['displaySymbol']
            
            if '.' in ticker:
                continue
                
            compliance = check_shariah_compliance(ticker)

            if compliance['isHalal']:
                price = get_live_price(ticker)
                compliant_stocks.append({
                    "ticker": ticker,
                    "name": stock['description'], # Finnhub gives us the actual company name!
                    "price": price,
                    "isHalal": True,
                    "reason": compliance['reason']
                })

        return jsonify({
            "success": True, 
            "count": len(compliant_stocks),
            "data": compliant_stocks
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@market_bp.route('/search', methods=['GET'])
@require_auth
def search_stock_possibilities():
    try:
        query = request.args.get('q', '').upper()
        if not query:
            return jsonify({"success": True, "data": []})

        api_key = os.getenv('FINNHUB_API_KEY')
        # Finnhub utility endpoint for searching companies
        search_url = f"https://finnhub.io/api/v1/search?q={query}&token={api_key}"
        response = requests.get(search_url)
        search_results = response.json().get('result', [])

        # Filter and clear out invalid symbols
        possibilities = []
        for stock in search_results[:10]: # Top 10 results
            symbol = stock.get('symbol', '')
            if '.' in symbol or not symbol:
                continue
            possibilities.append({
                "ticker": symbol,
                "name": stock.get('description', '')
            })

        return jsonify({"success": True, "data": possibilities})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500