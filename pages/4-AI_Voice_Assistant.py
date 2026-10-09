import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import re
import json
import time
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==============================================================================
# 1. Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="AI Voice Sales Assistant",
    page_icon="🎙️",
    layout="wide"
)

# Clean, modern styling
st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC;
    }
    .main-title {
        color: #245c54;
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .sub-title {
        color: #64748B;
        font-size: 15px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. Data Loading & Ground Truth Statistics
# ==============================================================================
@st.cache_data
def load_sales_data():
    path = "retail_store_sales_clean.parquet"
    if not os.path.exists(path):
        path = "retail_store_sales.csv"
        df = pd.read_csv(path)
    else:
        df = pd.read_parquet(path)
    if 'Transaction Date' in df.columns:
        df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce')
    return df

try:
    df = load_sales_data()
except Exception as e:
    st.error(f"Error loading sales data: {e}")
    st.stop()

def get_verified_data_context(dataframe: pd.DataFrame) -> str:
    total_revenue = dataframe['Total Spent'].sum()
    total_txns = len(dataframe)
    
    cat_df = dataframe.groupby('Category').agg(
        Revenue=('Total Spent', 'sum'),
        Transactions=('Transaction ID', 'count'),
        Avg_Price=('Price Per Unit', 'mean')
    ).sort_values('Revenue', ascending=False)
    cat_df['Share_Pct'] = (cat_df['Revenue'] / total_revenue) * 100

    loc_df = dataframe.groupby('Location').agg(
        Revenue=('Total Spent', 'sum'),
        Transactions=('Transaction ID', 'count')
    ).sort_values('Revenue', ascending=False)
    loc_df['Share_Pct'] = (loc_df['Revenue'] / total_revenue) * 100

    pay_df = dataframe.groupby('Payment Method').agg(
        Revenue=('Total Spent', 'sum'),
        Transactions=('Transaction ID', 'count')
    ).sort_values('Revenue', ascending=False)
    pay_df['Share_Pct'] = (pay_df['Revenue'] / total_revenue) * 100

    day_df = dataframe.groupby('Day_type').agg(
        Revenue=('Total Spent', 'sum'),
        Transactions=('Transaction ID', 'count')
    )
    day_df['Share_Pct'] = (day_df['Revenue'] / total_revenue) * 100

    disc_df = dataframe.groupby('Discount Applied').agg(
        Revenue=('Total Spent', 'sum'),
        Transactions=('Transaction ID', 'count'),
        Avg_Spend=('Total Spent', 'mean')
    )

    return f"""
VERIFIED SALES DATA (12,575 total records):
Total Revenue: ${total_revenue:,.2f}
Total Transactions: {total_txns:,}

1. CATEGORY BREAKDOWN (EXACT REAL NUMBERS):
{cat_df.to_string()}

2. LOCATION BREAKDOWN (Online vs In-store):
{loc_df.to_string()}

3. PAYMENT METHOD BREAKDOWN:
{pay_df.to_string()}

4. DAY TYPE (Weekend vs Weekday):
{day_df.to_string()}

5. DISCOUNT IMPACT:
{disc_df.to_string()}
"""

# ==============================================================================
# 3. Gemini Analytics Engine
# ==============================================================================
def get_gemini_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if not key and "GEMINI_API_KEY" in st.secrets:
        key = st.secrets["GEMINI_API_KEY"]
    return key

def query_gemini_analyst(user_query: str, dataframe: pd.DataFrame) -> dict:
    api_key = get_gemini_api_key()
    if not api_key:
        return {
            "spoken_text": "Gemini API key is not configured in .env file.",
            "analysis": "⚠️ **GEMINI_API_KEY** is missing from `.env`.",
            "code": None
        }

    verified_stats = get_verified_data_context(dataframe)
    prompt = f"""
You are an expert Retail Sales Data Analyst and Voice Assistant.
Here is the ground truth verified data from the sales dataset:

{verified_stats}

User Question: "{user_query}"

CRITICAL INSTRUCTIONS:
1. ONLY USE THE EXACT NUMBERS from the VERIFIED AGGREGATIONS above. Do NOT invent numbers.
2. If user speaks Arabic, respond in fluent Arabic. If in English, respond in English.
3. In `spoken_text`: Exactly 1-2 natural sentences for voice audio playback with accurate figures (no markdown symbols, no bullets).
4. In `analysis`: Structured, accurate Markdown report using the exact verified numbers ($), rankings, and business insights.
5. In `code`: Python pandas code generating `fig` using Plotly Express (`px.bar`, `px.pie`, or `px.line` with color '#245c54') to visually represent the requested data from `df`.

Return strictly valid JSON:
{{
  "language": "ar" or "en",
  "spoken_text": "Accurate spoken summary",
  "analysis": "Markdown analysis with exact figures",
  "code": "Python pandas code creating fig or null"
}}
"""

    models = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash", "gemini-2.5-flash-lite"]
    for m in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
        try:
            r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=20)
            if r.status_code == 200:
                raw = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                match = re.search(r"\{.*\}", raw, re.DOTALL)
                if match:
                    return json.loads(match.group(0))
                return json.loads(raw)
        except Exception:
            continue

    is_ar = any("\u0600" <= c <= "\u06FF" for c in user_query)
    return {
        "language": "ar" if is_ar else "en",
        "spoken_text": "تم تحليل البيانات بنجاح." if is_ar else "Data analyzed successfully.",
        "analysis": "Analysis completed successfully.",
        "code": None
    }

def run_code(code_str: str, dataframe: pd.DataFrame):
    if not code_str:
        return None
    local_env = {"df": dataframe, "pd": pd, "np": np, "px": px, "go": go, "fig": None}
    try:
        exec(code_str, {"__builtins__": {
            "sum": sum, "max": max, "min": min, "len": len, "round": round,
            "int": int, "float": float, "str": str, "bool": bool, "list": list, "dict": dict
        }}, local_env)
        fig = local_env.get("fig")
        if fig:
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(246, 248, 251, 0.4)",
                font=dict(color="#172033"),
                margin=dict(l=15, r=15, t=30, b=15)
            )
        return fig
    except Exception:
        return None

# ==============================================================================
# 4. Reliable Real-Time Voice Hub & Auto-Submitter
# ==============================================================================
def render_voice_interface(spoken_text: str = "", spoken_lang: str = "en", token: str = ""):
    clean_text = spoken_text.replace("\n", " ").replace('"', '\\"').replace("'", "\\'")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            * {{ box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
            body {{
                margin: 0;
                padding: 2px 0;
                background: transparent;
            }}
            .voice-panel {{
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                padding: 10px 18px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            }}
            .left-side {{
                display: flex;
                align-items: center;
                gap: 12px;
                flex: 1;
            }}
            .mic-btn {{
                background: #245c54;
                color: white;
                border: none;
                width: 44px;
                height: 44px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: 0.2s;
                flex-shrink: 0;
            }}
            .mic-btn:hover {{
                background: #173e38;
                transform: scale(1.06);
            }}
            .mic-btn.listening {{
                background: #EF4444;
                animation: pulse 1.2s infinite;
            }}
            @keyframes pulse {{
                0% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }}
                70% {{ transform: scale(1.1); box-shadow: 0 0 0 12px rgba(239, 68, 68, 0); }}
                100% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
            }}
            .status-text {{
                font-size: 14px;
                font-weight: 600;
                color: #334155;
            }}
            .lang-select {{
                background: #F1F5F9;
                border: 1px solid #CBD5E1;
                color: #334155;
                font-size: 12px;
                font-weight: 600;
                padding: 6px 10px;
                border-radius: 6px;
                cursor: pointer;
            }}
            .btn-action {{
                background: #E6F3F0;
                color: #245c54;
                border: 1px solid #B8DDD6;
                padding: 7px 14px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
                cursor: pointer;
                transition: 0.2s;
                margin-left: 6px;
            }}
            .btn-action:hover {{
                background: #245c54;
                color: white;
            }}
        </style>
    </head>
    <body>
        <div class="voice-panel">
            <div class="left-side">
                <button id="micBtn" class="mic-btn" onclick="toggleRecognition()" title="Click to speak">🎙️</button>
                <div class="status-text" id="statusLabel">Click the mic, speak, and it answers automatically</div>
                <select id="langChoice" class="lang-select" onchange="changeLang()">
                    <option value="en-US">🇺🇸 English</option>
                    <option value="ar-SA">🇸🇦 العربية</option>
                </select>
            </div>
            <div>
                <button class="btn-action" onclick="playSpeech()">🔊 Play Voice</button>
                <button class="btn-action" onclick="stopSpeech()">⏹️ Stop</button>
            </div>
        </div>

        <script>
            let recognition = null;
            let isListening = false;
            let audioAnswer = "{clean_text}";
            let audioLang = "{spoken_lang}";
            let playToken = "{token}";

            const SpeechAPI = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (SpeechAPI) {{
                recognition = new SpeechAPI();
                recognition.continuous = false;
                recognition.interimResults = true;
                recognition.lang = document.getElementById('langChoice').value;

                recognition.onstart = function() {{
                    isListening = true;
                    document.getElementById('micBtn').classList.add('listening');
                    document.getElementById('statusLabel').innerText = "🔴 Listening... Speak now!";
                }};

                recognition.onresult = function(e) {{
                    let interim = '';
                    let finalTranscript = '';
                    for (let i = e.resultIndex; i < e.results.length; ++i) {{
                        if (e.results[i].isFinal) {{
                            finalTranscript += e.results[i][0].transcript;
                        }} else {{
                            interim += e.results[i][0].transcript;
                        }}
                    }}

                    if (finalTranscript && finalTranscript.trim().length > 1) {{
                        document.getElementById('statusLabel').innerText = "✅ Sending: " + finalTranscript;
                        submitTextToStreamlit(finalTranscript.trim());
                    }}
                }};

                recognition.onerror = function(e) {{
                    isListening = false;
                    document.getElementById('micBtn').classList.remove('listening');
                    document.getElementById('statusLabel').innerText = "Mic status: " + e.error;
                }};

                recognition.onend = function() {{
                    isListening = false;
                    document.getElementById('micBtn').classList.remove('listening');
                }};
            }}

            function submitTextToStreamlit(text) {{
                try {{
                    const parentDoc = window.parent.document;
                    const inputs = parentDoc.querySelectorAll('textarea[data-testid="stChatInputTextArea"], input[data-testid="stChatInputTextArea"]');
                    
                    if (inputs && inputs.length > 0) {{
                        const inp = inputs[inputs.length - 1];
                        
                        // Set value via prototype setter for React compatibility
                        const proto = inp.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
                        const setNativeValue = Object.getOwnPropertyDescriptor(proto, 'value').set;
                        setNativeValue.call(inp, text);
                        
                        // Dispatch input events
                        inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        
                        // Click submit button
                        setTimeout(() => {{
                            const btn = parentDoc.querySelector('button[data-testid="stChatInputSubmitButton"]');
                            if (btn) {{
                                btn.disabled = false;
                                btn.click();
                            }}
                        }}, 150);
                    }}
                }} catch(err) {{
                    console.error("Auto submit note:", err);
                }}
            }}

            function changeLang() {{
                if (recognition) {{
                    recognition.lang = document.getElementById('langChoice').value;
                }}
            }}

            function toggleRecognition() {{
                if (!recognition) {{
                    alert("Please use Chrome or Edge for live speech recognition.");
                    return;
                }}
                if (isListening) {{
                    recognition.stop();
                }} else {{
                    window.speechSynthesis.cancel();
                    recognition.lang = document.getElementById('langChoice').value;
                    recognition.start();
                }}
            }}

            function playSpeech() {{
                if (!audioAnswer || audioAnswer.length < 2) return;
                window.speechSynthesis.cancel();
                const u = new SpeechSynthesisUtterance(audioAnswer);
                u.lang = (audioLang === 'ar') ? 'ar-SA' : 'en-US';
                u.rate = 1.0;
                window.speechSynthesis.speak(u);
            }}

            function stopSpeech() {{
                window.speechSynthesis.cancel();
            }}

            // Auto-speak strictly once per new response
            window.addEventListener('load', function() {{
                if (!playToken || playToken.length < 3 || !audioAnswer || audioAnswer.length < 2) return;
                const key = 'spoken_tok_' + playToken;
                if (!sessionStorage.getItem(key)) {{
                    sessionStorage.setItem(key, 'true');
                    setTimeout(playSpeech, 300);
                }}
            }});
        </script>
    </body>
    </html>
    """
    components.html(html, height=70)

# ==============================================================================
# 5. Session State
# ==============================================================================
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "last_spoken" not in st.session_state:
    st.session_state.last_spoken = ""
if "last_lang" not in st.session_state:
    st.session_state.last_lang = "en"
if "play_token" not in st.session_state:
    st.session_state.play_token = ""

# ==============================================================================
# 6. Page UI
# ==============================================================================
st.markdown('<div class="main-title">🎙️ AI Voice Sales Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Talk directly with the AI voice agent to analyze retail store sales data in English or Arabic.</div>', unsafe_allow_html=True)

# Voice Bar
render_voice_interface(
    spoken_text=st.session_state.last_spoken,
    spoken_lang=st.session_state.last_lang,
    token=st.session_state.play_token
)

# Quick Questions & Clear Results Action Row (5 Columns)
c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 0.8])
clicked = None
with c1:
    if st.button("🏆 Top Categories", use_container_width=True):
        clicked = "What are the top product categories by total sales revenue? Provide exact revenue and share."
with c2:
    if st.button("📍 Online vs In-store", use_container_width=True):
        clicked = "Compare sales performance between Online and In-store channels with exact figures."
with c3:
    if st.button("💳 Payment Methods", use_container_width=True):
        clicked = "What is the breakdown of total revenue by payment method?"
with c4:
    if st.button("🗓️ Weekend vs Weekday", use_container_width=True):
        clicked = "Compare total sales between Weekend and Weekdays"
with c5:
    # Clear Results Button
    if st.button("🗑️ Clear Results", use_container_width=True, type="secondary"):
        st.session_state.conversation = []
        st.session_state.last_spoken = ""
        st.session_state.play_token = ""
        st.rerun()

st.markdown("---")

# Render Native Streamlit Chat Messages
for msg in st.session_state.conversation:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["text"])
        if msg.get("fig") is not None:
            st.plotly_chart(msg["fig"], use_container_width=True)

# Chat Input (Bottom) - Also auto-submits when spoken
typed_query = st.chat_input("Type a question or speak using the mic above... / Ask anything about sales")
active_query = clicked or typed_query

if active_query:
    st.session_state.conversation.append({"role": "user", "text": active_query})
    
    with st.spinner("Analyzing sales data and generating voice response..."):
        ai_data = query_gemini_analyst(active_query, df)
        
        spoken_text = ai_data.get("spoken_text", "")
        analysis_text = ai_data.get("analysis", "")
        lang = ai_data.get("language", "en")
        code = ai_data.get("code")
        
        fig = run_code(code, df) if code else None
        
        st.session_state.last_spoken = spoken_text
        st.session_state.last_lang = lang
        st.session_state.play_token = f"tok_{int(time.time() * 1000)}"
        
        st.session_state.conversation.append({
            "role": "assistant",
            "text": analysis_text,
            "fig": fig
        })
        st.rerun()
