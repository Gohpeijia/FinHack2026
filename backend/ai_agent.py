import os
import asyncio
import time
import requests
from prompt_engine import ShariahAdvisorPromptManager
from shariah_filter import shariahfilter
from mirofish_loop import SwarmSimulationEngine
from consensus_engine import calculate_swarm_consensus


class AIAgent:
    def __init__(self):
        groq_key       = os.getenv("GROQ_API_KEY")
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        gemini_key     = os.getenv("GEMINI_API_KEY")

        self.providers = []

        if groq_key:
            self.providers.append({
                "name":    "Groq",
                "url":     "https://api.groq.com/openai/v1/chat/completions",
                "headers": {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                "model":   "llama-3.3-70b-versatile",
            })

        if openrouter_key:
            self.providers.append({
                "name":    "Grok (OpenRouter)",
                "url":     "https://openrouter.ai/api/v1/chat/completions",
                "headers": {"Authorization": f"Bearer {openrouter_key}", "Content-Type": "application/json"},
                "model":   "xai/grok-2-1212",
            })

        if openrouter_key:
            self.providers.append({
                "name":    "Qwen (OpenRouter)",
                "url":     "https://openrouter.ai/api/v1/chat/completions",
                "headers": {"Authorization": f"Bearer {openrouter_key}", "Content-Type": "application/json"},
                "model":   "qwen/qwen-max",
            })

        if gemini_key:
            self.providers.append({
                "name":    "Gemini 2.5 Flash (Google AI Studio)",
                "url":     "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
                "headers": {"Authorization": f"Bearer {gemini_key}", "Content-Type": "application/json"},
                "model":   "gemini-2.5-flash",
            })

        if not self.providers:
            print("🚨 WARNING: No AI API keys found in .env! The AI Agent will fail.")

        self._consensus_history: dict = {}
        self.prompt_engine  = ShariahAdvisorPromptManager()
        self.shariah        = shariahfilter()

        # FIX #1: Single SwarmSimulationEngine instance, reused every call.
        # The old code created self.swarm_engine here AND a second local one
        # inside process() on every request — the __init__ copy was dead weight.
        self.swarm_engine = SwarmSimulationEngine()

    def process(
        self,
        user_input:         str,
        ticker:             str  = None,
        chat_history:       list = None,
        page_context:       str  = "Unknown",
        preferences:        dict = None,
        previous_consensus: dict = None,
    ):
        if previous_consensus is None and ticker:
            previous_consensus = self._consensus_history.get(ticker)

        system_prompt = self.prompt_engine.get_system_prompt(preferences)

        is_compliant = False
        reason       = "No specific stock analyzed."
        cash_ratio   = 15.0
        debt_ratio   = 20.0

        if ticker:
            compliance_data = self.shariah.check_compliance(ticker)
            is_compliant    = compliance_data.get("isHalal", False)
            reason          = compliance_data.get("reason", "Unknown")
            cash_ratio      = compliance_data.get("cash_ratio", 15.0)
            debt_ratio      = compliance_data.get("debt_ratio", 20.0)

        quantitative = {
            "is_compliant": is_compliant,
            "reason":       reason,
            "cash_ratio":   cash_ratio,
            "debt_ratio":   debt_ratio,
        }

        # FIX #3: Use try/finally so loop.close() is ALWAYS called,
        # even when run_until_complete() raises an exception.
        # The old code called loop.close() only in the happy path — a loop
        # leak on every swarm failure.
        raw_swarm_results = []
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            raw_swarm_results = loop.run_until_complete(
                # FIX #1 continued: reuse self.swarm_engine instead of
                # constructing a throwaway SwarmSimulationEngine() here.
                self.swarm_engine.execute_rehearsal(ticker or "MARKET", quantitative)
            )
        except Exception as e:
            print(f"⚠️ Swarm Execution Failed: {e}")
        finally:
            loop.close()

        structured_consensus = calculate_swarm_consensus(
            raw_swarm_results,
            previous_consensus=previous_consensus,
        )
        print(
            f"📊 Swarm Consensus Reached: {structured_consensus['consensus']} "
            f"at {structured_consensus['confidence']}%"
        )

        if ticker:
            self._consensus_history[ticker] = structured_consensus

        prompt_content = self.prompt_engine.format_agent_input(
            user_input, quantitative, page_context, structured_consensus
        )

        return self.build_final_response(
            system_prompt,
            prompt_content,
            chat_history,
            quantitative,
        )

    def build_final_response(self, system_prompt, prompt_content, chat_history, shariah_result):
        messages = [{"role": "system", "content": system_prompt}]

        if chat_history:
            for msg in chat_history[-6:]:
                role = "assistant" if msg["role"] == "ai" else "user"
                messages.append({"role": role, "content": msg["content"]})

        messages.append({"role": "user", "content": prompt_content})

        errors = []

        for provider in self.providers:
            try:
                print(f"🌐 [AIAgent] Routing to: {provider['name']}...")

                payload = {
                    "model":       provider["model"],
                    "messages":    messages,
                    "temperature": 0.2,
                }

                response = requests.post(
                    provider["url"],
                    headers=provider["headers"],
                    json=payload,
                    timeout=20,
                )
                response.raise_for_status()

                data         = response.json()
                final_advice = data["choices"][0]["message"]["content"]
                print(f"✅ [AIAgent] Success via {provider['name']}")

                return {
                    "status":       "SUCCESS",
                    "final_advice": final_advice,
                    "raw_data":     {"shariah_status": shariah_result},
                }

            except Exception as e:
                err_msg = f"{provider['name']} failed: {str(e)}"
                print(f"❌ [AIAgent] {err_msg}")
                errors.append(err_msg)
                # FIX #2: `import time` was re-imported here on every retry
                # iteration. time is already imported at the top of the file.
                time.sleep(1)

        return {
            "status":       "ERROR",
            "final_advice": "I am currently experiencing high network traffic across all my cloud providers. Please try again in a few moments.",
            "error_details": errors,
        }