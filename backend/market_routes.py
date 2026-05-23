# market_routes.py
import os
import requests
from flask import Blueprint, jsonify, request
from security import require_auth
from shariah_filter import check_shariah_compliance
from finnhub_service import get_rich_market_quote, get_company_fundamentals, get_historical_candles

market_bp = Blueprint('market', __name__)


@market_bp.route('/details/<ticker>', methods=['GET'])
@require_auth
def get_stock_details(ticker):
    try:
        ticker = ticker.upper()

        is_halal     = check_shariah_compliance(ticker)
        quote        = get_rich_market_quote(ticker)

        if quote is None:
            return jsonify({
                "success": False,
                "error": f"Could not fetch price for {ticker}. Check the ticker symbol."
            }), 404

        fundamentals = get_company_fundamentals(ticker)
        chart_data   = get_historical_candles(ticker, days=30)

        return jsonify({
            "success": True,
            "data": {
                "ticker":          ticker,
                "price":           quote["price"],
                
                # --- The New Dual-Percentage Data ---
                "change":                quote["change"],
                "changePercent":         quote["changePercent"],
                "changeFromOpen":        quote["changeFromOpen"],
                "changePercentFromOpen": quote["changePercentFromOpen"],
                "marketStatus":          quote["marketStatus"],
                # ------------------------------------
                
                "high":            quote["high"],
                "low":             quote["low"],
                "open":            quote["open"],
                "previousClose":   quote["previousClose"],
                "peRatio":         fundamentals["peRatio"],
                "marketCap":       fundamentals["marketCap"],
                "netProfitMargin": fundamentals["netProfitMargin"],
                "debtToEquity":    fundamentals["debtToEquity"],
                "chartData":       chart_data,
                "isHalal":         is_halal["isHalal"],
                "complianceReason": is_halal["reason"],
            }
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@market_bp.route('/all', methods=['GET'])
@require_auth
def get_dynamic_halal_stocks():
    try:
        api_key = os.getenv('FINNHUB_API_KEY')
        limit   = int(request.args.get('limit', 15))

        all_symbols = requests.get(
            f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={api_key}"
        ).json()

        compliant_stocks = []
        for stock in all_symbols[:limit]:
            ticker = stock['displaySymbol']
            if '.' in ticker:
                continue

            compliance = check_shariah_compliance(ticker)
            if not compliance['isHalal']:
                continue

            quote = get_rich_market_quote(ticker)
            compliant_stocks.append({
                "ticker":        ticker,
                "name":          stock['description'],
                "price":         quote["price"]         if quote else None,
                "change":        quote["change"]        if quote else None,
                "changePercent": quote["changePercent"] if quote else None,
                "isHalal":       True,
                "reason":        compliance['reason'],
            })

        return jsonify({
            "success": True,
            "count":   len(compliant_stocks),
            "data":    compliant_stocks
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ✅ Only one definition of this route
@market_bp.route('/search', methods=['GET'])
@require_auth
def search_stock_possibilities():
    try:
        query = request.args.get('q', '').upper()
        if not query:
            return jsonify({"success": True, "data": []})

        api_key      = os.getenv('FINNHUB_API_KEY')
        search_results = requests.get(
            f"https://finnhub.io/api/v1/search?q={query}&token={api_key}"
        ).json().get('result', [])

        possibilities = []
        for stock in search_results[:10]:
            symbol = stock.get('symbol', '')
            if not symbol or '.' in symbol:
                continue
            possibilities.append({
                "ticker": symbol,
                "name":   stock.get('description', '')
            })

        return jsonify({"success": True, "data": possibilities})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500