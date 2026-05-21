# utils.py
import re

def clean_text(text: str) -> str:
    """Standardizes spacing and trims whitespace from inputs."""
    if not text:
        return ""
    return " ".join(text.split())

def detect_missing_info(user_input: str) -> list:
    """
    Scans the user query for your 5 specific criteria.
    Returns a list of missing strings if they are not found.
    """
    missing = []
    text = user_input.lower()
    
    # 1. Check for Current Status (working, studying, job, student, uni, etc.)
    if not re.search(r'(work|study|student|intern|job|uni|college|employ|fresh|grad)', text):
        missing.append("Current Status (working/studying)")
        
    # 2. Check for Budget (digits, RM, $, budget, invest, save, etc.)
    if not re.search(r'(\d+|budget|rm|\$|save|capital|amount|allocate)', text):
        missing.append("Budget (how much money is planning to be invest)")
        
    # 3. Check for Goals (earn, target, goal, return, profit, dividend, payout, etc.)
    if not re.search(r'(earn|goal|target|return|profit|dividend|payout|yield|make|gain)', text):
        missing.append("Goals (want to earn how much)")
        
    # 4. Check for Risk Profile (high, medium, low, aggressive, conservative, safe)
    if not re.search(r'(high|medium|low|risk|safe|aggressive|conservative|moderate)', text):
        missing.append("Risk Profile (High/medium/low)")
        
    # 5. Check for Time (year, month, long, short, hold, duration, horizon, etc.)
    if not re.search(r'(year|month|long|short|hold|duration|time|horizon|period|day)', text):
        missing.append("Time (want to invest how long)")
        
    return missing