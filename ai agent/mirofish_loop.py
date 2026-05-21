# mirofish_loop.py
from typing import List, Dict

class SwarmSimulationEngine:
    """
    Simulates a decentralized market discussion (MiroFish framework) where multiple
    specialized financial personas react simultaneously to corporate financial signals.
    """
    def __init__(self):
        # Updated specialized market agent personas matching your exact specifications
        self.personas = [
            {
                "role": "INVESTOR",
                "focus": "Profit Potential, Long-Term Growth, ROI, Risk & Safety, Valuation",
                "template": (
                    "Investor Matrix Stance: Valuation fundamentals tracking against an internal risk & safety threshold. "
                    "Long-term growth trajectory and return on investment (ROI) profit potential are evaluated at "
                    "a stability rating of {stability_score}% based on available balance sheet cash reserves."
                )
            },
            {
                "role": "RISK_ANALYST",
                "focus": "Volatility, Downside Risk, Capital Protection, Market Depth (Exit Ease), Inflation Eating Capital, Cash Access Speed",
                "template": (
                    "Risk Analysis Stance: Downside risk and volatility profiles are actively mapped to a market score of {risk_score}/10. "
                    "Capital protection priority flags interest-bearing debt ratio structures at {debt_ratio:.2f}%. "
                    "Evaluating market depth for exit ease and safeguards to prevent inflation eating capital."
                )
            },
            {
                "role": "MARKET_STRATEGIST",
                "focus": "Market Trend, Economic Condition, Demand & Momentum, Central Bank Policy, Historical P/E Ratios",
                "template": (
                    "Strategist Stance: Current corporate demand and momentum indicators match a global macro framework. "
                    "Analyzing underlying assets relative to historical P/E ratios and broader central bank policy conditions "
                    "to gauge macro economic condition alignment."
                )
            }
        ]

    def execute_parallel_rehearsal(self, ticker: str, audit_data: Dict) -> List[str]:
        """
        Executes a simulation loop across the new swarm personas using current financial indicators.
        Returns a structured array of advisory insights.
        """
        rehearsal_logs = []
        is_compliant = audit_data.get("is_compliant", False)
        cash_ratio = audit_data.get("cash_ratio", 0.0)
        debt_ratio = audit_data.get("debt_ratio", 0.0)

        # Map metrics to dynamic simulation indicators
        stability_score = int(cash_ratio)
        risk_score = 3 if debt_ratio < 25 else 6

        for persona in self.personas:
            # Inject corporate data variables into the agent's specific logic template
            log_entry = persona["template"].format(
                risk_score=risk_score,
                stability_score=stability_score,
                debt_ratio=debt_ratio
            )
            # Format the clean, scannable log string
            formatted_insight = f"**[{persona['role']}]** (Focus: {persona['focus']}) -> {log_entry}"
            rehearsal_logs.append(formatted_insight)

        return rehearsal_logs