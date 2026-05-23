from firebase_config import db
from flask import Blueprint, jsonify, request, g
from security import require_auth 

portfolio_bp = Blueprint('portfolio', __name__)

FITRAH_RATES = {
    "Johor": 7.00,
    "Kedah": 7.00,
    "Kelantan": 6.00,
    "Melaka": 7.00,
    "Negeri Sembilan": 7.00,
    "Pahang": 7.00,
    "Perak": 7.00,
    "Perlis": 6.50,
    "Pulau Pinang": 7.00,
    "Sabah": 7.00,
    "Sarawak": 7.00,
    "Selangor": 7.00,
    "Terengganu": 6.00,
    "W.P. Kuala Lumpur": 8.00,
    "W.P. Labuan": 7.00,
    "W.P. Putrajaya": 8.00
}

@portfolio_bp.route('/my-portfolio', methods=['GET'])
@require_auth 
def get_portfolio():
    try:
        # Grab the secure ID from the 'g' object
        secure_user_id = g.uid 
        
        doc_ref = db.collection('users').document(secure_user_id)
        doc = doc_ref.get()
        
        if doc.exists:
            return jsonify({"success": True, "data": doc.to_dict()})
        else:
            return jsonify({"success": False, "error": "User not found"}), 404
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@portfolio_bp.route('/buy', methods=['POST'])
@require_auth
def buy_stock():
    try:
        data = request.json
        secure_user_id = g.uid 
        
        # 1. Extract the new attributes from the frontend request
        sticker = data.get('sticker', '').upper()
        name = data.get('name', '').strip()
        
        try:
            shares = int(data.get('shares', 0))
        except ValueError:
            return jsonify({"success": False, "error": "Shares must be a valid number"}), 400

        # Extract extra metadata fields provided by the frontend
        fields = data.get('fields', {})       # Can be an object/dict or string
        chart = data.get('chart', {})         # Can be an object/dict or string
        watchlist = bool(data.get('watchlist', False))

        # Strict Validation Hardening
        if not sticker or shares <= 0:
            return jsonify({"success": False, "error": "Invalid trade values. Sticker is required and shares must be greater than zero."}), 400

        user_ref = db.collection('users').document(secure_user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({"success": False, "error": "User not found"}), 404

        user_data = user_doc.to_dict()
        portfolio = user_data.get('portfolio', [])
        
        # 2. Look for the asset inside the array using the new 'sticker' key
        stock_found = False
        for item in portfolio:
            if item.get('sticker') == sticker:
                item['shares'] += shares
                item['name'] = name
                item['fields'] = fields
                item['chart'] = chart
                item['watchlist'] = watchlist
                stock_found = True
                break

        # If it's a new stock, append the entire new schema layout
        if not stock_found:
            portfolio.append({
                "sticker": sticker,
                "name": name,
                "shares": shares,
                "fields": fields,
                "chart": chart,
                "watchlist": watchlist
            })

        # 3. Update payload (Accepting total portfolio value calculation directly from the frontend)
        update_payload = {
            "portfolio": portfolio
        }
        
        if 'totalPortfolioValue' in data:
            update_payload["totalPortfolioValue"] = float(data.get('totalPortfolioValue', 0.0))

        user_ref.update(update_payload)

        return jsonify({
            "success": True, 
            "message": f"Successfully updated portfolio entry for {sticker}!"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
# --- WATCHLIST MANAGEMENT ---
@portfolio_bp.route('/watchlist', methods=['POST'])
@require_auth
def manage_watchlist():
    try:
        data = request.json
        secure_user_id = g.uid

        # Extract the attributes
        sticker = data.get('sticker', '').upper()
        
        try:
            price = float(data.get('price', 0.0))
        except ValueError:
            return jsonify({"success": False, "error": "Price must be a valid number"}), 400

        if not sticker:
            return jsonify({"success": False, "error": "Sticker is required."}), 400

        user_ref = db.collection('users').document(secure_user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({"success": False, "error": "User not found"}), 404

        # Retrieve the existing watchlist array, or start a new one
        user_data = user_doc.to_dict()
        watchlist = user_data.get('watchlist', [])

        # Check if the sticker is already in the watchlist
        stock_found = False
        for item in watchlist:
            if item.get('sticker') == sticker:
                # If it exists, just update the latest saved price
                item['price'] = price
                stock_found = True
                break

        # If it's a new stock, add it to the array
        if not stock_found:
            watchlist.append({
                "sticker": sticker,
                "price": price
            })

        # Save back to Firestore
        user_ref.update({
            "watchlist": watchlist
        })

        return jsonify({
            "success": True, 
            "message": f"Successfully updated {sticker} in your watchlist!",
            "data": watchlist
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@portfolio_bp.route('/update', methods=['POST'])
@require_auth
def update_profile():
    try:
        data = request.json
        user_id = g.uid

        email = data.get('email', '').strip()
        preference_data = data.get('preference', {})

        update_payload = {"profile_complete": False}

        if email:
            update_payload["email"] = email

        # Safely map the preference object
        if preference_data:
            update_payload["preference"] = {
                "employmentStatus": preference_data.get('employmentStatus', ''),
                "monthlyIncome": float(preference_data.get('monthlyIncome', 0.0)),
                "investmentExperience": preference_data.get('investmentExperience', ''),
                "riskTolerance": preference_data.get('riskTolerance', ''),
                "zakatGoal": preference_data.get('zakatGoal', '')
            }
            update_payload["profile_complete"] = True

        # Use update() to merge without deleting their portfolio or history
        db.collection('users').document(user_id).set(update_payload, merge=True)

        return jsonify({
            "success": True,
            "message": "Preferences safely updated.",
            "data": update_payload
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@portfolio_bp.route('/me', methods=['GET'])
@require_auth
def get_profile():
    try:
        user_id = g.uid
        doc = db.collection('users').document(user_id).get()

        if not doc.exists:
            return jsonify({"success": False, "error": "User not found"}), 404

        data = doc.to_dict()

        return jsonify({
            "success": True,
            "data": {
                "email": data.get("email", ""),
                "preference": data.get("preference", {}),
                "profile_complete": data.get("profile_complete", False)
            }
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
        
@portfolio_bp.route('/watchlist/remove', methods=['POST'])
@require_auth
def remove_from_watchlist():
    try:
        data = request.json
        secure_user_id = g.uid
        sticker_to_remove = data.get('sticker', '').upper()

        if not sticker_to_remove:
             return jsonify({"success": False, "error": "Sticker is required."}), 400

        user_ref = db.collection('users').document(secure_user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({"success": False, "error": "User not found"}), 404

        user_data = user_doc.to_dict()
        watchlist = user_data.get('watchlist', [])

        # Filter out the sticker the user wants to remove
        updated_watchlist = [item for item in watchlist if item.get('sticker') != sticker_to_remove]

        user_ref.update({
            "watchlist": updated_watchlist
        })

        return jsonify({
            "success": True, 
            "message": f"Removed {sticker_to_remove} from watchlist."
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@portfolio_bp.route('/goal', methods=['POST'])
@require_auth
def manage_goal():
    try:
        data = request.json
        secure_user_id = g.uid

        # Extract the Tabung attributes from frontend
        goal_title = data.get('goaltitle', '').strip()
        target_date = data.get('date', '').strip()
        
        try:
            total_amount = float(data.get('totalamount', 0.0))
            total_gathered = float(data.get('totalgatheredamount', 0.0))
        except ValueError:
            return jsonify({"success": False, "error": "Amounts must be valid numbers"}), 400

        if not goal_title or total_amount <= 0:
            return jsonify({"success": False, "error": "Goal title and a target amount greater than zero are required."}), 400

        # Save to the user's Firestore document
        goal_payload = {
            "goaltitle": goal_title,
            "date": target_date,
            "totalamount": total_amount,
            "totalgatheredamount": total_gathered
        }

        # Merge it into the existing user document
        db.collection('users').document(secure_user_id).set({
            "tabung_goal": goal_payload
        }, merge=True)

        return jsonify({
            "success": True, 
            "message": f"Successfully updated your goal: {goal_title}!",
            "data": goal_payload
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500