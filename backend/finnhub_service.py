import os
import requests

def get_live_price(ticker):
    api_key = os.getenv('FINNHUB_API_KEY')
    url = f"https://finnhub.io/api/v1/quote?symbol={ticker.upper()}&token={api_key}"

    try:
        response = requests.get(url)
        data = response.json()
        
        # Finnhub returns the current price under the key 'c'
        if 'c' in data and data['c'] != 0:
            return data['c']
        return None
    except Exception as e:
        print(f"❌ Error fetching price for {ticker}: {e}")
        return None