class ZakatManager:
    # ... your existing methods ...

    def get_reminder_message(self, name: str, amount: float, days_left: int):
        """
        Returns a formatted reminder string based on the time remaining.
        Returns None if no reminder is needed.
        """
        if days_left < 0:
            return f"Assalamualaikum {name} 👋\n\n🔔 Zakat Reminder: Your zakat of RM{amount:,.2f} is **overdue**."
            
        elif days_left == 0:
            return f"Assalamualaikum {name} 👋\n\n🔔 Zakat Reminder: Your zakat of RM{amount:,.2f} is due **TODAY**."
            
        elif 0 < days_left <= 7:
        # Check if it is singular (1 day) or plural (2-7 days)
        day_text = "1 day" if days_left == 1 else f"{days_left} days"
        return f"Assalamualaikum {name} 👋\n\n🔔 Zakat Reminder: Your zakat of RM{amount:,.2f} is due in {day_text}."
            
        return None # No reminder needed