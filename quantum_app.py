def fetch_data(game_id):
    url = "https://91club.com/api/GetNoaverageEmerdList"
    payload = {"gameId": game_id, "pageNo": 1, "pageSize": 12}
    
    # 🕵️ Stealth Headers to bypass "Server Busy"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://91club.com/",
        "Origin": "https://91club.com",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": "Bearer" # This sometimes triggers a fresh response
    }
    
    try:
        # We use a session to maintain connection stability
        session = requests.Session()
        response = session.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            return response.json().get('data', {}).get('list', [])
        return None
    except Exception as e:
        print(f"Error Log: {e}")
        return None
