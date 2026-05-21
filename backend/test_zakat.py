import requests

# The URL of your local Flask server
url = 'http://127.0.0.1:5000/api/zakat/save'

# The fake data the frontend WILL send when they click "Save"
test_data = {
    "userId": "test_user_123",
    "type": "Zakat Harta",
    "wealth": 45000,
    "zakat_due": 1125,
    "status": "ELIGIBLE_FOR_ZAKAT"
}

print("🚀 Sending POST request to backend...")
response = requests.post(url, json=test_data)

print("Status Code:", response.status_code)
print("Response:", response.json())
