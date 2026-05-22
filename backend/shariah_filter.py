import os
import requests

class shariahfilter:
    def __init__(self):
        # The API key is grabbed automatically
        self.api_key = os.getenv('FINNHUB_API_KEY')
        
        # The "No-Go" Business Sectors
        self.forbidden_keywords = [
            "bank", "banking", "insurance", "takaful", "finance", "credit", "interest", "riba",
            "gambling", "gaming", "casino", "lottery", "betting", "maysir",
            "alcohol", "beer", "wine", "brewery", "distillery", "tobacco", "cigarette", "vape",
            "pork", "bacon", "pornography", "nightclub", "cinema", "entertainment", "weapon", "military"
        ]

    def check_compliance(self, ticker: str) -> dict:
        """
        The Ultimate Screener: Fetches live Finnhub data and runs both
        Qualitative (Sector) and Quantitative (Debt) Shariah checks.
        """
        ticker = ticker.upper()
        
        try:
            # --- STEP 1: FETCH LIVE DATA FROM FINNHUB ---
            # Get Company Profile (to see what they do)
            profile_url = f"https://finnhub.io/api/v1/stock/profile2?symbol={ticker}&token={self.api_key}"
            profile_data = requests.get(profile_url).json()
            
            # Get Financial Metrics (to see their debt)
            metric_url = f"https://finnhub.io/api/v1/stock/metric?symbol={ticker}&metric=all&token={self.api_key}"
            metric_data = requests.get(metric_url).json()

            # --- STEP 2: QUALITATIVE CHECK (Business Activity) ---
            industry = profile_data.get('finnhubIndustry', '').lower()
            company_name = profile_data.get('name', '').lower()
            combined_text = f"{industry} {company_name}"
            
            # Allow Islamic banks
            if "islamic" not in combined_text and "takaful" not in combined_text:
                for keyword in self.forbidden_keywords:
                    if keyword in combined_text:
                        return {
                            "isHalal": False, 
                            "reason": f"Qualitative Failure: Involved in forbidden sector ({keyword})."
                        }

            # --- STEP 3: QUANTITATIVE CHECK (Financial Ratios) ---
            metrics = metric_data.get('metric', {})
            debt_to_equity = metrics.get('totalDebt/totalEquityAnnual')
            
            if debt_to_equity is None:
                return {
                    "isHalal": False, 
                    "reason": "Financial data unavailable. Cannot verify compliance safely."
                }
                
            if debt_to_equity > 33.33:
                return {
                    "isHalal": False, 
                    "reason": f"Quantitative Failure: Debt ratio is {round(debt_to_equity, 2)}% (Exceeds 33.33% limit)."
                }

            # --- STEP 4: PASS VERDICT ---
            return {
                "isHalal": True, 
                "reason": f"Halal. Passes business screening and debt ratios ({round(debt_to_equity, 2)}%)."
            }
            
        except Exception as e:
            print(f"❌ Error screening {ticker}: {e}")
            return {"isHalal": False, "reason": "API Connection Error"}

# Example of how to use it instantly:
# filter = shariahfilter()
# result = filter.check_compliance("AAPL")