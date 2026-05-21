import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter               
from flask_limiter.util import get_remote_address

# Import your route blueprints
from portfolio_routes import portfolio_bp
from market_routes import market_bp  
from zakat_endpoints import zakat_bp


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

app = Flask(__name__)
CORS(app) 

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "10 per minute"],
    storage_uri="memory://"
)

# Register the blueprints
app.register_blueprint(portfolio_bp, url_prefix='/api/stocks/portfolio')
app.register_blueprint(market_bp, url_prefix='/api/stocks/market')
app.register_blueprint(zakat_bp, url_prefix='/api/zakat')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"message": "Modular Islamic Stocks API is running! 🐍🚀"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=True)