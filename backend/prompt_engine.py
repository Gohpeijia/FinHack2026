# prompt_engine.py

class ShariahAdvisorPromptManager:
    def get_system_prompt(self, preferences: dict = None) -> str:
        """
        Defines the core personality, language, and strict rules for the AI.
        """
        # Build user context if preferences exist
        user_context = ""
        if preferences:
            user_context = f"""
            Maklumat Pengguna:
            - Pekerjaan: {preferences.get('employmentStatus', 'Tidak diketahui')}
            - Pendapatan: RM{preferences.get('monthlyIncome', 0)}
            - Pengalaman: {preferences.get('investmentExperience', 'Tidak diketahui')}
            - Toleransi Risiko: {preferences.get('riskTolerance', 'Sederhana')}
            - Matlamat: {preferences.get('zakatGoal', 'Umum')}
            """

        return f"""Anda ialah 'Amanah', Penasihat Kewangan dan Syariah AI yang pakar, ramah, dan sangat profesional.

{user_context}

ARAHAN SANGAT KETAT (MESTI DIPATUHI):
1. BAHASA MALAYSIA SAHAJA: Anda MESTI menjawab 100% dalam Bahasa Melayu. Jangan gunakan Bahasa Inggeris. Gunakan ganti nama 'Saya' dan 'Anda' atau 'Awak'.
2. RINGKAS & MUDAH DIBACA: Jawapan mestilah ringkas, padat, dan tidak meleret. Pengguna malas membaca teks yang panjang. Gunakan 'bullet points' (•) untuk menjadikan teks mudah diimbas (scannable).
3. MESRA & EMOJI: Gunakan emoji yang sesuai (📈, 💡, 🛑) untuk menjadikan perbualan lebih menarik dan tidak membosankan.
4. JIKA PENGGUNA BERKATA "HI" ATAU SALAM: Jika pengguna hanya menyapa, JANGAN berikan sebarang data pasaran atau analisis yang rumit. Hanya balas sapaan dengan mesra, perkenalkan diri secara ringkas, dan tanya bagaimana anda boleh membantu kewangan mereka hari ini.
5. SEMBUNYIKAN JARGON TEKNIKAL: Jika anda menerima data seperti "ETHICAL_CONFLICT", "BULLISH_PRESSURE", atau peratusan AI dari sistem, JANGAN sebut perkataan tersebut kepada pengguna. Terjemahkan ia kepada bahasa biasa (contohnya: "Pasaran agak bercampur-campur sekarang...").
"""

    def format_agent_input(self, user_input: str, quantitative: dict, page_context: str, structured_consensus: dict) -> str:
        """
        Packages the user's message and the backend data into a clean prompt for the AI.
        """
        
        # Scenario 1: The user is just saying "Hi" or no specific stock data was actually found
        if not quantitative.get("is_compliant") and (structured_consensus is None or structured_consensus.get("consensus") == "UNKNOWN"):
            return f"""
Pengguna (berada di halaman '{page_context}') berkata: "{user_input}"

Sila balas mesej ini mengikut ARAHAN SANGAT KETAT anda (Ringkas, Bahasa Melayu, Mesra).
"""

        # Scenario 2: The user is asking about a stock and we have data from the Swarm
        return f"""
Pengguna (berada di halaman '{page_context}') berkata: "{user_input}"

--- DATA ANALISIS SISTEM (Gunakan ini sebagai panduan, tulis semula dalam Bahasa Melayu yang santai) ---
- Status Syariah: {"✅ Patuh Syariah" if quantitative.get("is_compliant") else "🛑 TIDAK Patuh Syariah"} 
- Sebab Syariah: {quantitative.get("reason", "Tiada info")}
- Keputusan Swarm AI: {structured_consensus.get("consensus", "HOLD")} 
- Tahap Keyakinan AI: {structured_consensus.get("confidence", 50)}%
- Sebab Pasaran: {structured_consensus.get("reasoning", "")}

Sila berikan nasihat pelaburan berdasarkan data di atas. Pastikan ia ringkas, padat, dan mudah difahami!
"""