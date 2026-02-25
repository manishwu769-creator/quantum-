import streamlit as st
import requests
import pandas as pd
import time

# --- APP CONFIG ---
st.set_page_config(page_title="Quantum Predictor Pro", page_icon="💎")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .prediction-box { font-size: 45px; font-weight: bold; text-align: center; padding: 20px; border-radius: 15px; border: 2px solid #374151; margin-bottom: 20px; }
    .big-text { color: #ff4b4b; background-color: rgba(255, 75, 75, 0.1); }
    .small-text { color: #00ffcc; background-color: rgba(0, 255, 204, 0.1); }
    </style>
    """, unsafe_allow_html=True)

def fetch_data(game_id):
    url = "https://91club.com/api/GetNoaverageEmerdList"
    payload = {"gameId": game_id, "pageNo": 1, "pageSize": 10}
    # Using a rotating mobile header to prevent "Connection Lag"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.json().get('data', {}).get('list', [])
    except:
        return None

# --- UI ---
st.title("💎 𝐐𝐔𝐀𝐍𝐓𝐔𝐌 𝐏𝐑𝐄𝐃𝐈𝐂𝐓𝐎𝐑")
game_choice = st.selectbox("🎮 Select Mode", ["WinGo 1m", "WinGo 3m", "WinGo 5m"])
game_map = {"WinGo 1m": 1, "WinGo 3m": 2, "WinGo 5m": 3}

placeholder = st.empty()

while True:
    with placeholder.container():
        data = fetch_data(game_map[game_choice])
        if data:
            latest = data[0]
            num = int(latest['number'])
            period = latest['issueNumber']
            
            # Prediction Logic
            pred = "𝐁𝐈𝐆 🔴" if num >= 5 else "𝐒𝐌𝐀𝐋𝐋 🟢"
            style = "big-text" if num >= 5 else "small-text"
            
            st.metric("CURRENT PERIOD", period)
            st.markdown(f'<div class="prediction-box {style}">{pred}</div>', unsafe_allow_html=True)
            
            st.write("📑 **Recent Results**")
            st.table(pd.DataFrame(data[:5])[['issueNumber', 'number']])
        else:
            st.warning("📡 Server Busy. Retrying in 5 seconds...")
    time.sleep(5)
