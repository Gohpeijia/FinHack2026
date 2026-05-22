import google.generativeai as genai

class ZakatKnowledgeBase:
    def __init__(self):
        # Initialize the model once when the class is created
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def get_zakat_info(self):
        # Keep your static knowledge here
        return { ... }

    def ask_gemini(self, user_question):
        """
        Uses the already-initialized model to generate a response.
        """
        prompt = f"""
        You are an Islamic Finance AI Assistant.
        Follow these rules strictly:
        1. Answer simply for a beginner.
        2. Explain within an Islamic finance context.
        3. Start immediately with the format below:

        TERM: [The subject]
        Definition: [Concise definition]
        Simple Explanation: [Simple analogy]
        Shariah Status: [Halal/Haram/Mubah]
        Related Topics: [Topics]

        User Question/Term: {user_question}
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error retrieving information: {str(e)}"