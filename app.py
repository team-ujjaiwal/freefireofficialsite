from flask import Flask, request
import requests
from urllib.parse import quote

app = Flask(__name__)

def clean_response(data):
    """Recursively removes all externalIconInfo from response data"""
    if isinstance(data, dict):
        # Remove from current level
        data.pop('externalIconInfo', None)
        # Clean all dictionary values
        return {k: clean_response(v) for k, v in data.items()}
    elif isinstance(data, list):
        # Clean all list items
        return [clean_response(item) for item in data]
    return data

@app.route('/api/player/search', methods=['GET'])
def search():
    nickname = request.args.get('nickname', '').strip()
    region = request.args.get('region', '').strip()
    
    if not nickname or not region:
        return {"status": False, "message": "Missing nickname or region"}, 400
    
    try:
        url = f"https://api.bielnetwork.com.br/api/search_nick?nickname={quote(nickname)}&region={quote(region)}"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        # Deep clean the entire response
        cleaned_data = clean_response(data)
        return cleaned_data, response.status_code
        
    except requests.exceptions.RequestException as e:
        return {"status": False, "error": str(e)}, 500

@app.route('/')
def home():
    return {
        "api": "Free Fire Player Search",
        "endpoint": "/search?nickname=NAME&region=REGION",
        "example": "/search?nickname=PRO&region=brazil"
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)