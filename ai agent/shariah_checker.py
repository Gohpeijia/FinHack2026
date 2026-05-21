# shariah_checker.py

class ShariahChecker:
    def __init__(self):
        # RULE 1: THE "NO-GO" BUSINESS SECTORS
        self.forbidden_keywords = [
            "bank", "banking", "insurance", "takaful", "finance", "credit", "interest", "riba",
            "gambling", "gaming", "casino", "lottery", "betting", "maysir",
            "alcohol", "beer", "wine", "brewery", "distillery", "tobacco", "cigarette", "vape",
            "pork", "bacon", "pornography", "nightclub", "cinema", "entertainment", "weapon", "military"
        ]

    def check_business_description(self, description: str, sector: str) -> dict:
        """Qualitative filter scanning industry keywords for absolute No-Go activities."""
        combined_text = f"{str(sector).lower()} {str(description).lower()}"
        
        # Explicit Exception for Islamic banks/takaful operating inside financial sectors
        if "islamic" in combined_text or "takaful" in combined_text or "sukuk" in combined_text:
            return {"is_allowed": True, "matched_keyword": None}

        for keyword in self.forbidden_keywords:
            if keyword in combined_text:
                return {"is_allowed": False, "matched_keyword": keyword}
        return {"is_allowed": True, "matched_keyword": None}

    def evaluate_ratios(self, dirty_income: float, total_income: float, 
                        conventional_cash: float, conventional_debt: float, total_assets: float) -> dict:
        """Quantitative filter implementing the 5% Income limit and 33% Balance Sheet ratios."""
        
        # Rule 2: 5% Income Safety Limit
        dirty_income_pct = (dirty_income / total_income * 100) if total_income > 0 else 0
        if dirty_income_pct >= 5.0:
            return {
                "is_compliant": False,
                "reason": f"[HARAM] Non-Halal income is {dirty_income_pct:.2f}%, hitting or exceeding the 5% limit."
            }

        # Rule 3: 33% Balance Sheet Ratios
        if total_assets <= 0:
            return {"is_compliant": False, "reason": "[ERROR] Missing total asset data to compute ratios."}

        cash_ratio = (conventional_cash / total_assets) * 100
        debt_ratio = (conventional_debt / total_assets) * 100

        if cash_ratio >= 33.0:
            return {
                "is_compliant": False,
                "reason": f"[HARAM] Cash Ratio is {cash_ratio:.2f}%. Too much cash held in traditional interest bank accounts (Max 33%)."
            }
        if debt_ratio >= 33.0:
            return {
                "is_compliant": False,
                "reason": f"[HARAM] Debt Ratio is {debt_ratio:.2f}%. Interest-bearing loans exceed the 33% structural capacity rule."
            }

        return {
            "is_compliant": True,
            "reason": (
                f"[HALAL / COMPLIANT]\n"
                f"- Non-halal Revenue: {dirty_income_pct:.2f}% (Safe under 5%)\n"
                f"- Conventional Cash Ratio: {cash_ratio:.2f}% (Safe under 33%)\n"
                f"- Conventional Debt Ratio: {debt_ratio:.2f}% (Safe under 33%)"
            )
        }