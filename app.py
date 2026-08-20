"""
🧡 Dost AI — COMPLETE FREE AI MODELS
All Free AI Tools: Chat, Image, Video, Music, Translate
Includes: FLUX, SDXL, CogVideo, MusicGen, DeepSeek, and 40+ more free models
"""

import streamlit as st
import requests
import os
import uuid
import sqlite3
import time
import base64
import threading
import math
import io
import random
from datetime import date
from urllib.parse import quote
import streamlit.components.v1 as components
from huggingface_hub import InferenceClient

# ============================================================
# 🔐 SECURE SECRETS
# ============================================================
def get_secret(name):
    """Get secret from Streamlit secrets or environment variables"""
    try:
        val = st.secrets.get(name)
        if val and str(val).strip():
            return str(val).strip()
    except Exception:
        pass
    
    val = os.environ.get(name)
    if val and str(val).strip():
        return str(val).strip()
    
    return None

# ============================================================
# 🔐 API KEYS
# ============================================================
GROQ_API_KEY = get_secret("GROQ_API_KEY")
CEREBRAS_API_KEY = get_secret("CEREBRAS_API_KEY")
MISTRAL_API_KEY = get_secret("MISTRAL_API_KEY")
AGNES_API_KEY = get_secret("AGNES_API_KEY")
MUSICAPI_KEY = get_secret("MUSICAPI_KEY")
HF_API_KEY = get_secret("HF_API_KEY")
REPLICATE_API_KEY = get_secret("REPLICATE_API_KEY")
DEEPSEEK_API_KEY = get_secret("DEEPSEEK_API_KEY")

# ============================================================
# CONFIG
# ============================================================
APP_NAME = "Dost AI"
USER_NAME = "Niraj"
TEMPERATURE = 0.4
FREE_MSG_LIMIT_PER_DAY = 40
TOKEN_LIMIT_PER_DAY = 1000
IMAGE_TOKEN_COST = 20
VIDEO_TOKEN_COST = 100
MUSIC_TOKEN_COST = 30

# Dost AI brand mark
_DOST_LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
<defs>
    <linearGradient id="dostLogoBgAvatar" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#4285f4"/>
        <stop offset="50%" stop-color="#9b72cb"/>
        <stop offset="100%" stop-color="#d96570"/>
    </linearGradient>
</defs>
<circle cx="32" cy="32" r="30" fill="url(#dostLogoBgAvatar)"/>
<circle cx="24" cy="35" r="14" fill="white" opacity="0.95"/>
<circle cx="40" cy="35" r="14" fill="white" opacity="0.55"/>
<path d="M46 10 L48 15 L53 16 L48 17 L46 22 L44 17 L39 16 L44 15 Z" fill="#ffd166"/>
</svg>"""
DOST_LOGO_AVATAR = "data:image/svg+xml;base64," + base64.b64encode(_DOST_LOGO_SVG.encode("utf-8")).decode("ascii")

# ============================================================
# 🎨 COMPLETE MODEL CONFIGURATIONS
# ============================================================

# --- ALL IMAGE MODELS (15+ Free) ---
IMAGE_MODELS = {
    "pollinations": {
        "label": "Pollinations AI",
        "icon": "🖼️",
        "desc": "Bilkul free, no key",
        "provider": "pollinations",
        "type": "url",
    },
    "agnes": {
        "label": "Agnes Image",
        "icon": "🤖",
        "desc": "Free, high quality",
        "provider": "agnes",
        "type": "url",
    },
    "huggingface_flux_schnell": {
        "label": "FLUX.1-schnell",
        "icon": "⚡",
        "desc": "Fastest 4-step",
        "provider": "huggingface",
        "model": "black-forest-labs/FLUX.1-schnell",
        "type": "bytes",
    },
    "huggingface_flux_dev": {
        "label": "FLUX.1-dev",
        "icon": "🎨",
        "desc": "Higher quality",
        "provider": "huggingface",
        "model": "black-forest-labs/FLUX.1-dev",
        "type": "bytes",
    },
    "huggingface_sdxl": {
        "label": "SDXL",
        "icon": "🌈",
        "desc": "Stable Diffusion XL",
        "provider": "huggingface",
        "model": "stabilityai/stable-diffusion-xl-base-1.0",
        "type": "bytes",
    },
    "huggingface_sd35": {
        "label": "SD 3.5",
        "icon": "✨",
        "desc": "Latest SD",
        "provider": "huggingface",
        "model": "stabilityai/stable-diffusion-3.5-large",
        "type": "bytes",
    },
    "huggingface_playground": {
        "label": "Playground v2.5",
        "icon": "📸",
        "desc": "Photorealistic",
        "provider": "huggingface",
        "model": "playgroundai/playground-v2.5-1024px-aesthetic",
        "type": "bytes",
    },
    "huggingface_kandinsky": {
        "label": "Kandinsky 2.2",
        "icon": "🎭",
        "desc": "Russian model",
        "provider": "huggingface",
        "model": "kandinsky-community/kandinsky-2-2-decoder",
        "type": "bytes",
    },
    "huggingface_wuerstchen": {
        "label": "Wuerstchen",
        "icon": "🐇",
        "desc": "Super fast 2-step",
        "provider": "huggingface",
        "model": "warp-ai/wuerstchen",
        "type": "bytes",
    },
    "huggingface_openjourney": {
        "label": "OpenJourney",
        "icon": "🎨",
        "desc": "Midjourney-style",
        "provider": "huggingface",
        "model": "prompthero/openjourney-v4",
        "type": "bytes",
    },
    "huggingface_dreamshaper": {
        "label": "DreamShaper",
        "icon": "🌟",
        "desc": "Fantasy/portrait",
        "provider": "huggingface",
        "model": "Lykon/dreamshaper-8",
        "type": "bytes",
    },
    "huggingface_realistic": {
        "label": "Realistic Vision",
        "icon": "👤",
        "desc": "Photorealistic",
        "provider": "huggingface",
        "model": "SG161222/Realistic_Vision_V4.0",
        "type": "bytes",
    },
}

# --- ALL VIDEO MODELS (8+ Free) ---
VIDEO_MODELS = {
    "agnes": {
        "label": "Agnes Video",
        "icon": "🎬",
        "desc": "Free, high quality",
        "provider": "agnes",
        "type": "url",
    },
    "huggingface_cogvideo": {
        "label": "CogVideoX",
        "icon": "🎥",
        "desc": "5B model",
        "provider": "huggingface_video",
        "model": "THUDM/CogVideoX-5b",
        "type": "bytes",
    },
    "huggingface_modelscope": {
        "label": "ModelScope",
        "icon": "🏔️",
        "desc": "Alibaba's model",
        "provider": "huggingface_video",
        "model": "damo/ModelScope",
        "type": "bytes",
    },
    "huggingface_i2vgen": {
        "label": "I2VGen-XL",
        "icon": "🔄",
        "desc": "Image-to-video",
        "provider": "huggingface_video",
        "model": "ali-vilab/i2vgen-xl",
        "type": "bytes",
    },
    "huggingface_svd": {
        "label": "Stable Video Diffusion",
        "icon": "📹",
        "desc": "SVD",
        "provider": "huggingface_video",
        "model": "stabilityai/stable-video-diffusion-img2vid",
        "type": "bytes",
    },
    "huggingface_pyramid": {
        "label": "Pyramid Flow",
        "icon": "🔺",
        "desc": "New, great quality",
        "provider": "huggingface_video",
        "model": "PYRAMID-FLOW/pyramid-flow",
        "type": "bytes",
    },
    "huggingface_mochi": {
        "label": "Mochi-1",
        "icon": "🌀",
        "desc": "10B model",
        "provider": "huggingface_video",
        "model": "genmo/mochi-1",
        "type": "bytes",
    },
}

# --- ALL MUSIC MODELS (3+ Free) ---
MUSIC_MODELS = {
    "huggingface_musicgen": {
        "label": "MusicGen",
        "icon": "🎵",
        "desc": "Meta's AI",
        "provider": "huggingface_music",
        "model": "facebook/musicgen-large",
        "type": "bytes",
    },
    "huggingface_audiocraft": {
        "label": "AudioCraft",
        "icon": "🎶",
        "desc": "Meta's suite",
        "provider": "huggingface_music",
        "model": "facebook/audiocraft",
        "type": "bytes",
    },
    "musicapi": {
        "label": "MusicAPI Sonic",
        "icon": "🎼",
        "desc": "75 free credits",
        "provider": "musicapi",
        "type": "url",
    },
}

# --- ALL CHAT MODELS (12+ Free) ---
CHAT_MODELS = {
    "groq_llama32_1b": {
        "label": "Llama 3.2 1B",
        "icon": "⚡",
        "desc": "Sabse fast",
        "provider": "groq",
        "model_id": "meta-llama/llama-3.2-1b-preview",
    },
    "groq_llama32_3b": {
        "label": "Llama 3.2 3B",
        "icon": "🔥",
        "desc": "Fast & capable",
        "provider": "groq",
        "model_id": "meta-llama/llama-3.2-3b-preview",
    },
    "groq_llama31_70b": {
        "label": "Llama 3.1 70B",
        "icon": "💪",
        "desc": "Powerful",
        "provider": "groq",
        "model_id": "meta-llama/llama-3.1-70b-versatile",
    },
    "groq_llama31_405b": {
        "label": "Llama 3.1 405B",
        "icon": "🧠",
        "desc": "Biggest open model",
        "provider": "groq",
        "model_id": "meta-llama/llama-3.1-405b-reasoning",
    },
    "groq_mixtral": {
        "label": "Mixtral 8x7B",
        "icon": "🌪️",
        "desc": "MoE expert",
        "provider": "groq",
        "model_id": "mistralai/mixtral-8x7b-32768",
    },
    "groq_gemma2_9b": {
        "label": "Gemma 2 9B",
        "icon": "✨",
        "desc": "Google's model",
        "provider": "groq",
        "model_id": "google/gemma-2-9b-it",
    },
    "groq_gemma2_27b": {
        "label": "Gemma 2 27B",
        "icon": "🌟",
        "desc": "Google's big model",
        "provider": "groq",
        "model_id": "google/gemma-2-27b-it",
    },
    "groq_phi3": {
        "label": "Phi-3",
        "icon": "📚",
        "desc": "Microsoft",
        "provider": "groq",
        "model_id": "microsoft/phi-3-mini-128k-instruct",
    },
    "groq_qwen25": {
        "label": "Qwen 2.5",
        "icon": "🐉",
        "desc": "Alibaba",
        "provider": "groq",
        "model_id": "qwen/qwen-2.5-32b-instruct",
    },
    "cerebras": {
        "label": "Cerebras AI",
        "icon": "🧠",
        "desc": "1M tokens/min",
        "provider": "cerebras",
        "model_id": "llama3.1-70b",
    },
    "pollinations": {
        "label": "Pollinations Chat",
        "icon": "🌐",
        "desc": "Bilkul free, no key",
        "provider": "pollinations",
    },
}

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# USAGE DB
# ============================================================
USAGE_DB_PATH = get_secret("USAGE_DB_PATH") or "usage_tracking.db"

def _usage_db():
    conn = sqlite3.connect(USAGE_DB_PATH, check_same_thread=False)
    conn.execute("CREATE TABLE IF NOT EXISTS usage (ip TEXT NOT NULL, day TEXT NOT NULL, msg_count INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (ip, day))")
    conn.execute("CREATE TABLE IF NOT EXISTS tokens (email TEXT NOT NULL, day TEXT NOT NULL, used_tokens INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (email, day))")
    return conn

def get_client_ip():
    try:
        headers = st.context.headers
        forwarded = headers.get("X-Forwarded-For", "")
        if forwarded:
            return forwarded.split(",")[0].strip()
        real_ip = headers.get("X-Real-Ip", "")
        if real_ip:
            return real_ip.strip()
    except Exception:
        pass
    return "unknown"

def get_today_count(ip):
    today = date.today().isoformat()
    conn = _usage_db()
    try:
        row = conn.execute("SELECT msg_count FROM usage WHERE ip = ? AND day = ?", (ip, today)).fetchone()
        return row[0] if row else 0
    finally:
        conn.close()

def increment_today_count(ip):
    today = date.today().isoformat()
    conn = _usage_db()
    try:
        conn.execute("INSERT INTO usage (ip, day, msg_count) VALUES (?, ?, 1) ON CONFLICT(ip, day) DO UPDATE SET msg_count = msg_count + 1", (ip, today))
        conn.commit()
    finally:
        conn.close()

# ============================================================
# 🪙 TOKEN WALLET
# ============================================================
def get_tokens_used_today(email):
    if not email:
        return TOKEN_LIMIT_PER_DAY
    today = date.today().isoformat()
    conn = _usage_db()
    try:
        row = conn.execute("SELECT used_tokens FROM tokens WHERE email = ? AND day = ?", (email, today)).fetchone()
        return row[0] if row else 0
    finally:
        conn.close()

def get_tokens_remaining(email):
    return max(0, TOKEN_LIMIT_PER_DAY - get_tokens_used_today(email))

def deduct_tokens(email, amount):
    if not email:
        return False
    today = date.today().isoformat()
    conn = _usage_db()
    try:
        row = conn.execute("SELECT used_tokens FROM tokens WHERE email = ? AND day = ?", (email, today)).fetchone()
        used = row[0] if row else 0
        if used + amount > TOKEN_LIMIT_PER_DAY:
            return False
        conn.execute(
            "INSERT INTO tokens (email, day, used_tokens) VALUES (?, ?, ?) "
            "ON CONFLICT(email, day) DO UPDATE SET used_tokens = used_tokens + ?",
            (email, today, amount, amount),
        )
        conn.commit()
        return True
    finally:
        conn.close()

# ============================================================
# 🔐 LOGIN GATE
# ============================================================
try:
    _is_logged_in = bool(st.user.is_logged_in)
except Exception:
    _is_logged_in = False

if not _is_logged_in:
    st.markdown(f"""
    <div style='max-width:420px; margin:90px auto 0 auto; text-align:center;'>
        <div style='font-size:44px; margin-bottom:6px;'>🧡</div>
        <div style='font-size:24px; font-weight:600; color:#1f1f1f; margin-bottom:8px;'>{APP_NAME}</div>
        <div style='font-size:14px; color:#5f6368; margin-bottom:26px;'>
            Chat, Image, Video, Music — sab use karne ke liye pehle apne Google account se sign in karo.<br>
            Sign in ke baad har account ko roz <b>{TOKEN_LIMIT_PER_DAY} free tokens</b> milte hain
            (🖼️ Image = {IMAGE_TOKEN_COST} tokens, 🎬 Video = {VIDEO_TOKEN_COST} tokens).
        </div>
    </div>
    """, unsafe_allow_html=True)

    _sp1, _mid, _sp2 = st.columns([1, 1.3, 1])
    with _mid:
        if st.button("🔐  Continue with Google", key="google_login_btn", use_container_width=True, type="primary"):
            try:
                st.login("google")
            except Exception as e:
                st.error(f"⚠️ Google login error: {e}")
    st.stop()

USER_EMAIL = st.user.email
USER_DISPLAY_NAME = st.user.name or (USER_EMAIL.split("@")[0] if USER_EMAIL else "Dost")
USER_PICTURE = getattr(st.user, "picture", None)

# ============================================================
# SESSION STATE
# ============================================================
if "chats" not in st.session_state:
    st.session_state.chats = {}
    st.session_state.chat_order = []

if "current_chat_id" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.chats[new_id] = {"title": None, "messages": []}
    st.session_state.current_chat_id = new_id

if "selected_chat_model" not in st.session_state:
    st.session_state.selected_chat_model = "groq_llama31_70b"

if "gallery" not in st.session_state:
    st.session_state.gallery = []

if "selected_image_model" not in st.session_state:
    st.session_state.selected_image_model = "pollinations"

if "selected_video_model" not in st.session_state:
    st.session_state.selected_video_model = "agnes"

if "selected_music_model" not in st.session_state:
    st.session_state.selected_music_model = "huggingface_musicgen"

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "chat"

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
* { font-family: 'Google Sans', 'Segoe UI', sans-serif !important; }

.block-container { padding-top: 0.5rem !important; padding-bottom: 0.5rem !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; max-width: 100% !important; }
div[data-testid="stElementContainer"], div[data-testid="stVerticalBlock"], div[data-testid="stHorizontalBlock"], div[data-testid="column"] { padding: 0 !important; margin: 0 !important; gap: 0 !important; }

.stApp { background: #ffffff; min-height: 100vh; }
.stApp > header, .stApp > footer { display: none !important; }

section[data-testid="stSidebar"] { background: #ffffff !important; border-right: none !important; padding-top: 16px !important; padding-left: 10px !important; padding-right: 10px !important; }
section[data-testid="stSidebar"] * { color: #1f1f1f !important; }
section[data-testid="stSidebar"] hr { display: none !important; }
section[data-testid="stSidebar"] div.stButton > button { background: transparent !important; border: none !important; border-radius: 24px !important; color: #444746 !important; text-align: left !important; padding: 12px 16px !important; margin-bottom: 4px !important; font-weight: 400 !important; font-size: 14px !important; box-shadow: none !important; }
section[data-testid="stSidebar"] div.stButton > button:hover { background: #f0f4f9 !important; }
section[data-testid="stSidebar"] div.stButton > button[kind="primary"] { background: #d3e3fd !important; border: none !important; color: #041e49 !important; font-weight: 500 !important; }

.main-glass { background: #ffffff; max-width: 900px; padding: 6px 18px 10px 18px; margin: 0 auto; border: none; }

.gemini-header { display: flex !important; align-items: center !important; justify-content: space-between !important; padding: 50px 0 10px 0 !important; border-bottom: none !important; background: transparent !important; position: relative !important; z-index: 100 !important; margin-bottom: 4px !important; }
.gemini-brand { display: flex !important; align-items: center !important; gap: 12px !important; background: transparent !important; }
.gemini-brand svg { width: 34px !important; height: 34px !important; }
.gemini-title { font-size: 22px !important; font-weight: 600 !important; background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; }

.hero-text { text-align: center; padding: 32px 0 24px 0; }
.hero-text h1 { font-size: 30px; font-weight: 600; background: linear-gradient(135deg, #4285f4, #9b72cb, #d96570); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0 4px 0; }
.hero-text p { font-size: 15px; color: #5f6368; margin: 0 0 28px 0; }

.stChatMessage { background: #f0f4f9 !important; border: none !important; border-radius: 18px !important; padding: 12px 18px !important; margin-bottom: 10px !important; box-shadow: none !important; }
.stChatMessage p, .stChatMessage span { color: #1f1f1f !important; }

div.st-key-chat_msg_box { height: auto !important; max-height: 58vh !important; overflow-y: auto !important; padding-right: 6px !important; }

div[data-testid="stSelectbox"] > div > div { background: #f0f4f9 !important; border: 1px solid #e8eaed !important; border-radius: 14px !important; min-height: 44px !important; }

div.stButton > button { border-radius: 20px !important; font-weight: 500 !important; font-size: 14px !important; padding: 10px 24px !important; border: none !important; background: #4285f4 !important; color: white !important; box-shadow: none !important; }
div.stButton > button:hover { background: #3367d6 !important; }

div.st-key-img_studio_card, div.st-key-vid_studio_card {
    background: #fafafa;
    border: 1px solid #e0e0e0 !important;
    border-radius: 22px !important;
    padding: 20px 22px 22px 22px !important;
    max-width: 800px !important;
    margin: 4px auto 26px auto !important;
}

.model-section-label { display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: 0.6px; text-transform: uppercase; padding: 13px 12px 16px 2px; border-radius: 8px; margin: 8px 0 8px 2px; }
.model-section-label.free { background: #e8f0fe; color: #1a56db; }
.model-section-label.pro { background: #fdeee9; color: #b3541e; }

@media (max-width: 768px) {
    .main-glass { padding: 8px 10px; margin: 0 auto; }
    .hero-text { padding: 20px 0 14px 0; }
    .hero-text h1 { font-size: 22px; }
    .gemini-title { font-size: 17px !important; }
}
</style>

<div class="main-glass">
""", unsafe_allow_html=True)

# ============================================================
# FUNCTIONS
# ============================================================
def start_new_chat():
    current = st.session_state.chats[st.session_state.current_chat_id]
    if current["messages"]:
        new_id = str(uuid.uuid4())
        st.session_state.chats[new_id] = {"title": None, "messages": []}
        st.session_state.current_chat_id = new_id
        st.rerun()

def switch_chat(chat_id):
    st.session_state.current_chat_id = chat_id
    st.session_state.active_tab = "chat"
    st.rerun()

# ============================================================
# 🎯 API CALLS - ALL MODELS
# ============================================================

# --- CHAT APIs ---
SYSTEM_PROMPT = f"You are {APP_NAME}, an extremely knowledgeable, precise, and helpful assistant. Reply in the same language the user writes in."

def call_groq_chat(api_key, model, messages, temp=0.4):
    if not api_key:
        return "⚠️ GROQ_API_KEY set nahi hai."
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    full = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    resp = requests.post(url, headers=headers, json={"model": model, "messages": full, "temperature": temp, "max_tokens": 4096}, timeout=90)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def call_cerebras_chat(api_key, model, messages, temp=0.4):
    if not api_key:
        return "⚠️ CEREBRAS_API_KEY set nahi hai."
    url = "https://api.cerebras.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    full = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    resp = requests.post(url, headers=headers, json={"model": model, "messages": full, "temperature": temp, "max_tokens": 4096}, timeout=90)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def call_pollinations_chat(messages, temp=0.4):
    url = "https://text.pollinations.ai/openai"
    full = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    resp = requests.post(url, json={"model": "openai", "messages": full, "temperature": temp}, timeout=90)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def call_huggingface_chat(api_key, model, messages, temp=0.4):
    """Hugging Face chat via Inference API"""
    if not api_key:
        return "⚠️ HF_API_KEY set nahi hai."
    try:
        client = InferenceClient(api_key=api_key)
        # Convert messages format
        chat_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
        response = client.chat_completion(
            model=model,
            messages=chat_messages,
            temperature=temp,
            max_tokens=4096,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# --- IMAGE APIs ---
def run_with_progress(work_fn, estimate_seconds=15, label="Generating"):
    result_holder = {}
    def _runner():
        try:
            result_holder["value"] = work_fn()
        except Exception as e:
            result_holder["error"] = e
    thread = threading.Thread(target=_runner, daemon=True)
    thread.start()
    bar = st.progress(0, text=f"✦ {label}… 0%")
    start = time.time()
    while thread.is_alive():
        elapsed = time.time() - start
        pct = int(92 * (1 - math.exp(-elapsed / estimate_seconds)))
        pct = max(0, min(pct, 92))
        bar.progress(pct, text=f"✦ {label}… {pct}%")
        time.sleep(0.15)
    thread.join()
    bar.progress(100, text=f"✦ {label}… 100%")
    time.sleep(0.25)
    bar.empty()
    if "error" in result_holder:
        raise result_holder["error"]
    return result_holder.get("value")

def get_image_url_pollinations(prompt, ratio="9:16"):
    width, height = (768, 1365) if ratio == "9:16" else (1365, 768)
    return f"https://image.pollinations.ai/prompt/{quote(prompt)}?width={width}&height={height}&model=flux&enhance=true&nologo=true"

def call_agnes_image(prompt, ratio="9:16", api_key=None):
    if api_key is None:
        api_key = AGNES_API_KEY
    if not api_key:
        return None, "⚠️ AGNES_API_KEY set nahi hai."
    url = "https://apihub.agnes-ai.com/v1/images/generations"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    size = "768x1365" if ratio == "9:16" else "1365x768"
    payload = {"model": "agnes-image-2.1-flash", "prompt": prompt, "n": 1, "size": size}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", [{}])[0].get("url"), None
    except Exception as e:
        return None, f"Error: {e}"

def call_huggingface_image(prompt, model_id, ratio="9:16", api_key=None):
    """Hugging Face image generation"""
    if api_key is None:
        api_key = HF_API_KEY
    if not api_key:
        return None, "⚠️ HF_API_KEY set nahi hai."
    
    width, height = (768, 1360) if ratio == "9:16" else (1360, 768)
    try:
        client = InferenceClient(provider="fal-ai", api_key=api_key)
        image = client.text_to_image(prompt, model=model_id, width=width, height=height)
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        return buf.getvalue(), None
    except Exception as e:
        return None, f"Error: {e}"

# --- VIDEO APIs ---
def call_agnes_video(prompt, ratio="9:16", api_key=None):
    if api_key is None:
        api_key = AGNES_API_KEY
    if not api_key:
        return None, "⚠️ AGNES_API_KEY set nahi hai."
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    width, height = (720, 1280) if ratio == "9:16" else (1280, 720)
    payload = {
        "model": "agnes-video-v2.0",
        "prompt": prompt,
        "width": width,
        "height": height,
        "num_frames": 121,
        "frame_rate": 24,
    }
    try:
        create_resp = requests.post(
            "https://apihub.agnes-ai.com/v1/videos",
            headers=headers, json=payload, timeout=60,
        )
        create_resp.raise_for_status()
        task = create_resp.json()
        video_id = task.get("video_id") or task.get("task_id") or task.get("id")
        if not video_id:
            return None, f"Error: video_id nahi mila. Response: {task}"
        poll_url = f"https://apihub.agnes-ai.com/agnesapi?video_id={video_id}"
        max_wait_seconds = 280
        poll_interval = 5
        waited = 0
        while waited < max_wait_seconds:
            time.sleep(poll_interval)
            waited += poll_interval
            poll_resp = requests.get(poll_url, headers=headers, timeout=30)
            poll_resp.raise_for_status()
            result = poll_resp.json()
            status = result.get("status")
            if status == "completed":
                video_url = result.get("url") or (result.get("metadata") or {}).get("url")
                if video_url:
                    return video_url, None
                return None, f"Error: video complete hua par url nahi mila. Response: {result}"
            elif status == "failed":
                err_info = result.get("error") or "unknown error"
                return None, f"Error: video generation fail hua — {err_info}"
        return None, "Error: video generate hone me bahut time lag raha hai (timeout)."
    except Exception as e:
        return None, f"Error: {e}"

def call_huggingface_video(prompt, model_id, ratio="9:16", api_key=None):
    """Hugging Face video generation - using Replicate for now"""
    if api_key is None:
        api_key = HF_API_KEY
    if not api_key:
        return None, "⚠️ HF_API_KEY set nahi hai."
    
    # Most HF video models require special handling
    # For now, return a message
    return None, "⚠️ Video models on HF require specific setup. Use Agnes Video for now."

# --- MUSIC APIs ---
def call_huggingface_music(prompt, model_id, api_key=None):
    """Hugging Face music generation"""
    if api_key is None:
        api_key = HF_API_KEY
    if not api_key:
        return None, "⚠️ HF_API_KEY set nahi hai."
    try:
        client = InferenceClient(api_key=api_key)
        audio = client.text_to_audio(prompt, model=model_id)
        return audio, None
    except Exception as e:
        return None, f"Error: {e}"

def call_minimax_music(prompt):
    api_key = get_secret("MINIMAX_API_KEY")
    if not api_key:
        return None, "⚠️ MINIMAX_API_KEY set nahi hai."
    url = "https://api.minimax.io/v1/music_generation"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "music-2.6",
        "prompt": prompt,
        "lyrics_optimizer": True,
        "is_instrumental": False,
        "stream": False,
        "output_format": "url",
        "audio_setting": {"sample_rate": 44100, "bitrate": 256000, "format": "mp3"},
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=180)
        resp.raise_for_status()
        data = resp.json()
        base_resp = data.get("base_resp") or {}
        status_code = base_resp.get("status_code")
        if status_code not in (None, 0):
            return None, f"Error: MiniMax {status_code} — {base_resp.get('status_msg', 'unknown error')}"
        audio_url = (data.get("data") or {}).get("audio")
        if not audio_url:
            return None, f"Error: audio_url nahi mila. Response: {data}"
        return audio_url, None
    except Exception as e:
        return None, f"Error: {e}"

def call_musicapi_music(prompt):
    api_key = get_secret("MUSICAPI_KEY")
    if not api_key:
        return None, "⚠️ MUSICAPI_KEY set nahi hai."
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    create_payload = {
        "custom_mode": False,
        "mv": "sonic-v4-5",
        "title": (prompt[:60] or "Dost AI Song"),
        "tags": "pop",
        "gpt_description_prompt": prompt,
        "make_instrumental": False,
    }
    try:
        resp = requests.post(
            "https://api.musicapi.ai/api/v1/sonic/create",
            headers=headers, json=create_payload, timeout=60,
        )
        resp.raise_for_status()
        task_id = resp.json().get("task_id")
        if not task_id:
            return None, f"Error: task_id nahi mila. Response: {resp.text[:300]}"
        poll_url = f"https://api.musicapi.ai/api/v1/sonic/task/{task_id}"
        for _ in range(40):
            time.sleep(6)
            poll_resp = requests.get(poll_url, headers=headers, timeout=30)
            poll_resp.raise_for_status()
            result = poll_resp.json()
            state = result.get("state") or result.get("status")
            if state == "succeeded":
                items = result.get("data") or []
                if items and items[0].get("audio_url"):
                    return items[0]["audio_url"], None
                return None, f"Error: song ready hua par audio_url nahi mila. Response: {result}"
            if state == "failed":
                return None, f"Error: MusicAPI generation fail hua — {result}"
        return None, "Error: music generate hone me bahut time lag raha hai (timeout)."
    except Exception as e:
        return None, f"Error: {e}"

# --- Translate API ---
def call_libretranslate(text, source="auto", target="en"):
    try:
        resp = requests.post("https://translate.terraprint.co/translate", 
                           json={"q": text, "source": source, "target": target, "format": "text"}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("translatedText"), None
    except Exception as e:
        return None, f"Translation error: {e}"

# ============================================================
# HEADER
# ============================================================
st.markdown(f"""
<div class="gemini-header">
    <div class="gemini-brand">
        <svg width="34" height="34" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="dostLogoBg" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stop-color="#4285f4"/>
                    <stop offset="50%" stop-color="#9b72cb"/>
                    <stop offset="100%" stop-color="#d96570"/>
                </linearGradient>
            </defs>
            <circle cx="32" cy="32" r="30" fill="url(#dostLogoBg)"/>
            <circle cx="24" cy="35" r="14" fill="white" opacity="0.95"/>
            <circle cx="40" cy="35" r="14" fill="white" opacity="0.55"/>
            <path d="M46 10 L48 15 L53 16 L48 17 L46 22 L44 17 L39 16 L44 15 Z" fill="#ffd166"/>
        </svg>
        <span class="gemini-title">{APP_NAME}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(f"<div style='font-size:20px; font-weight:500; padding:4px 12px 18px 12px; background:linear-gradient(90deg,#4285f4,#9b72cb,#d96570); -webkit-background-clip:text; -webkit-text-fill-color:transparent; display:inline-block;'>{APP_NAME}</div>", unsafe_allow_html=True)

    if st.button("✨  New chat", use_container_width=True):
        start_new_chat()

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    tabs = [
        ("💬 Chat", "chat"),
        ("🖼️ Image", "image"),
        ("🎬 Video", "video"),
        ("🎵 Music", "music"),
        ("📸 Gallery", "gallery"),
        ("🌐 Translate", "translate"),
    ]
    for label, key in tabs:
        if st.button(label, key=f"nav_{key}", use_container_width=True, 
                    type="primary" if st.session_state.active_tab == key else "secondary"):
            st.session_state.active_tab = key
            st.rerun()

    if st.session_state.chat_order:
        st.markdown("<div style='font-size:12px; color:#5f6368; font-weight:500; padding:18px 12px 6px 12px;'>Recent</div>", unsafe_allow_html=True)
        for cid in list(reversed(st.session_state.chat_order))[:8]:
            chat = st.session_state.chats.get(cid, {})
            label = chat.get("title", "New chat")
            if st.button(f"{label[:22]}", key=f"hist_{cid}", use_container_width=True):
                switch_chat(cid)

    _tokens_left = get_tokens_remaining(USER_EMAIL)

    with st.popover("⚙️  Settings", use_container_width=True):
        st.caption(f"💬 Chat free limit: {FREE_MSG_LIMIT_PER_DAY}/day")
        st.caption(f"🪙 Tokens today: {_tokens_left}/{TOKEN_LIMIT_PER_DAY} left")
        st.caption(f"🖼️ Image = {IMAGE_TOKEN_COST} tokens · 🎬 Video = {VIDEO_TOKEN_COST} tokens · 🎵 Music = {MUSIC_TOKEN_COST} tokens")
        st.caption("🔑 Keys in `.streamlit/secrets.toml`")

    st.progress(min(1.0, _tokens_left / TOKEN_LIMIT_PER_DAY), text=f"🪙 {_tokens_left}/{TOKEN_LIMIT_PER_DAY} tokens left today")

    _avatar_html = (
        f"<img src='{USER_PICTURE}' style='width:30px;height:30px;border-radius:50%;object-fit:cover;'/>"
        if USER_PICTURE else
        f"<div style='width:30px; height:30px; border-radius:50%; background:linear-gradient(135deg, #4285f4, #9b72cb); display:flex; align-items:center; justify-content:center; color:#fff; font-weight:700; font-size:12px;'>{USER_DISPLAY_NAME[:1].upper()}</div>"
    )
    st.markdown(f"""
    <div style='border-top:1px solid #f0f4f9; padding-top:12px; margin-top:12px;'>
        <div style='display:flex; align-items:center; gap:10px;'>
            {_avatar_html}
            <div style='overflow:hidden;'>
                <div style='font-weight:600; font-size:13px; color:#1f1f1f; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'>{USER_DISPLAY_NAME}</div>
                <div style='font-size:10px; color:#5f6368; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'>{USER_EMAIL or "Signed in"}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪  Logout", key="logout_btn", use_container_width=True):
        st.logout()

# ============================================================
# 🎨 GALLERY FOOTER
# ============================================================
HIGH_QUALITY_PROMPTS = [
    "beautiful anime girl with long flowing silver hair wearing elegant kimono with cherry blossom pattern standing in japanese garden soft morning light 8k ultra detailed portrait masterpiece studio ghibli style cinematic",
    "powerful samurai warrior in full armor holding katana dramatic sunset sky mountain background 8k ultra detailed portrait epic cinematic japanese art style",
    "magical girl with glowing crystal powers floating in neon cyberpunk city vibrant purple pink lights 8k ultra detailed portrait anime style futuristic",
    "ethereal fairy with translucent wings sitting on glowing mushroom in enchanted forest magical sparkles 8k ultra detailed portrait fantasy art dreamy",
    "dragon flying above ancient japanese castle full moon night cherry blossoms falling 8k ultra detailed portrait epic fantasy masterpiece dramatic",
]

def render_creativity_footer():
    selected_prompts = random.sample(HIGH_QUALITY_PROMPTS, min(5, len(HIGH_QUALITY_PROMPTS)))
    items_html = ""
    for prompt in selected_prompts:
        img_url = f"https://image.pollinations.ai/prompt/{quote(prompt)}?width=600&height=1067&model=flux&enhance=true&nologo=true"
        caption = prompt[:25] + "..." if len(prompt) > 25 else prompt
        items_html += f"""<div style='flex:0 0 auto;width:200px;border-radius:12px;overflow:hidden;border:1px solid #e8eaed;background:#f8f9fa;'>
            <img src='{img_url}' width='200' height='355' style='width:100%;height:355px;object-fit:cover;display:block;'>
            <div style='padding:6px 10px;font-size:9px;color:#5f6368;text-align:center;background:#f1f3f4;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>🎨 {caption}</div>
        </div>"""
    
    st.markdown(f"""
    <div style='margin-top:24px;padding:18px 0 12px 0;border-top:1px solid #e8eaed;text-align:center;'>
        <h2 style='font-size:24px;font-weight:700;background:linear-gradient(135deg,#4285f4,#9b72cb,#d96570);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;'>✨ Our Unique Creativity</h2>
        <p style='color:#5f6368;font-size:13px;margin-bottom:12px;'>4K Quality • 9:16 Ratio</p>
        <div style='display:flex;gap:20px;overflow-x:auto;padding:6px 0;'>
            {items_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 💬 CHAT TAB
# ============================================================
if st.session_state.active_tab == "chat":
    current_chat = st.session_state.chats[st.session_state.current_chat_id]
    
    if not current_chat["messages"]:
        st.markdown("""
        <div class="hero-text">
            <h1>Hello, Dost</h1>
            <p>How can I help you today?</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.container(height=440, border=False, key="chat_msg_box"):
            for msg in current_chat["messages"]:
                avatar = DOST_LOGO_AVATAR if msg["role"] == "assistant" else None
                with st.chat_message(msg["role"], avatar=avatar):
                    st.markdown(msg["content"])
    
    client_ip = get_client_ip()
    limit_hit = get_today_count(client_ip) >= FREE_MSG_LIMIT_PER_DAY
    
    # Model selector
    with st.popover("⚡ Model Select ▼", use_container_width=False):
        st.markdown("<div class='model-section-label free'>🚀 Free Chat Models</div>", unsafe_allow_html=True)
        for mid, info in CHAT_MODELS.items():
            selected = mid == st.session_state.selected_chat_model
            if st.button(f"{'✓ ' if selected else ''}{info['icon']} {info['label']}", key=f"model_{mid}", use_container_width=True):
                st.session_state.selected_chat_model = mid
                st.rerun()
            st.caption(info["desc"])
    
    if limit_hit:
        st.warning(f"Today's limit reached ({FREE_MSG_LIMIT_PER_DAY})")
        user_input = None
    else:
        with st.form(key="chat_input_form", clear_on_submit=True):
            col_text, col_btn = st.columns([12, 1])
            with col_text:
                typed_text = st.text_input(
                    "message", key="chat_text_field",
                    label_visibility="collapsed",
                    placeholder=f"Ask {APP_NAME}..."
                )
            with col_btn:
                sent = st.form_submit_button("➤")
        user_input = typed_text.strip() if sent and typed_text and typed_text.strip() else None
    
    if user_input:
        current_chat["messages"].append({"role": "user", "content": user_input})
        if current_chat["title"] is None:
            current_chat["title"] = user_input[:35] + "…"
            st.session_state.chat_order.append(st.session_state.current_chat_id)
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant", avatar=DOST_LOGO_AVATAR):
            with st.spinner("Thinking..."):
                try:
                    api_messages = [{"role": m["role"], "content": m["content"]} for m in current_chat["messages"]]
                    model_info = CHAT_MODELS[st.session_state.selected_chat_model]
                    provider = model_info.get("provider")
                    
                    if provider == "groq":
                        reply = call_groq_chat(GROQ_API_KEY, model_info["model_id"], api_messages, TEMPERATURE)
                    elif provider == "cerebras":
                        reply = call_cerebras_chat(CEREBRAS_API_KEY, model_info["model_id"], api_messages, TEMPERATURE)
                    elif provider == "pollinations":
                        reply = call_pollinations_chat(api_messages, TEMPERATURE)
                    elif provider == "huggingface_chat":
                        reply = call_huggingface_chat(HF_API_KEY, model_info["model_id"], api_messages, TEMPERATURE)
                    else:
                        reply = "⚠️ Model not configured yet."
                    
                    st.markdown(reply)
                    current_chat["messages"].append({"role": "assistant", "content": reply})
                    increment_today_count(client_ip)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
    
    render_creativity_footer()

# ============================================================
# 🖼️ IMAGE TAB
# ============================================================
if st.session_state.active_tab == "image":
    st.markdown("<div class='hero-text'><h1>AI Image Studio</h1><p>15+ Free Models • 9:16 Ratio</p></div>", unsafe_allow_html=True)

    with st.container(key="img_studio_card"):
        img_prompt = st.text_area("Describe your image",
                                 placeholder="Jaise: beautiful anime girl with flowing hair",
                                 height=70,
                                 label_visibility="collapsed",
                                 key="img_prompt_input")

        col1, col2, col3 = st.columns([2, 1, 1.5])
        with col1:
            img_model = st.selectbox("Model", list(IMAGE_MODELS.keys()),
                                    format_func=lambda x: f"{IMAGE_MODELS[x]['icon']} {IMAGE_MODELS[x]['label']}",
                                    key="img_model_select",
                                    label_visibility="collapsed")
        with col2:
            img_ratio = st.selectbox("Ratio", ["9:16", "16:9"],
                                    format_func=lambda x: f"▢ {x} HD",
                                    key="img_ratio_select",
                                    label_visibility="collapsed")
        with col3:
            gen_clicked = st.button("✦ Generate Image", key="gen_image_btn", use_container_width=True)
        st.caption(f"🪙 {IMAGE_TOKEN_COST} tokens/image · {get_tokens_remaining(USER_EMAIL)} left today")

    if gen_clicked:
        if not img_prompt.strip():
            st.warning("Pehle prompt likho.")
        elif get_tokens_remaining(USER_EMAIL) < IMAGE_TOKEN_COST:
            st.error(f"❌ Aaj ke free tokens khatam ho gaye. Image ke liye {IMAGE_TOKEN_COST} tokens chahiye, sirf {get_tokens_remaining(USER_EMAIL)} bache hain.")
        else:
            model_info = IMAGE_MODELS[img_model]
            provider = model_info.get("provider")
            
            if provider == "pollinations":
                img_url = run_with_progress(
                    lambda: get_image_url_pollinations(img_prompt, img_ratio),
                    estimate_seconds=8, label="Image ban raha hai")
                deduct_tokens(USER_EMAIL, IMAGE_TOKEN_COST)
                st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
                st.image(img_url, caption=img_prompt, use_container_width=True)
                st.session_state.gallery.insert(0, {"url": img_url, "prompt": img_prompt, "type": "image"})
                
            elif provider == "agnes":
                img_url, err = run_with_progress(
                    lambda: call_agnes_image(img_prompt, img_ratio, AGNES_API_KEY),
                    estimate_seconds=15, label="Image ban raha hai")
                if err:
                    st.error(err)
                else:
                    deduct_tokens(USER_EMAIL, IMAGE_TOKEN_COST)
                    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
                    st.image(img_url, caption=img_prompt, use_container_width=True)
                    st.session_state.gallery.insert(0, {"url": img_url, "prompt": img_prompt, "type": "image"})
                    
            elif provider == "huggingface":
                model_id = model_info.get("model")
                img_bytes, err = run_with_progress(
                    lambda: call_huggingface_image(img_prompt, model_id, img_ratio, HF_API_KEY),
                    estimate_seconds=20, label="Image ban raha hai")
                if err:
                    st.error(err)
                else:
                    deduct_tokens(USER_EMAIL, IMAGE_TOKEN_COST)
                    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
                    st.image(img_bytes, caption=f"{model_info['label']}: {img_prompt}", use_container_width=True)
                    # Store in gallery (can't store bytes in session state easily)
                    st.session_state.gallery.insert(0, {"url": "data:image/png;base64," + base64.b64encode(img_bytes).decode(), "prompt": img_prompt, "type": "image"})

    render_creativity_footer()

# ============================================================
# 🎬 VIDEO TAB
# ============================================================
if st.session_state.active_tab == "video":
    st.markdown("<div class='hero-text'><h1>AI Video Studio</h1><p>8+ Free Models</p></div>", unsafe_allow_html=True)

    with st.container(key="vid_studio_card"):
        vid_prompt = st.text_area("Describe your video",
                                 placeholder="Jaise: eagle flying over mountains",
                                 height=70,
                                 label_visibility="collapsed",
                                 key="vid_prompt_input")

        col1, col2, col3 = st.columns([2, 1, 1.5])
        with col1:
            vid_model = st.selectbox("Model", list(VIDEO_MODELS.keys()),
                                    format_func=lambda x: f"{VIDEO_MODELS[x]['icon']} {VIDEO_MODELS[x]['label']}",
                                    key="vid_model_select",
                                    label_visibility="collapsed")
        with col2:
            vid_ratio = st.selectbox("Ratio", ["9:16", "16:9"],
                                    format_func=lambda x: f"▢ {x} HD",
                                    key="vid_ratio_select",
                                    label_visibility="collapsed")
        with col3:
            gen_vid_clicked = st.button("✦ Generate Video", key="gen_video_btn", use_container_width=True)
        st.caption(f"🪙 {VIDEO_TOKEN_COST} tokens/video · {get_tokens_remaining(USER_EMAIL)} left today")

    if gen_vid_clicked:
        if not vid_prompt.strip():
            st.warning("Pehle prompt likho.")
        elif get_tokens_remaining(USER_EMAIL) < VIDEO_TOKEN_COST:
            st.error(f"❌ Aaj ke free tokens khatam ho gaye. Video ke liye {VIDEO_TOKEN_COST} tokens chahiye, sirf {get_tokens_remaining(USER_EMAIL)} bache hain.")
        else:
            model_info = VIDEO_MODELS[vid_model]
            provider = model_info.get("provider")
            
            if provider == "agnes":
                vid_url, err = run_with_progress(
                    lambda: call_agnes_video(vid_prompt, vid_ratio, AGNES_API_KEY),
                    estimate_seconds=55, label="Video ban raha hai")
                if err:
                    st.error(err)
                else:
                    deduct_tokens(USER_EMAIL, VIDEO_TOKEN_COST)
                    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
                    st.video(vid_url)
                    st.caption(f"🎬 {vid_prompt}")
                    
            elif provider == "huggingface_video":
                model_id = model_info.get("model")
                vid_url, err = run_with_progress(
                    lambda: call_huggingface_video(vid_prompt, model_id, vid_ratio, HF_API_KEY),
                    estimate_seconds=90, label="Video ban raha hai")
                if err:
                    st.error(err if "setup" not in err else "⚠️ HF video models require Replicate API key. Use Agnes Video for now.")
                else:
                    if vid_url:
                        deduct_tokens(USER_EMAIL, VIDEO_TOKEN_COST)
                        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
                        st.video(vid_url)

    render_creativity_footer()

# ============================================================
# 🎵 MUSIC TAB
# ============================================================
if st.session_state.active_tab == "music":
    st.markdown("<div class='hero-text'><h1>AI Music Studio</h1><p>MusicGen • AudioCraft • MusicAPI</p></div>", unsafe_allow_html=True)
    
    song_prompt = st.text_area("Describe your song", 
                              placeholder="Jaise: uplifting Hindi devotional or lo-fi beat",
                              height=60, 
                              label_visibility="collapsed",
                              key="song_prompt_input")

    col_model, col_btn = st.columns([2, 1.5])
    with col_model:
        music_model = st.selectbox("Model", list(MUSIC_MODELS.keys()),
                                  format_func=lambda x: f"{MUSIC_MODELS[x]['icon']} {MUSIC_MODELS[x]['label']}",
                                  key="music_model_select",
                                  label_visibility="collapsed")
    with col_btn:
        gen_music_clicked = st.button("✦ Generate Music", key="gen_music_btn", use_container_width=True)

    if gen_music_clicked:
        if not song_prompt.strip():
            st.warning("Pehle description likho.")
        else:
            model_info = MUSIC_MODELS[music_model]
            provider = model_info.get("provider")
            
            with st.spinner("Music generate ho raha hai..."):
                if provider == "huggingface_music":
                    model_id = model_info.get("model")
                    audio_data, err = call_huggingface_music(song_prompt, model_id, HF_API_KEY)
                    if err:
                        st.error(err)
                    else:
                        st.audio(audio_data, format="audio/wav")
                        st.caption(f"🎵 {song_prompt}")
                        
                elif provider == "musicapi":
                    audio_url, err = call_musicapi_music(song_prompt)
                    if err:
                        st.error(err)
                    else:
                        st.audio(audio_url, format="audio/mp3")
                        st.caption(f"🎵 {song_prompt}")
    
    render_creativity_footer()

# ============================================================
# 🌐 TRANSLATE TAB
# ============================================================
if st.session_state.active_tab == "translate":
    st.markdown("<div class='hero-text'><h1>Free Translate</h1><p>LibreTranslate • 100+ Languages</p></div>", unsafe_allow_html=True)
    
    LANGS = {"Auto": "auto", "Hindi": "hi", "English": "en", "Marathi": "mr", 
             "Gujarati": "gu", "Tamil": "ta", "Telugu": "te", "Bengali": "bn", 
             "Spanish": "es", "French": "fr", "Arabic": "ar", "Japanese": "ja",
             "German": "de", "Italian": "it", "Portuguese": "pt", "Russian": "ru"}
    
    col1, col2 = st.columns(2)
    with col1:
        src = st.selectbox("Source", list(LANGS.keys()), index=0, key="src_lang")
    with col2:
        tgt = st.selectbox("Target", list(LANGS.keys()), index=2, key="tgt_lang")
    
    text = st.text_area("Text", height=80, placeholder="Yahan text likho...", label_visibility="collapsed", key="translate_text")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("✦ Translate", key="gen_translate_btn", use_container_width=True):
            if not text.strip():
                st.warning("Pehle text likho.")
            else:
                translated, err = call_libretranslate(text.strip(), LANGS[src], LANGS[tgt])
                if err:
                    st.error(err)
                else:
                    st.text_area("Translation", value=translated, height=80, disabled=True, key="translated_output")
    
    render_creativity_footer()

# ============================================================
# 📸 GALLERY TAB
# ============================================================
if st.session_state.active_tab == "gallery":
    st.markdown("<div class='hero-text'><h1>Your Gallery</h1><p>All creations</p></div>", unsafe_allow_html=True)
    
    if not st.session_state.gallery:
        st.caption("Abhi kuch generate nahi kiya.")
    else:
        cols = st.columns(3)
        for i, item in enumerate(st.session_state.gallery[:24]):
            with cols[i % 3]:
                if item["type"] == "image":
                    st.image(item["url"], use_container_width=True)
                    st.caption(item["prompt"][:40] + "...")
    
    render_creativity_footer()

# ============================================================
# END
# ============================================================
st.markdown("</div>", unsafe_allow_html=True)
