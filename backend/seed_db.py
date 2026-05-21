from firebase_config import db
from datetime import datetime

def seed_database():
    print("🌱 Seeding database with test data...")

    # 1. Seed the stocks_cache (Just like your screenshot!)
    stock_ref = db.collection('stocks_cache').document('AAPL')
    stock_ref.set({
        'name': 'Apple Inc.',
        'isHalal': True,
        'lastPrice': 175.4,
        'lastUpdated': datetime.utcnow().isoformat() + "Z"
    })
    print("✅ Added AAPL to stocks_cache!")

    # 2. Seed a test user (So you can test your Zakat & Portfolio routes!)
    user_id = 'test_user_123'
    user_ref = db.collection('users').document(user_id)
    user_ref.set({
        'name': 'Hackathon Judge',
        'totalPortfolioValue': 45000,
        'portfolio': [
            {
                'ticker': 'AAPL',
                'shares': 10,
                'averagePrice': 170.0
            }
        ],
        'zakat_history': [] # Empty array ready for your /save route!
    })
    print(f"✅ Added Test User to users collection (ID: {user_id})!")

    print("🎉 Database seeding complete! Go check your Firebase Console.")

if __name__ == '__main__':
    seed_database()