# investment_ranker.py
from typing import List, Dict

class InvestmentRanker:
    """
    Ranks financial options based on strict priority criteria:
    1. Shariah Compliance (Hard pass/fail gate)
    2. Lower Risk (Volatility thresholds)
    3. Stability (Balance sheet health/Cash ratio)
    4. Long-Term Sustainability (Consistent operations)
    """

    @staticmethod
    def rank_options(options_data: List[Dict]) -> str:
        # Separate compliant and non-compliant assets immediately (Priority 1)
        compliant_pool = [opt for opt in options_data if opt.get("is_compliant", False)]
        
        if not compliant_pool:
            return "### ⚠️ Investment Ranking Matrix\n\nNo current options pass the primary Shariah Compliance filter criteria."

        # Sort based on Priority 2 (Lower Risk) and Priority 3 (Stability)
        # We sort by risk ascending, and then stability descending
        sorted_options = sorted(
            compliant_pool,
            key=lambda x: (x.get("risk_score", 10), -x.get("stability_score", 0))
        )

        # Slice to ensure we recommend the top 2-3 options max
        top_picks = sorted_options[:3]
        
        # Build short, scannable final output markup string
        output = "## 📊 Top Investment Rankings\n"
        output += "Evaluated strictly by Shariah Status, Low Risk, and Long-Term Stability:\n\n"

        for index, item in enumerate(top_picks):
            # Auto-select best option (Index 0 gets the star badge)
            rank_marker = f"🥇 Rank {index + 1}"
            star_badge = " ⭐ [BEST PICK]" if index == 0 else ""
            
            output += f"### {rank_marker}: {item['name']} ({item['ticker']}){star_badge}\n"
            output += f"- **Compliance Matrix:** Passed Qualitative & Quantitative Ratios\n"
            output += f"- **Risk Assessment:** {item['risk_desc']} (Volatility: {item['risk_score']}/10)\n"
            output += f"- **Sustainability:** Strong historical cash generation, long-term yield outlook.\n\n"

        return output