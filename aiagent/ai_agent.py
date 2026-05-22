import os
import time
import requests
from utils import clean_text, detect_missing_info
from prompt_engine import ShariahAdvisorPromptManager
from savings_advisor import SavingsAdvisor
from mirofish_loop import SwarmSimulationEngine
from shariah_checker import ShariahChecker
from investment_ranker import InvestmentRanker

from backend.shariah_filter import check_shariah_compliance

class AIAgent:
    def __init__(self):
        groq_key = os.getenv("GROQ_API_KEY")
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")

        self.providers = []

        # 1. GROQ (Primary)
        if groq_key:
            self.providers.append({
                "name": "Groq",
                "url": "https://api.groq.com/openai/v1/chat/completions",
                "headers": {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                "model": "llama-3.3-70b-versatile" 
            })

        # 2. OPENROUTER: GROK
        if openrouter_key:
            self.providers.append({
                "name": "Grok (OpenRouter)",
                "url": "https://openrouter.ai/api/v1/chat/completions",
                "headers": {"Authorization": f"Bearer {openrouter_key}", "Content-Type": "application/json"},
                "model": "xai/grok-2-1212"
            })

        # 3. OPENROUTER: QWEN
        if openrouter_key:
            self.providers.append({
                "name": "Qwen 3.6 (OpenRouter)",
                "url": "https://openrouter.ai/api/v1/chat/completions",
                "headers": {"Authorization": f"Bearer {openrouter_key}", "Content-Type": "application/json"},
                "model": "qwen/qwen-max"
            })

        # 4. GOOGLE AI STUDIO: GEMINI
        if gemini_key:
            self.providers.append({
                "name": "Gemini 2.5 Flash (Google AI Studio)",
                "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
                "headers": {"Authorization": f"Bearer {gemini_key}", "Content-Type": "application/json"},
                "model": "gemini-2.5-flash"
            })

        if not self.providers:
            print("🚨 WARNING: No AI API keys found in .env! The AI Agent will fail.")

        self.prompt_engine = ShariahAdvisorPromptManager()
        self.savings_advisor = SavingsAdvisor()
        self.mirofish = SwarmSimulationEngine()
        self.shariah = ShariahChecker()
        self.rank_engine = InvestmentRanker()

    def process(self, user_input: str, ticker: str = None):
        user_input = clean_text(user_input)
        missing = detect_missing_info(user_input)
        
        missing_context = ""
        if missing:
            missing_items = ", ".join(missing)
            missing_context = f"\n\nCRITICAL INSTRUCTION: The user forgot to provide: {missing_items}. In your response, politely ask them to provide this information so you can give better advice."

        system_prompt = self.prompt_engine.get_system_prompt()
        savings_options = self.savings_advisor.get_recommendations()

        is_compliant = False
        debt_ratio = 0.0
        reason = "No specific stock analyzed."
        
        if ticker:
            compliance_data = check_shariah_compliance(ticker)
            is_compliant = compliance_data.get("isHalal", False)
            reason = compliance_data.get("reason", "Unknown")
            debt_ratio = 15.0 if is_compliant else 45.0 

        mirofish_insights = self.mirofish.execute_parallel_rehearsal(
            ticker=ticker or "General Portfolio", 
            audit_data={"is_compliant": is_compliant, "cash_ratio": 20, "debt_ratio": debt_ratio}
        )

        quantitative = {
            "is_compliant": is_compliant, 
            "reason": reason
        }

        raw_investments = self._generate_investment_pool()
        for item in raw_investments:
            item["is_compliant"] = is_compliant
        ranked_output = self.rank_engine.rank_options(raw_investments)

        return self.build_final_response(
            user_input, 
            system_prompt, 
            savings_options, 
            ranked_output, 
            mirofish_insights, 
            quantitative,
            missing_context
        )

    def build_final_response(self, user_input, system_prompt, savings, investments, insights, shariah_result, missing_context=""):
        prompt_content = f"""
        User Query: {user_input}
        Real-Time Shariah Data: {shariah_result}
        Market Context (Mirofish): {insights}
        {missing_context}
        
        Using the System Rules, generate the final response.
        """
        
        errors = []
        
        # 🔄 THE FALLBACK LOOP USING RAW REST CALLS
        for provider in self.providers:
            try:
                print(f"🌐 [AIAgent] Routing raw HTTP request to: {provider['name']}...")
                
                # Construct the standard OpenAI JSON payload manually
                payload = {
                    "model": provider["model"],
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt_content}
                    ],
                    "temperature": 0.2
                }
                
                # Make the raw request
                response = requests.post(provider["url"], headers=provider["headers"], json=payload, timeout=20)
                
                # Throw an error if the server rejected the request
                response.raise_for_status()
                
                # Parse the JSON and extract the text
                data = response.json()
                final_advice = data["choices"][0]["message"]["content"]
                
                print(f"✅ [AIAgent] Success! Response generated by {provider['name']}")

                return {
                    "status": "SUCCESS",
                    "final_advice": final_advice, 
                    "raw_data": {                 
                        "savings": savings,
                        "investments": investments,
                        "shariah_status": shariah_result
                    }
                }
                
            except Exception as e:
                err_msg = f"{provider['name']} failed: {str(e)}"
                print(f"❌ [AIAgent] {err_msg}")
                errors.append(err_msg)
                time.sleep(1) # Small 1-second buffer

        return {
            "status": "ERROR",
            "final_advice": "I am currently experiencing high network traffic across all my cloud providers. Please try again in a few moments.",
            "error_details": errors
        }