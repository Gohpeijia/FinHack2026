import os
from flask import Flask, jsonify
from flask_cors import CORS

# Import your route blueprints
from portfolio_routes import portfolio_bp
from market_routes import market_bp  
from ai_routes import ai_bp

app = Flask(__name__)
CORS(app) 

# Register the blueprints
app.register_blueprint(portfolio_bp, url_prefix='/api/stocks/portfolio')
app.register_blueprint(market_bp, url_prefix='/api/stocks/market')
app.register_blueprint(ai_bp, url_prefix='/api/stocks/ai')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"message": "Modular Islamic Stocks API is running! 🐍🚀"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=True)