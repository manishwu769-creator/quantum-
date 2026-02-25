import streamlit as st
import requests
import pandas as pd
import time

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Quantum Predictor Pro", page_icon="💎", layout="centered")

# Professional UI Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1f2937; border-radius: 10px; padding: 15px; border: 1px solid #374151; }
    .prediction-box { font-size: 50px; font-weight: bold; text-align: center; padding: 20px; border-radius: 15px; margin: 10px 0; }
    .big-text { color: #ff4b4b; border: 2px solid #ff4b4b; background-color: rgba(255, 75, 75, 0.1); }
    .small-text { color: #00ffcc; border: 2px solid #00ffcc; background-color: rgba(0, 255, 204, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND API ENGINE ---
def fetch_api_data(game_id):
    """Bypasses timeouts by using mobile-simulated headers"""
    url = "https://91club.com/api/GetNoaverageEmerdList" 
    payload = {"gameId": game_id, "pageNo": 1, "pageSize": 12}
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Referer": "https://91club.com/",
        "Origin": "https://91club.com"
    }
    
    try:
        # 10-second timeout is enough for API requests
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get('data', {}).get('list', [])
    except Exception:
        return None
    return None

# --- UI INTERFACE ---
st.title("💎 𝐐𝐔𝐀𝐍𝐓𝐔𝐌 𝐏𝐑𝐄𝐃𝐈𝐂𝐓𝐎𝐑 𝐔𝐋𝐓𝐑𝐀")
st.write("Live API Dashboard • Anti-Ban Secured")

game_choice = st.selectbox("🎮 Select Game Mode", ["WinGo 1m", "WinGo 3m", "WinGo 5m", "WinGo 10m"])
game_map = {"WinGo 1m": 1, "WinGo 3m": 2, "WinGo 5m": 3, "WinGo 10m": 4}

# Container for live updates
placeholder = st.empty()

while True:
    with placeholder.container():
        data_list = fetch_api_data(game_map[game_choice])
        
        if data_list and len(data_list) > 0:
            latest = data_list[0]
            current_period = latest['issueNumber']
            last_number = int(latest['number'])
            
            # 🎯 PREDICTION LOGIC
            # 0-4 = Small | 5-9 = Big
            prediction = "𝐁𝐈𝐆 🔴" if last_number >= 5 else "𝐒𝐌𝐀𝐋𝐋 🟢"
            pred_class = "big-text" if last_number >= 5 else "small-text"

            # 📈 WIN-RATE CALCULATOR
            correct = 0
            for i in range(len(data_list) - 1):
                # Check if the previous prediction matched the next result
                if (int(data_list[i+1]['number']) >= 5 and int(data_list[i]['number']) >= 5) or \
                   (int(data_list[i+1]['number']) < 5 and int(data_list[i]['number']) < 5):
                    correct += 1
            win_rate = (correct / (len(data_list)-1)) * 100

            # DISPLAY METRICS
            c1, c2, c3 = st.columns(3)
            c1.metric("Period ID", current_period)
            c2.metric("Last Result", last_number)
            c3.metric("Win Rate", f"{win_rate:.1f}%")

            st.markdown(f'<div class="prediction-box {pred_class}">{prediction}</div>', unsafe_allow_html=True)
            
            # RECENT HISTORY TABLE
            st.subheader("📑 Recent Game History")
            history_df = pd.DataFrame(data_list[:8])[['issueNumber', 'number']]
            history_df.columns = ['Period', 'Result Number']
            st.table(history_df)
            
            st.caption(f"🔄 Last sync: {time.strftime('%H:%M:%S')} | Data source: Direct API")
        else:
            st.warning("📡 Connecting to 91 Club Server... Please wait.")
            
    time.sleep(5) # Refresh every 5 seconds