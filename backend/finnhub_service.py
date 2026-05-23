# finnhub_service.py
import os
import time
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

API_KEY = os.getenv('FINNHUB_API_KEY')


def get_live_price(ticker: str):
    """Legacy helper — kept so nothing else breaks."""
    quote = get_rich_market_quote(ticker)
    return quote["price"] if quote else None


def get_rich_market_quote(ticker: str) -> dict:
    url = f"https://finnhub.io/api/v1/quote?symbol={ticker.upper()}&token={API_KEY}"
    try:
        data = requests.get(url, timeout=5).json()
        if data.get('c'):
            current_price = data.get('c')
            open_price = data.get('o')
            
            # --- 1. Calculate "Price Difference" from Today's Open ---
            change_from_open = 0.0
            change_pct_from_open = 0.0
            if open_price and open_price > 0:
                change_from_open = round(current_price - open_price, 3) # The absolute difference
                change_pct_from_open = round((change_from_open / open_price) * 100, 2) # The %

            # --- 2. Determine Market Status ---
            ny_time = datetime.now(ZoneInfo('America/New_York'))
            is_weekday = ny_time.weekday() < 5
            is_open_hours = (ny_time.hour > 9 or (ny_time.hour == 9 and ny_time.minute >= 30)) and ny_time.hour < 16
            market_status = "Market Open" if (is_weekday and is_open_hours) else f"Market Closed (As of {ny_time.strftime('%b %d')})"

            return {
                "price": current_price,
                
                # SET 1: Compared to Previous Close (Native Finnhub Data)
                "change": round(data.get('d', 0.0), 3),                # Price Difference (e.g. -0.040)
                "changePercent": round(data.get('dp', 0.0), 2),        # Percentage (e.g. -0.36)
                
                # SET 2: Compared to Today's Open (Our Custom Math)
                "changeFromOpen": change_from_open,                    # Price Difference (e.g. -0.015)
                "changePercentFromOpen": change_pct_from_open,         # Percentage (e.g. -0.12)
                
                "marketStatus": market_status,
                "high": data.get('h'),
                "low": data.get('l'),
                "open": open_price,
                "previousClose": data.get('pc')
            }
        return None
    except Exception as e:
        print(f"❌ Quote error [{ticker}]: {e}")
        return None


def get_company_fundamentals(ticker: str) -> dict:
    """P/E ratio, market cap, net profit margin, debt-to-equity."""
    url = f"https://finnhub.io/api/v1/stock/metric?symbol={ticker.upper()}&metric=all&token={API_KEY}"
    try:
        metrics = requests.get(url, timeout=5).json().get('metric', {})
        return {
            "peRatio":         metrics.get('peAnnual') or metrics.get('peTTM') or 0.0,
            "marketCap":       metrics.get('marketCapitalization') or 0.0,
            "netProfitMargin": metrics.get('netProfitMarginAnnual') or metrics.get('netProfitMarginTTM') or 0.0,
            "debtToEquity":    metrics.get('totalDebt/totalEquityAnnual') or 0.0,
        }
    except Exception as e:
        print(f"❌ Fundamentals error [{ticker}]: {e}")
        return {"peRatio": 0.0, "marketCap": 0.0, "netProfitMargin": 0.0, "debtToEquity": 0.0}


def get_historical_candles(ticker: str, days: int = 30) -> list:
    """Daily closing prices for the past `days` days, formatted for charting."""
    end_time   = int(time.time())
    start_time = int((datetime.now() - timedelta(days=days)).timestamp())

    url = (
        f"https://finnhub.io/api/v1/stock/candle"
        f"?symbol={ticker.upper()}&resolution=D"
        f"&from={start_time}&to={end_time}&token={API_KEY}"
    )
    try:
        data = requests.get(url, timeout=5).json()
        if data.get('s') == 'ok':
            return [
                {"date": datetime.fromtimestamp(t).strftime('%Y-%m-%d'), "value": c}
                for t, c in zip(data.get('t', []), data.get('c', []))
            ]
        return []
    except Exception as e:
        print(f"❌ Candles error [{ticker}]: {e}")
        return []