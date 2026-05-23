# finnhub_service.py
import os
import time
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

API_KEY = os.getenv('FINNHUB_API_KEY')

# Maps frontend period strings → (resolution, days_back)
PERIOD_MAP = {
    '1D':  ('5',  1),
    '1W':  ('15', 7),
    '1M':  ('60', 30),
    '3M':  ('D',  90),
    '1Y':  ('D',  365),
    'ALL': ('W',  1825),  # ~5 years
}


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

            change_from_open = 0.0
            change_pct_from_open = 0.0
            if open_price and open_price > 0:
                change_from_open = round(current_price - open_price, 3)
                change_pct_from_open = round((change_from_open / open_price) * 100, 2)

            ny_time = datetime.now(ZoneInfo('America/New_York'))
            is_weekday = ny_time.weekday() < 5
            is_open_hours = (
                (ny_time.hour > 9 or (ny_time.hour == 9 and ny_time.minute >= 30))
                and ny_time.hour < 16
            )
            market_status = (
                "Market Open"
                if (is_weekday and is_open_hours)
                else f"Market Closed (As of {ny_time.strftime('%b %d')})"
            )

            return {
                "price": current_price,
                "change": round(data.get('d', 0.0), 3),
                "changePercent": round(data.get('dp', 0.0), 2),
                "changeFromOpen": change_from_open,
                "changePercentFromOpen": change_pct_from_open,
                "marketStatus": market_status,
                "high": data.get('h'),
                "low": data.get('l'),
                "open": open_price,
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


def get_historical_candles(ticker: str, period: str = '1Y') -> list:
    """
    OHLCV candles for the given period string ('1D','1W','1M','3M','1Y','ALL').
    Returns [{ date, value }] formatted for the frontend chart.
    """
    resolution, days = PERIOD_MAP.get(period, ('D', 365))
    end_time   = int(time.time())
    start_time = int((datetime.now() - timedelta(days=days)).timestamp())

    url = (
        f"https://finnhub.io/api/v1/stock/candle"
        f"?symbol={ticker.upper()}&resolution={resolution}"
        f"&from={start_time}&to={end_time}&token={API_KEY}"
    )
    try:
        data = requests.get(url, timeout=8).json()
        if data.get('s') == 'ok':
            timestamps = data.get('t', [])
            closes     = data.get('c', [])

            # Format label based on resolution
            if resolution in ('5', '15', '60'):
                fmt = '%H:%M'
            else:
                fmt = '%b %d' if days <= 90 else '%b %Y'

            return [
                {"date": datetime.fromtimestamp(t).strftime(fmt), "value": c}
                for t, c in zip(timestamps, closes)
            ]
        return []
    except Exception as e:
        print(f"❌ Candles error [{ticker}]: {e}")
        return []