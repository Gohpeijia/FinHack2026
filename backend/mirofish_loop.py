import os
import json
import asyncio
import aiohttp


class SwarmSimulationEngine:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

        self.personas = [
            {
                "id":          "ETHICAL_COMPLIANCE_OFFICER",
                "prompt":      "You are a strict Shariah compliance officer. Your ONLY concern is whether the debt ratio exceeds the 33% haram threshold. If it does, you must VETO. Analyze the data and output ONLY valid JSON.",
                "temperature": 0.1,
                "weight":      1.0,
            },
            {
                "id":          "CONSERVATIVE_PRESERVER",
                "prompt":      "You are a conservative wealth preserver. Priority is zero risk and capital protection. High debt terrifies you. Output ONLY valid JSON.",
                "temperature": 0.2,
                "weight":      0.8,
            },
            {
                "id":          "VALUE_SNIPER",
                "prompt":      "You look for fundamentally strong companies ignored by the market. You accept moderate debt if intrinsic value is high. Output ONLY valid JSON.",
                "temperature": 0.3,
                "weight":      0.7,
            },
            {
                "id":          "MOMENTUM_FOLLOWER",
                "prompt":      "You follow market trends and crowd sentiment. You buy when others buy, ignoring underlying risk if the hype is strong. Output ONLY valid JSON.",
                "temperature": 0.8,
                "weight":      0.5,
            },
            {
                "id":          "AGGRESSIVE_SPECULATOR",
                "prompt":      "You are a high-risk hedge fund trader. Maximize ROI. Ignore volatility. Tolerate high debt if growth is massive. Output ONLY valid JSON.",
                "temperature": 0.9,
                "weight":      0.4,
            },
        ]

        self.json_format_instructions = """
        You must respond with ONLY a JSON object in this exact format, with no markdown formatting or extra text:
        {
            "decision": "BUY",
            "confidence": 85,
            "reasoning": "1 sentence explaining why."
        }
        decision must be strictly one of: "BUY", "HOLD", "SELL", or "VETO".
        confidence must be an integer between 1 and 100.
        """

    def _clean_json_response(self, text: str) -> str:
        """Strips markdown code fences safely."""
        text = text.strip()
        if text.startswith("```json"):
            text = text.replace("```json", "", 1)
        elif text.startswith("```"):
            text = text.replace("```", "", 1)
        if text.endswith("```"):
            text = text[::-1].replace("```", "", 1)[::-1]
        return text.strip()

    def _validate_decision(self, data: dict, persona_id: str, weight: float) -> dict:
        """
        Strict schema validation — prevents LLM hallucinations from reaching
        the consensus engine. Enforces VALID_DECISIONS, numeric confidence bounds,
        and caps reasoning length.
        """
        VALID_DECISIONS = {"BUY", "HOLD", "SELL", "VETO"}

        decision = str(data.get("decision", "")).strip().upper()
        if decision not in VALID_DECISIONS:
            print(f"⚠️ [{persona_id}] Hallucinated decision '{decision}' → defaulting to HOLD")
            decision = "HOLD"

        try:
            confidence = int(data.get("confidence", 50))
            if not (1 <= confidence <= 100):
                confidence = 50
        except (ValueError, TypeError):
            confidence = 50

        return {
            "agent":     persona_id,
            "decision":  decision,
            "confidence": confidence,
            "reasoning": str(data.get("reasoning", ""))[:300],
            "weight":    weight,
        }

    async def _fetch_agent_opinion(self, session, persona, market_data, retries=3):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type":  "application/json",
        }

        messages = [
            {"role": "system", "content": persona["prompt"] + self.json_format_instructions},
            {"role": "user",   "content": f"Market Data for Asset: {market_data}"},
        ]

        payload = {
            "model":       "llama-3.3-70b-versatile",
            "messages":    messages,
            "temperature": persona["temperature"],
        }

        for attempt in range(retries):
            try:
                async with session.post(self.api_url, headers=headers, json=payload) as response:
                    response.raise_for_status()
                    result  = await response.json()
                    ai_text = result["choices"][0]["message"]["content"]

                    cleaned_text  = self._clean_json_response(ai_text)
                    raw_data      = json.loads(cleaned_text)

                    # FIX #1: _validate_decision() was defined but NEVER called.
                    # Raw JSON was injected directly into the pipeline, meaning
                    # hallucinated decisions like "STRONG BUY" or out-of-range
                    # confidence values reached consensus_engine unchecked.
                    return self._validate_decision(raw_data, persona["id"], persona["weight"])

            except Exception as e:
                if attempt == retries - 1:
                    print(f"❌ [{persona['id']}] Failed after {retries} attempts: {e}")
                    return {
                        "agent":      persona["id"],
                        "decision":   "ERROR",
                        "confidence": 0,
                        "reasoning":  "API Failure",
                        "weight":     persona["weight"],
                    }
                await asyncio.sleep(1)

    async def execute_rehearsal(self, ticker: str, audit_data: dict, user_goal: dict = None):
        print(f"🧠 [MiroFish] Orchestrating Swarm for {ticker}...")
        market_context = (
            f"Ticker: {ticker} | "
            f"Shariah Compliant: {audit_data.get('is_compliant')} | "
            f"Cash Ratio: {audit_data.get('cash_ratio')}% | "
            f"Debt Ratio: {audit_data.get('debt_ratio')}%"
        )

        if user_goal:
            progress = 0
            if user_goal.get('totalamount', 0) > 0:
                progress = round((user_goal.get('totalgatheredamount', 0) / user_goal.get('totalamount')) * 100, 1)
                
            market_context += (
                f" | USER FINANCIAL GOAL: '{user_goal.get('goaltitle')}' "
                f"(Target: RM{user_goal.get('totalamount')}, "
                f"Saved: RM{user_goal.get('totalgatheredamount')} [{progress}% Complete], "
                f"Deadline: {user_goal.get('date')})"
            )

        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks   = [asyncio.create_task(self._fetch_agent_opinion(session, persona, market_context)) for persona in self.personas]
            results = await asyncio.gather(*tasks)

        return results