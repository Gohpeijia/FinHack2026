from flask import Blueprint, jsonify, request, g
from security import require_auth
from zakat_service import get_current_nisab
from firebase_config import db
from datetime import datetime

zakat_bp = Blueprint('zakat', __name__)

# --- 1. ZAKAT FITRAH ---
@zakat_bp.route('/fitrah/calculate', methods=['POST'])
@require_auth
def calculate_fitrah():
    try:
        data = request.json
        state_rate = float(data.get('rate', 7.0)) 
        family_members = int(data.get('family_members', 1))
        
        total_fitrah = state_rate * family_members
        
        return jsonify({
            "success": True,
            "data": {
                "total_fitrah": total_fitrah,
                "deadline": "Before Eid al-Fitr prayers",
                "status": "UNPAID"
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# --- 2. ZAKAT HARTA & NISAB (The 10/10 Version) ---
@zakat_bp.route('/harta/calculate', methods=['POST'])
@require_auth
def calculate_harta():
    try:
        data = request.json
        
        # ISSUE 6: Strict Input Validation
        try:
            total_assets = float(data.get('total_assets', 0))
            liabilities = float(data.get('liabilities', 0))
            months_above_nisab = int(data.get('months_above_nisab', 0))
        except ValueError:
            return jsonify({"success": False, "error": "Invalid data format. Numbers required."}), 400
            
        if total_assets < 0 or liabilities < 0 or months_above_nisab < 0:
            return jsonify({"success": False, "error": "Values cannot be negative."}), 400
        
        # Core Financial Math
        eligible_wealth = max(0, total_assets - liabilities)
        current_nisab = get_current_nisab()
        
        above_nisab = eligible_wealth >= current_nisab
        haul_completed = months_above_nisab >= 12
        zakat_obligatory = above_nisab and haul_completed
        
        zakat_due = round(eligible_wealth * 0.025, 2) if zakat_obligatory else 0.0
        
        # Cleaner Status Logic
        if not above_nisab:
            status = "BELOW_NISAB"
        elif above_nisab and not haul_completed:
            status = "ABOVE_NISAB_NO_HAUL"
        else:
            status = "ELIGIBLE_FOR_ZAKAT"
            
        # ISSUE 4: Detailed Explanation Object for Frontend Storytelling
        nisab_progress = min(100, int((eligible_wealth / current_nisab) * 100)) if current_nisab > 0 else 0
        wealth_gap = round(max(0, current_nisab - eligible_wealth), 2)
        months_remaining = max(0, 12 - months_above_nisab) if above_nisab else 12
        
        # THE BIG IMPROVEMENT: AI Financial Health Score (Gamification)
        haul_progress = min(100, int((months_above_nisab / 12) * 100))
        
        # Calculate a fun "Readiness Score" based on how close they are to obligation
        if not above_nisab:
            readiness_score = int(nisab_progress * 0.8) # Cap at 80 if they haven't hit Nisab
        else:
            readiness_score = min(100, int((nisab_progress + haul_progress) / 2))
            
        health_status = "Good Progress" if readiness_score > 50 else "Building Foundation"
        if zakat_obligatory:
            health_status = "Zakat Obligatory - Action Required"

        return jsonify({
            "success": True,
            "data": {
                "above_nisab": above_nisab,
                "haul_completed": haul_completed,
                "zakat_obligatory": zakat_obligatory,
                "nisab": current_nisab,
                "wealth": eligible_wealth,
                "progress_percentage": nisab_progress,
                "zakat_due": zakat_due,
                "status": status,
                "explanation": {
                    "months_remaining": months_remaining,
                    "required_wealth_for_nisab": current_nisab,
                    "current_wealth_gap": wealth_gap
                },
                "financial_health": {
                    "zakat_readiness_score": readiness_score,
                    "status": health_status
                }
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@zakat_bp.route('/save', methods=['POST'])
@require_auth
def save_zakat_record():
    try:
        data = request.json
        user_id = g.uid
        
        if not user_id:
            return jsonify({"success": False, "error": "Missing userId"}), 400

        # Create the historical record payload
        new_record = {
            "timestamp": datetime.now().isoformat(),
            "type": data.get("type", "Zakat Harta"),
            "wealth": float(data.get("wealth", 0)),
            "zakat_due": float(data.get("zakat_due", 0)),
            "status": data.get("status", "UNKNOWN"),
            "paid": False # Defaults to unpaid so the frontend can show a "Pay Now" button later
        }

        # Reference the specific user in Firestore
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({"success": False, "error": "User not found in database"}), 404

        # Grab existing data
        user_data = user_doc.to_dict()
        zakat_history = user_data.get('zakat_history', [])

        # Append the new calculation
        zakat_history.append(new_record)

        # Push the updated array back to the cloud
        user_ref.update({
            "zakat_history": zakat_history
        })

        return jsonify({
            "success": True,
            "message": "Zakat record permanently saved to the cloud ledger!",
            "data": new_record
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500