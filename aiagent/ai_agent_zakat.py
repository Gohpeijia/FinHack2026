import google.generativeai as genai
from zakat import ZakatKnowledgeBase
from reminder import ZakatManager

class ZakatAgent:
    """
    The Zakat Control Center.
    Coordinates Zakat reminders (proactive) and knowledge explanations (reactive).
    """
    def __init__(self):
        # Initialize sub-modules
        self.kb = ZakatKnowledgeBase()
        self.reminder_engine = ZakatManager()
        
        # Initialize the classifier model for smart detection
        self.classifier_model = genai.GenerativeModel('gemini-1.5-flash')

    def detect_islamic_intent(self, user_input: str) -> bool:
        """
        Uses Gemini to semantically analyze if the user's intent is Islamic Finance.
        """
        prompt = f"""
        Analyze the following user input: "{user_input}"
        
        Is this query related to Islamic Finance concepts? 
        (Examples: Zakat, Riba, Takaful, Shariah compliance, Halal earnings, wealth purification).
        
        Answer ONLY 'YES' or 'NO'.
        """
        try:
            response = self.classifier_model.generate_content(prompt)
            return "YES" in response.text.upper()
        except Exception:
            return False

    def process_request(self, user_input: str, user_profile: dict):
        """
        Main execution point for Zakat-related tasks.
        
        user_profile expects: {"name": str, "zakat_amount": float, "days_left": int}
        """
        results = {
            "reminder": None,
            "explanation": None
        }

        # 1. PROACTIVE: Check for Zakat Reminder
        # This runs every time to see if the user needs a notification
        if user_profile:
            reminder = self.reminder_engine.get_reminder_message(
                name=user_profile.get("name", "User"),
                amount=user_profile.get("zakat_amount", 0.0),
                days_left=user_profile.get("days_left", 999) 
            )
            results["reminder"] = reminder

        # 2. REACTIVE: Check for Knowledge Request
        # This uses the Smart Detector to see if the user is asking about Zakat/Islamic Finance
        if self.detect_islamic_intent(user_input):
            results["explanation"] = self.kb.ask_gemini(user_input)
            
        return results