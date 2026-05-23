# finnhub_service.py
import os
import time
import requests
from datetime import datetime, timedelta

API_KEY = os.getenv('FINNHUB_API_KEY')


def get_live_price(ticker: str):
    """Legacy helper — kept so nothing else breaks."""
    quote = get_rich_market_quote(ticker)
    return quote["price"] if quote else None


def get_rich_market_quote(ticker: str) -> dict:
    """Real-time price, change, change %, high, low, open, previous close."""
    url = f"https://finnhub.io/api/v1/quote?symbol={ticker.upper()}&token={API_KEY}"
    try:
        data = requests.get(url, timeout=5).json()
        if data.get('c'):
            return {
                "price":         data.get('c'),
                "change":        round(data.get('d',  0.0), 2),
                "changePercent": round(data.get('dp', 0.0), 2),
                "high":          data.get('h'),
                "low":           data.get('l'),
                "open":          data.get('o'),
                "previousClose": data.get('pc'),
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