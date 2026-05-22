import os
import requests

MAX_DEBT_RATIO = 33.33

def check_shariah_compliance(ticker):
    """
    100% Dynamic Filter: Checks real-time debt-to-equity ratios.
    Islamic Finance Rule: Total Debt should not exceed 33%.
    """
    api_key = os.getenv('FINNHUB_API_KEY')
    url = f"https://finnhub.io/api/v1/stock/metric?symbol={ticker.upper()}&metric=all&token={api_key}"

    try:
        response = requests.get(url)
        data = response.json()
        
        metrics = data.get('metric', {})
        debt_to_equity = metrics.get('totalDebt/totalEquityAnnual')

        # Run the dynamic check
        if debt_to_equity is not None:
            if debt_to_equity > MAX_DEBT_RATIO:
                return {"isHalal": False, "reason": f"Haram. Debt ratio {round(debt_to_equity, 2)}% > {MAX_DEBT_RATIO}% limit."}
            else:
                return {"isHalal": True, "reason": f"Halal. Passes debt screening ({round(debt_to_equity, 2)}%)."}
        
        # If the company hasn't reported debt to the SEC/Finnhub, we must reject it to be safe.
        return {"isHalal": False, "reason": "Financial data unavailable. Cannot verify compliance."}
        
    except Exception as e:
        print(f"❌ Error fetching metrics for {ticker}: {e}")
        return {"isHalal": False, "reason": "API Connection Error"}