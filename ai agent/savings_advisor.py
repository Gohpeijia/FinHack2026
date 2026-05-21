class SavingsAdvisor:
    """
    Provides curated, Shariah-compliant savings options for Malaysian users.
    Focuses on Islamic digital banks and Shariah-compliant money market funds.
    """
    
    def get_recommendations(self):
        return {
            "Digital Banks": [
                {
                    "name": "AEON Bank Savings Pot",
                    "rate": "3.00% p.a.",
                    "compliance": "Fully Shariah-Compliant (Islamic Digital Bank)",
                    "benefit": "PIDM protected, no minimum balance, seamless app integration."
                },
                {
                    "name": "KAF Digital Bank",
                    "rate": "5.00% (on first RM2k)",
                    "compliance": "100% Shariah-Compliant",
                    "benefit": "Excellent entry-level yield for beginners with small balances."
                }
            ],
            "Growth & Yield": [
                {
                    "name": "Moomoo Cash Plus",
                    "rate": "~3.50% p.a.",
                    "compliance": "Shariah-Compliant Money Market Funds",
                    "benefit": "Daily profit accrual; liquid and perfect for transitioning to investing."
                }
            ]
        }