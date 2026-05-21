import openai # Ensure you have this installed
from utils import clean_text, detect_missing_info
from prompt_engine import ShariahAdvisorPromptManager
from savings_advisor import SavingsAdvisor
from mirofish_loop import SwarmSimulationEngine
from shariah_checker import ShariahChecker
from investment_ranker import InvestmentRanker

class AIAgent:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.prompt_engine = ShariahAdvisorPromptManager()
        self.savings_advisor = SavingsAdvisor()
        self.mirofish = SwarmSimulationEngine()
        self.shariah = ShariahChecker()
        self.rank_engine = InvestmentRanker()

    def process(self, user_input: str):
        # 1. UTILS
        user_input = clean_text(user_input)
        missing = detect_missing_info(user_input)
        if missing:
            return {"status": "NEED_MORE_INFO", "missing_fields": missing}

        # 2. PROMPT ENGINE
        system_prompt = self.prompt_engine.get_system_prompt()

        # 3. SAVINGS ADVISOR
        savings_options = self.savings_advisor.get_recommendations()

        # 4. MIROFISH LOOP
        mirofish_insights = self.mirofish.execute_parallel_rehearsal(
            ticker="USER_INPUT", 
            audit_data={"is_compliant": True, "cash_ratio": 25, "debt_ratio": 20}
        )

        # 5. SHARIAH CHECKER
        audit_result = self.shariah.check_business_description(user_input, "personal_finance")
        quantitative = self.shariah.evaluate_ratios(0, 100, 20, 10, 100)
        is_compliant = audit_result["is_allowed"] and quantitative["is_compliant"]

        # 6. INVESTMENT RANKING
        raw_investments = self._generate_investment_pool()
        for item in raw_investments:
            item["is_compliant"] = is_compliant
        ranked_output = self.rank_engine.rank_options(raw_investments)

        # 7. FINAL RESPONSE BUILDER (Now with LLM Call)
        return self.build_final_response(
            user_input, system_prompt, savings_options, ranked_output, mirofish_insights, quantitative
        )

    def build_final_response(self, user_input, system_prompt, savings, investments, insights, shariah_result):
        # 1. Ask the LLM to format the response according to your rules
        prompt_content = f"""
        User Query: {user_input}
        Ranked Investment Data: {investments}
        Market Context: {insights}
        
        Using the System Rules, generate the final response.
        """
        
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_content}
            ],
            temperature=0.2
        )
        
        final_advice = completion.choices[0].message.content

        # 2. Return structured dictionary for the team
        return {
            "status": "SUCCESS",
            "final_advice": final_advice, # The formatted text for the UI
            "raw_data": {                 # The data for the frontend graphs
                "savings": savings,
                "investments": investments,
                "shariah_status": shariah_result
            }
        }

    def _generate_investment_pool(self):
        # Keep your existing pool logic here
        return [
            {"name": "Islamic Global Equity Fund", "ticker": "IGE", "risk_score": 3, "risk_desc": "Low-Medium", "stability_score": 85},
            {"name": "Shariah Tech Growth ETF", "ticker": "STG", "risk_score": 5, "risk_desc": "Medium", "stability_score": 70}
        ]