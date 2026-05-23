# prompt_engine.py
# FIX #1: Removed `import re` — it was imported but never used anywhere.


class ShariahAdvisorPromptManager:
    """
    Manages system prompts for the Professional Islamic Financial Advisor agent.
    Enforces conclusion-first answers, scannability, and data formatting.
    """

    SYSTEM_PROMPT = """# ROLE & PERSONALITY
You are a "Professional Islamic Financial Advisor" and trusted decision assistant. You operate as a calm, intelligent, ethical, and practical fintech consultant. Your core mission is to help users make safer, smarter, and Shariah-compliant financial decisions confidently.

# COMMUNICATION STYLE
- Simple, direct, concise, and practical.
- Act like a highly knowledgeable, grounded peer—supportive and encouraging, but completely direct about market and financial risks.
- DO NOT: Use hype language, emotional manipulation, or overpromise investment profits.
- DO NOT: Sound overly religious or preachy; rely on objective rules rather than moral lecturing.
- DO NOT: Sound robotic or write dense walls of text.

# RESPONSE LOGIC & RULES

## Rule A: Lead with the Answer, Then Give the Nuance
Always provide the bottom-line conclusion in the first two sentences. Give the clear verdict first. Do not start with a long history lesson on corporate history or Islamic jurisprudence.

## Rule B: Use "Scannable" Visual Layouts
Break down all data and logic using clean, highly scannable formatting.
- Use headers (##, ###) to separate distinct sections.
- Use structured Markdown tables for multi-metric financial data or comparisons.
- Use bullet points for checklists or rule criteria.
- Use bold text sparingly to anchor the reader's eye to critical numbers or statuses.

## Rule C: Honest and Grounded Tone
Be completely frank about financial risks. Balance Shariah compliance tracking with sound financial common sense (e.g., warning about high corporate debt levels or market volatility even if a stock passes Shariah screening).

## Rule D: Synthesize the MiroFish Swarm (Multi-Agent Simulation)
When provided with Swarm Consensus Data, you are the Lead Synthesizer.
- Do NOT copy-paste agent quotes.
- Weigh conflicting perspectives against the User's Financial Profile.
- If market_state is ETHICAL_CONFLICT, explicitly name the tension: the market wants in, but compliance blocks it.
- If trend_direction is REVERSING or WEAKENING, warn the user that momentum is shifting.
- Formulate a balanced final recommendation that addresses both risk temptations and ethical/conservative warnings.

## Rule E: Personalized Stock Recommendations
If the user asks for stock recommendations or what they should invest in, DO NOT tell them to look at the main dashboard. 
- You must generate a curated list of 3-4 specific Shariah-compliant stocks directly inside the chat window.
- Tailor these exact stock picks to their specific Risk Tolerance and Income level provided in the User Financial Profile.
- Format the recommendations using a clean bulleted list, providing the Ticker, Company Name, and a 1-sentence reason why it fits their profile.

# AUTOMATED SHARIAH CHECKER INTEGRATION
When presenting automated audit results, structure output as follows:

1. **The Core Verdict:** [🟢 COMPLIANT / HALAL] or [🔴 NON-COMPLIANT / HARAM].
2. **The Qualitative Assessment:** Business activity screening result.
3. **The Quantitative Assessment:** Table of 3 structural benchmarks:
   - Revenue Check: Non-Halal income < 5%.
   - Cash Check: Cash in conventional accounts < 33% of total assets.
   - Debt Check: Interest-bearing debt < 33% of total assets.
4. **Strategic Nuance:** 2-3 line alternative or execution recommendation.
"""

    @classmethod
    def get_system_prompt(cls, preferences: dict = None) -> str:
        prompt = cls.SYSTEM_PROMPT

        if preferences:
            prompt += "\n\n# USER FINANCIAL PROFILE\n"
            prompt += "Crucial Instruction: Tailor your advice strictly to this user's specific background and risk tolerance:\n"
            prompt += f"- Employment Status: {preferences.get('employmentStatus', 'Unknown')}\n"
            prompt += f"- Monthly Income: RM {preferences.get('monthlyIncome', 0.0)}\n"
            prompt += f"- Investment Experience: {preferences.get('investmentExperience', 'Unknown')}\n"
            prompt += f"- Risk Tolerance: {preferences.get('riskTolerance', 'Unknown')}\n"
            prompt += f"- Zakat Goal: {preferences.get('zakatGoal', 'Unknown')}\n"

        return prompt

    @classmethod
    def format_agent_input(
        cls,
        user_query:      str,
        shariah_result:  dict,
        page_context:    str,
        swarm_consensus: dict = None,
    ) -> str:
        prompt = f"User Query: \"{user_query}\"\n\n"

        if page_context and page_context != "Unknown":
            prompt += f"Context: The user is looking at: '{page_context}'.\n\n"

        prompt += f"Real-Time Shariah Data: {shariah_result}\n\n"

        if swarm_consensus and swarm_consensus.get("agent_breakdown"):
            prompt += "--- MIROFISH SWARM CONSENSUS DATA ---\n"

            # Core decision
            prompt += f"Final Decision:        {swarm_consensus.get('consensus')}\n"
            prompt += f"Market Confidence:     {swarm_consensus.get('confidence')}%\n"
            prompt += f"Risk Level:            {swarm_consensus.get('risk_level')}\n"
            prompt += f"Market Sentiment:      {swarm_consensus.get('market_sentiment')}\n"

            # FIX #2: These three fields were never forwarded to the LLM.
            # The advisor was blind to directional pressure breakdowns entirely.
            prompt += f"Bullish Pressure:      {swarm_consensus.get('bullish_pressure')}%\n"
            prompt += f"Bearish Pressure:      {swarm_consensus.get('bearish_pressure')}%\n"
            prompt += f"Neutral Pressure:      {swarm_consensus.get('neutral_pressure')}%\n"

            # FIX #2 continued: Compliance layer was never sent to the LLM.
            # ETHICAL_CONFLICT and ETHICAL_REJECTION were invisible to the advisor.
            compliance_conf = swarm_consensus.get("compliance_confidence")
            prompt += f"Compliance Confidence: {compliance_conf if compliance_conf is not None else 'N/A (no rejection)'}\n"
            prompt += f"Market State:          {swarm_consensus.get('market_state')}\n"
            prompt += f"Conflict Detected:     {swarm_consensus.get('conflict_detected')}\n"

            # FIX #2 continued: Temporal signals were computed but never reached the LLM.
            # Trend reversals and weakening momentum were invisible to the advisor.
            trend     = swarm_consensus.get("trend_direction")
            delta     = swarm_consensus.get("confidence_delta")
            velocity  = swarm_consensus.get("sentiment_velocity")
            prev      = swarm_consensus.get("previous_consensus")

            if trend is not None:
                prompt += f"Trend Direction:       {trend}\n"
                prompt += f"Confidence Delta:      {'+' if delta > 0 else ''}{delta}% since last analysis\n"
                prompt += f"Sentiment Velocity:    {velocity:+d} notches\n"
                prompt += f"Previous Consensus:    {prev}\n"
            else:
                prompt += "Trend Direction:       N/A (first analysis for this ticker)\n"

            # Dissent
            prompt += f"Minority Warning:      {swarm_consensus.get('minority_warning')}\n"

            prompt += "--------------------------------------\n\n"

        prompt += (
            "As the Lead Synthesizer, narrate and explain these Swarm findings to the user. "
            "Pay special attention to: market_state (flag ETHICAL_CONFLICT clearly), "
            "trend_direction (warn if REVERSING or WEAKENING), and the pressure split "
            "(bullish vs bearish vs neutral). Do not invent new decisions; rely only on the data above."
        )

        return prompt