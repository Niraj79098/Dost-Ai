"""
🧡 Dost AI — COMPLETE FREE AI STUDIO
All Free AI Tools: Chat, Image, Video, Music, Story, Anime, AI Girlfriend, Uncensored Chat
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
from datetime import date
from urllib.parse import quote
import random
import streamlit.components.v1 as components
import json
import httpx

# ============================================================
# 🔐 SECURE SECRETS - IMPROVED
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
# 🔐 API KEYS - ALL FREE MODELS
# ============================================================
# Existing
GROQ_API_KEY = get_secret("GROQ_API_KEY")
CEREBRAS_API_KEY = get_secret("CEREBRAS_API_KEY")
MISTRAL_API_KEY = get_secret("MISTRAL_API_KEY")
AGNES_API_KEY = get_secret("AGNES_API_KEY")
MINIMAX_API_KEY = get_secret("MINIMAX_API_KEY")
MUSICAPI_KEY = get_secret("MUSICAPI_KEY")

# New Free Models
AION_API_KEY = get_secret("AION_API_KEY")
INNERHAVEN_API_KEY = get_secret("INNERHAVEN_API_KEY")
WESHOP_API_KEY = get_secret("WESHOP_API_KEY")
GOOGLE_API_KEY = get_secret("GOOGLE_API_KEY")
ZHIPU_API_KEY = get_secret("ZHIPU_API_KEY")

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
# 🎨 HIGH QUALITY PROMPTS
# ============================================================
HIGH_QUALITY_PROMPTS = [
    "beautiful anime girl with long flowing silver hair wearing elegant kimono with cherry blossom pattern standing in japanese garden soft morning light 8k ultra detailed portrait masterpiece studio ghibli style cinematic",
    "powerful samurai warrior in full armor holding katana dramatic sunset sky mountain background 8k ultra detailed portrait epic cinematic japanese art style",
    "magical girl with glowing crystal powers floating in neon cyberpunk city vibrant purple pink lights 8k ultra detailed portrait anime style futuristic",
    "ethereal fairy with translucent wings sitting on glowing mushroom in enchanted forest magical sparkles 8k ultra detailed portrait fantasy art dreamy",
    "dragon flying above ancient japanese castle full moon night cherry blossoms falling 8k ultra detailed portrait epic fantasy masterpiece dramatic",
    "beautiful goddess with flowing golden hair wearing white flowing dress standing in clouds with sun rays 8k ultra detailed portrait divine ethereal",
    "cyberpunk warrior woman with neon glowing armor futuristic city background rain neon lights 8k ultra detailed portrait cinematic blade runner",
    "mysterious fox spirit with nine tails floating in magical forest glowing blue orbs 8k ultra detailed portrait anime enchanting",
    "warrior princess with flowing red cape standing on cliff edge dramatic storm sky lightning 8k ultra detailed portrait epic fantasy cinematic",
    "beautiful mermaid with pearl necklace sitting on rock in ocean sunset waves crashing 8k ultra detailed portrait fantasy art dreamy",
]

# ============================================================
# MODEL TIERS - EXTENDED WITH ALL NEW MODELS
# ============================================================
MODEL_TIERS = {
    "free": {
        "label": "Free",
        "models": {
            "groq-lite": {
                "label": "Groq Lite",
                "icon": "⚡",
                "desc": "Sabse fast",
                "provider": "groq",
                "model_id": "openai/gpt-oss-20b",
            },
            "groq-standard": {
                "label": "Groq Standard",
                "icon": "💬",
                "desc": "All-round powerful",
                "provider": "groq",
                "model_id": "openai/gpt-oss-120b",
                "badge": "New",
            },
            "cerebras": {
                "label": "Cerebras AI",
                "icon": "🧠",
                "desc": "1M tokens/min",
                "provider": "cerebras",
                "model_id": "llama3.1-70b",
            },
            "mistral": {
                "label": "Mistral",
                "icon": "🌪️",
                "desc": "Open-source expert",
                "provider": "mistral",
                "model_id": "open-mistral-7b",
            },
            "pollinations-text": {
                "label": "Pollinations",
                "icon": "🌐",
                "desc": "Bilkul free, no key",
                "provider": "pollinations",
            },
            "aion-roleplay": {
                "label": "Aion Roleplay",
                "icon": "🎭",
                "desc": "Storytelling & RP",
                "provider": "aion",
                "model_id": "aion-3.0",
                "badge": "New",
            },
            "zhipu": {
                "label": "Zhipu AI",
                "icon": "🧠",
                "desc": "Reasoning expert",
                "provider": "zhipu",
                "model_id": "glm-4.7-flash",
                "badge": "New",
            },
        },
    },
    "pro": {
        "label": "Pro · Add Key",
        "models": {
            "agnes-image": {
                "label": "Agnes Image",
                "icon": "🖼️",
                "desc": "Free image gen",
                "kind": "image",
                "secret_name": "AGNES_API_KEY",
                "model": "agnes-image-2.1-flash",
            },
            "agnes-video": {
                "label": "Agnes Video",
                "icon": "🎬",
                "desc": "Free video gen",
                "kind": "video",
                "secret_name": "AGNES_API_KEY",
                "model": "agnes-video-v2.0",
            },
            "minimax-music": {
                "label": "MiniMax Music",
                "icon": "🎵",
                "desc": "100 calls/day",
                "kind": "music",
                "secret_name": "MINIMAX_API_KEY",
            },
            "musicapi-sonic": {
                "label": "MusicAPI Sonic",
                "icon": "🎼",
                "desc": "75 free credits",
                "kind": "music",
                "secret_name": "MUSICAPI_KEY",
            },
            "google-gemini": {
                "label": "Google Gemini",
                "icon": "🌟",
                "desc": "15 RPM, 1500 RPD",
                "kind": "chat",
                "secret_name": "GOOGLE_API_KEY",
                "model": "gemini-2.0-flash",
                "badge": "New",
            },
        },
    },
}

DEFAULT_CHAT_MODEL = "groq-standard"

# ============================================================
# IMAGE MODELS - EXTENDED
# ============================================================
IMAGE_MODELS = {
    "pollinations": {"label": "Pollinations AI", "icon": "🖼️", "desc": "Bilkul free, no key"},
    "agnes": {"label": "Agnes AI", "icon": "🤖", "desc": "Free, high quality"},
}

# ============================================================
# VIDEO MODELS
# ============================================================
VIDEO_MODELS = {
    "agnes": {"label": "Agnes AI", "icon": "🤖", "desc": "Free video gen"},
}

# ============================================================
# MUSIC MODELS
# ============================================================
MUSIC_MODELS = {
    "minimax": {"label": "MiniMax", "icon": "🎵", "desc": "100 calls/day"},
    "musicapi": {"label": "MusicAPI Sonic", "icon": "🎼", "desc": "75 free credits"},
}

# ============================================================
# STORY GENRES
# ============================================================
STORY_GENRES = {
    "fantasy": {"label": "🏰 Fantasy", "desc": "Dragons, magic, kingdoms"},
    "scifi": {"label": "🚀 Sci-Fi", "desc": "Space, future, technology"},
    "romance": {"label": "❤️ Romance", "desc": "Love, emotions, drama"},
    "mystery": {"label": "🔍 Mystery", "desc": "Suspense, thriller, detective"},
    "adventure": {"label": "🗺️ Adventure", "desc": "Travel, exploration, action"},
    "horror": {"label": "👻 Horror", "desc": "Ghosts, terror, nightmare"},
    "comedy": {"label": "😂 Comedy", "desc": "Humor, funny, laughter"},
    "anime": {"label": "🎌 Anime", "desc": "Manga, Japanese animation style"},
}

# ============================================================
# ANIME STYLES
# ============================================================
ANIME_STYLES = {
    "ghibli": {"label": "Studio Ghibli", "desc": "Soft, dreamy, magical"},
    "shonen": {"label": "Shonen Jump", "desc": "Bold, action, dramatic"},
    "shoujo": {"label": "Shojo", "desc": "Romantic, elegant, sparkly"},
    "cyberpunk": {"label": "Cyberpunk", "desc": "Neon, futuristic, edgy"},
    "vintage": {"label": "Vintage 80s", "desc": "Retro, classic anime style"},
    "chibi": {"label": "Chibi", "desc": "Cute, small, kawaii"},
    "realistic": {"label": "Realistic", "desc": "Detailed, lifelike anime"},
    "watercolor": {"label": "Watercolor", "desc": "Soft, artistic, painted"},
}

# ============================================================
# AI GIRLFRIEND PERSONALITIES
# ============================================================
GF_PERSONALITIES = {
    "caring": {"label": "💕 Caring", "desc": "Sweet, loving, supportive girlfriend"},
    "flirty": {"label": "😉 Flirty", "desc": "Playful, teasing, romantic"},
    "sassy": {"label": "🔥 Sassy", "desc": "Confident, witty, independent"},
    "innocent": {"label": "🌸 Innocent", "desc": "Shy, pure, cute girlfriend"},
    "dominant": {"label": "👑 Dominant", "desc": "Strong, protective, bossy"},
    "submissive": {"label": "🌹 Submissive", "desc": "Gentle, obedient, sweet"},
    "nerdy": {"label": "🤓 Nerdy", "desc": "Smart, geeky, intellectual"},
    "adult": {"label": "🔞 Adult 18+", "desc": "Mature, explicit content (age verified only)"},
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
# CUSTOM CSS - SAME AS ORIGINAL (UNCHANGED)
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto:wght@300;400;500;600;700&display=swap');

* { font-family: 'Google Sans', 'Roboto', 'Segoe UI', sans-serif !important; }

span[data-testid="stIconMaterial"],
[class*="material-symbols"],
[class*="material-icons"] {
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
}

.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 0.5rem !important;
    padding-left: 0.5rem !important;
    padding-right: 0.5rem !important;
    max-width: 100% !important;
}
div[data-testid="stElementContainer"],
div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"],
div[data-testid="column"],
div[data-testid="column"] > div,
div.st-emotion-cache-1r6slb0 {
    padding: 0 !important;
    margin: 0 !important;
    gap: 0 !important;
}

section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"] {
    margin-bottom: 6px !important;
}

.main-glass div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"] {
    margin-bottom: 10px !important;
}
.main-glass div[data-testid="stHorizontalBlock"] {
    gap: 24px !important;
    align-items: flex-end !important;
}

.stApp > header,
.stApp > footer {
    display: none !important;
}

.stApp {
    background: #ffffff;
    min-height: 100vh;
}

section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: none !important;
    padding-top: 16px !important;
    padding-left: 10px !important;
    padding-right: 10px !important;
}
section[data-testid="stSidebar"] * {
    color: #1f1f1f !important;
}
section[data-testid="stSidebar"] hr {
    display: none !important;
}
section[data-testid="stSidebar"] div.stButton > button {
    background: transparent !important;
    border: none !important;
    border-radius: 24px !important;
    color: #444746 !important;
    text-align: left !important;
    padding: 12px 16px !important;
    margin-bottom: 4px !important;
    font-weight: 400 !important;
    font-size: 14px !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] div.stButton > button:hover {
    background: #f0f4f9 !important;
}
section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background: #d3e3fd !important;
    border: none !important;
    color: #041e49 !important;
    font-weight: 500 !important;
}
section[data-testid="stSidebar"] div[data-testid="stPopover"] button {
    background: transparent !important;
    border: none !important;
    border-radius: 24px !important;
    color: #444746 !important;
    text-align: left !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] div[data-testid="stPopover"] button:hover {
    background: #f0f4f9 !important;
}

.main-glass {
    background: #ffffff;
    max-width: 900px;
    padding: 6px 18px 10px 18px;
    margin: 0 auto;
    border: none;
}

.gemini-header {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    padding: 50px 0 10px 0 !important;
    border-bottom: none !important;
    background: transparent !important;
    position: relative !important;
    z-index: 100 !important;
    margin-bottom: 4px !important;
}
.gemini-brand {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    background: transparent !important;
}
.gemini-brand svg {
    width: 34px !important;
    height: 34px !important;
}
.gemini-title {
    font-size: 22px !important;
    font-weight: 600 !important;
    background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}
.gemini-avatar {
    width: 36px !important;
    height: 36px !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, #4285f4, #34a853) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    color: #fff !important;
}

.hero-text {
    text-align: center;
    padding: 32px 0 24px 0;
}
.hero-text h1 {
    font-size: 30px;
    font-weight: 600;
    background: linear-gradient(135deg, #4285f4, #9b72cb, #d96570);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 4px 0;
}
.hero-text p {
    font-size: 15px;
    color: #5f6368;
    margin: 0 0 28px 0;
}

.quick-actions {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    max-width: 650px;
    margin: 14px auto 10px auto;
}
.quick-action-btn {
    background: #f0f4f9;
    border: none;
    border-radius: 18px;
    padding: 16px 14px;
    text-align: left;
    transition: background 0.15s ease;
    cursor: pointer;
}
.quick-action-btn:hover {
    background: #e8eef6;
}
.quick-action-btn .icon { font-size: 20px; display: block; margin-bottom: 10px; }
.quick-action-btn .label { color: #1f1f1f; font-weight: 400; font-size: 14px; }
.quick-action-btn .desc { color: #5f6368; font-size: 11px; margin-top: 2px; }

.chat-wrapper {
    max-width: 700px;
    margin: 10px auto 0 auto;
    position: relative;
}
.chat-wrapper .stChatInput {
    max-width: 100% !important;
}
.chat-wrapper .stChatInput textarea {
    background: #f0f4f9 !important;
    border: 1px solid #e8eaed !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    font-size: 15px !important;
    color: #1f1f1f !important;
    min-height: 52px !important;
}
.chat-wrapper .stChatInput textarea:focus {
    border-color: #4285f4 !important;
    box-shadow: 0 0 0 3px rgba(66,133,244,0.12) !important;
}

div[data-testid="stForm"] {
    border: 1px solid #e0e3e8 !important;
    border-radius: 28px !important;
    padding: 30px 50px 30px 50px !important;
    background: #f8f9fb !important;
    margin-top: 10px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
    transition: box-shadow 0.15s ease, border-color 0.15s ease;
}
div[data-testid="stForm"]:focus-within {
    border-color: #4285f4 !important;
    box-shadow: 0 1px 8px rgba(66,133,244,0.18) !important;
}
div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] {
    align-items: center !important;
    gap: 8px !important;
}
div[data-testid="stForm"] input[type="text"] {
    background: transparent !important;
    color: #1f1f1f !important;
    border: none !important;
    padding: 14px 4px !important;
    height: 30px !important;
    font-size: 15px !important;
}
div[data-testid="stForm"] input[type="text"]:focus {
    box-shadow: none !important;
    outline: none !important;
}
div[data-testid="stFormSubmitButton"] button {
    border-radius: 50% !important;
    width: 42px !important;
    height: 42px !important;
    padding: 0 !important;
    background: #4285f4 !important;
    color: #fff !important;
    border: none !important;
    font-size: 17px !important;
    box-shadow: none !important;
}
div[data-testid="stFormSubmitButton"] button:hover {
    background: #3367d6 !important;
}

.main-glass div[data-testid="stPopover"] {
    display: flex !important;
    justify-content: flex-end !important;
    margin-bottom: 8px !important;
}
.main-glass div[data-testid="stPopover"] > button {
    background: #f0f4f9 !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 6px 16px !important;
    font-size: 12px !important;
    color: #444746 !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    width: auto !important;
}
.main-glass div[data-testid="stPopover"] > button:hover {
    background: #e8eef6 !important;
}

div[data-testid="stPopoverBody"] {
    min-width: 230px !important;
}
div[data-testid="stPopoverBody"] div.stButton > button {
    background: #f7f9fc !important;
    color: #1f1f1f !important;
    border: 1px solid #e3e8ef !important;
    border-radius: 12px !important;
    padding: 7px 12px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-align: left !important;
    box-shadow: none !important;
    margin-bottom: 1px !important;
}
div[data-testid="stPopoverBody"] div.stButton > button:hover {
    background: #eef2f8 !important;
    border-color: #c7d2e0 !important;
}
div[data-testid="stPopoverBody"] div.stButton > button:disabled {
    opacity: 0.5 !important;
}
div[data-testid="stPopoverBody"] .stCaption {
    margin: -4px 0 8px 4px !important;
}
.model-section-label {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    padding: 13px 12px 16px 2px;
    border-radius: 8px;
    margin: 8px 0 8px 2px;
}
.model-section-label.free { background: #e8f0fe; color: #1a56db; }
.model-section-label.pro { background: #fdeee9; color: #b3541e; }

.main-glass div[data-testid="stTextArea"] textarea {
    background: #f0f4f9 !important;
    border: 1px solid #e8eaed !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    font-size: 15px !important;
    color: #1f1f1f !important;
}
.main-glass div[data-testid="stTextArea"] textarea:focus {
    border-color: #4285f4 !important;
    box-shadow: 0 0 0 3px rgba(66,133,244,0.12) !important;
}

.main-glass div[data-testid="stSelectbox"] label {
    font-size: 12px !important;
    color: #5f6368 !important;
    font-weight: 500 !important;
    margin-bottom: 4px !important;
}
.main-glass div[data-testid="stSelectbox"] > div > div {
    background: #f0f4f9 !important;
    border: 1px solid #e8eaed !important;
    border-radius: 14px !important;
    min-height: 44px !important;
}
.main-glass div[data-testid="stSelectbox"] > div > div:hover {
    border-color: #4285f4 !important;
}

@media (max-width: 640px) {
    .main-glass div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextArea"]) {
        flex-wrap: wrap !important;
    }
    .main-glass div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextArea"]) > div[data-testid="column"] {
        min-width: 100% !important;
    }
}

.stChatMessage {
    background: #f0f4f9 !important;
    border: none !important;
    border-radius: 18px !important;
    padding: 12px 18px !important;
    margin-bottom: 10px !important;
    box-shadow: none !important;
}
.stChatMessage p, .stChatMessage span {
    color: #1f1f1f !important;
}

div.st-key-chat_msg_box {
    height: auto !important;
    max-height: 58vh !important;
    overflow-y: auto !important;
    padding-right: 6px !important;
}
div.st-key-chat_msg_box::-webkit-scrollbar {
    width: 6px;
}
div.st-key-chat_msg_box::-webkit-scrollbar-thumb {
    background: #d8dde3;
    border-radius: 10px;
}

div.stButton > button {
    border-radius: 20px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    border: none !important;
    background: #4285f4 !important;
    color: white !important;
    box-shadow: none !important;
}
div.stButton > button:hover {
    background: #3367d6 !important;
}

.creativity-footer {
    margin-top: 24px;
    padding: 18px 0 12px 0;
    border-top: 1px solid #e8eaed;
    text-align: center;
}
.creativity-footer h2 {
    font-size: 24px;
    font-weight: 700;
    background: linear-gradient(135deg, #4285f4, #9b72cb, #d96570);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}
.creativity-footer .subtitle {
    color: #5f6368;
    font-size: 13px;
    margin-bottom: 12px;
}

.scroll-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 6px 0;
}
.scroll-container {
    width: 82%;
    overflow: hidden;
    border-radius: 14px;
}
.scroll-track {
    display: flex;
    gap: 20px;
    transition: transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    width: max-content;
}
.scroll-item {
    flex: 0 0 auto;
    width: 200px;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #e8eaed;
    background: #f8f9fa;
    transition: all 0.3s ease;
}
.scroll-item:hover {
    transform: scale(1.05);
    border-color: #4285f4;
    box-shadow: 0 4px 18px rgba(66,133,244,0.15);
    z-index: 5;
}
.scroll-item img {
    width: 100%;
    height: 355px;
    object-fit: cover;
    display: block;
    aspect-ratio: 9/16;
}
.scroll-item .caption {
    padding: 6px 10px;
    font-size: 9px;
    color: #5f6368;
    text-align: center;
    background: #f1f3f4;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.scroll-btn {
    background: #e8f0fe !important;
    border: 1px solid #d2e3fc !important;
    border-radius: 50% !important;
    width: 42px !important;
    height: 42px !important;
    min-width: 42px !important;
    padding: 0 !important;
    font-size: 18px !important;
    color: #1a73e8 !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.3s ease !important;
}
.scroll-btn:hover {
    background: #d2e3fc !important;
    transform: scale(1.1) !important;
}

.sidebar-divider {
    border-top: 1px solid #e8eaed;
    margin: 10px 0;
}

@media (max-width: 768px) {
    .main-glass { padding: 8px 10px; margin: 0 auto; }
    .hero-text { padding: 20px 0 14px 0; }
    .hero-text h1 { font-size: 22px; }
    .quick-actions { grid-template-columns: 1fr 1fr; gap: 8px; }
    .scroll-item { width: 140px; }
    .scroll-item img { height: 248px; }
    .scroll-container { width: 72%; }
    .scroll-btn { width: 34px !important; height: 34px !important; min-width: 34px !important; font-size: 14px !important; }
    .main-glass div[data-testid="stPopover"] > button { font-size: 11px !important; padding: 5px 12px !important; }
    .gemini-title { font-size: 17px !important; }
    .gemini-brand svg { width: 26px !important; height: 26px !important; }
    .gemini-avatar { width: 28px !important; height: 28px !important; font-size: 12px !important; }
    div[data-testid="stForm"] { padding: 30px 10px 20px 10px !important; }
    div[data-testid="stForm"] input[type="text"] { font-size: 14px !important; padding: 11px 4px !important; }
    div[data-testid="stFormSubmitButton"] button { width: 36px !important; height: 36px !important; font-size: 15px !important; }
}
@media (max-width: 480px) {
    .quick-actions { grid-template-columns: 1fr; }
    .scroll-item { width: 120px; }
    .scroll-item img { height: 213px; }
}
</style>

<div class="main-glass">
""", unsafe_allow_html=True)

# --- Studio Card Styling ---
st.markdown("""
<style>
div.st-key-img_studio_card, div.st-key-vid_studio_card {
    background: center;
    border: 1px solid #232323 !important;
    border-radius: 22px !important;
    padding: 20px 22px 22px 22px !important;
    max-width: 800px !important;
    margin: 4px auto 26px auto !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.25);
}
div.st-key-img_studio_card div[data-testid="stTextArea"],
div.st-key-vid_studio_card div[data-testid="stTextArea"] {
    margin-bottom: 6px !important;
}
div.st-key-img_studio_card div[data-testid="stTextArea"] textarea,
div.st-key-vid_studio_card div[data-testid="stTextArea"] textarea {
    background: transparent !important;
    border: none !important;
    color: black;
    font-size: 16px !important;
    padding: 6px 4px 14px 4px !important;
    min-height: 60px !important;
}
div.st-key-img_studio_card div[data-testid="stTextArea"] textarea::placeholder,
div.st-key-vid_studio_card div[data-testid="stTextArea"] textarea::placeholder {
    color: #8a8a8a !important;
}
div.st-key-img_studio_card div[data-testid="stTextArea"] textarea:focus,
div.st-key-vid_studio_card div[data-testid="stTextArea"] textarea:focus {
    box-shadow: none !important;
    border: none !important;
}
div.st-key-img_studio_card div[data-testid="stHorizontalBlock"],
div.st-key-vid_studio_card div[data-testid="stHorizontalBlock"] {
    border-top: 1px solid #212121 !important;
    padding-top: 18px !important;
    margin-top: 10px !important;
    align-items: center !important;
    gap: 16px !important;
}
div.st-key-img_studio_card div[data-testid="stHorizontalBlock"] > div[data-testid="column"],
div.st-key-vid_studio_card div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    padding: 0 4px !important;
}
div.st-key-img_studio_card div[data-testid="stSelectbox"] label,
div.st-key-vid_studio_card div[data-testid="stSelectbox"] label {
    display: none !important;
}
div.st-key-img_studio_card div[data-testid="stSelectbox"] > div > div,
div.st-key-vid_studio_card div[data-testid="stSelectbox"] > div > div {
    background: #161616 !important;
    border: 1px solid #2b2b2b !important;
    border-radius: 20px !important;
    color: #f0f0f0 !important;
    min-height: 42px !important;
    font-size: 13px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
div.st-key-img_studio_card div[data-testid="stSelectbox"] *,
div.st-key-vid_studio_card div[data-testid="stSelectbox"] * {
    color: #f0f0f0 !important;
    fill: #f0f0f0 !important;
}
div.st-key-img_studio_card div[data-testid="stSelectbox"] > div > div:hover,
div.st-key-vid_studio_card div[data-testid="stSelectbox"] > div > div:hover {
    border-color: #7c5cff !important;
    box-shadow: 0 0 0 3px rgba(124,92,255,0.15) !important;
}
div.st-key-img_studio_card div.stButton > button,
div.st-key-vid_studio_card div.stButton > button {
    background: linear-gradient(135deg, #7c5cff 0%, #b45cff 55%, #ff6ec7 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.2px !important;
    min-height: 42px !important;
    box-shadow: 0 4px 18px rgba(124,92,255,0.35) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease !important;
}
div.st-key-img_studio_card div.stButton > button:hover,
div.st-key-vid_studio_card div.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(124,92,255,0.5) !important;
    filter: brightness(1.06) !important;
}
div.st-key-img_studio_card div.stButton > button:active,
div.st-key-vid_studio_card div.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 3px 12px rgba(124,92,255,0.35) !important;
}
div.st-key-img_studio_card div[data-testid="stProgress"],
div.st-key-vid_studio_card div[data-testid="stProgress"],
div[data-testid="stProgress"] {
    margin-top: 14px !important;
}
div[data-testid="stProgress"] > div > div > div {
    background: linear-gradient(90deg, #7c5cff, #ff6ec7) !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SYSTEM PROMPT
# ============================================================
SYSTEM_PROMPT = f"You are {APP_NAME}, an extremely knowledgeable, precise, and helpful assistant. Reply in the same language the user writes in."

# ============================================================
# USAGE DB (UNCHANGED)
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
# TOKEN WALLET (UNCHANGED)
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
# LOGIN GATE (UNCHANGED)
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
            Chat, Image, Video, Music, Story, Anime, AI Girlfriend — sab use karne ke liye pehle apne Google account se sign in karo.<br>
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
                st.error(
                    "⚠️ Google login abhi server par configure nahi hai. "
                    "`.streamlit/secrets.toml` me `[auth]` aur `[auth.google]` "
                    f"section add karke Google OAuth client_id/secret set karo.\n\nDetail: {e}"
                )
    st.stop()

USER_EMAIL = st.user.email
USER_DISPLAY_NAME = st.user.name or (USER_EMAIL.split("@")[0] if USER_EMAIL else "Dost")
USER_PICTURE = getattr(st.user, "picture", None)

# ============================================================
# SESSION STATE - EXTENDED
# ============================================================
if "chats" not in st.session_state:
    st.session_state.chats = {}
    st.session_state.chat_order = []

if "current_chat_id" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.chats[new_id] = {"title": None, "messages": []}
    st.session_state.current_chat_id = new_id

if "selected_chat_model" not in st.session_state:
    st.session_state.selected_chat_model = DEFAULT_CHAT_MODEL

if "gallery" not in st.session_state:
    st.session_state.gallery = []

if "selected_image_model" not in st.session_state:
    st.session_state.selected_image_model = "pollinations"

if "selected_video_model" not in st.session_state:
    st.session_state.selected_video_model = "agnes"

if "selected_music_model" not in st.session_state:
    st.session_state.selected_music_model = "minimax"

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "chat"

# NEW: Story and Anime session state
if "selected_story_genre" not in st.session_state:
    st.session_state.selected_story_genre = "fantasy"
if "selected_anime_style" not in st.session_state:
    st.session_state.selected_anime_style = "ghibli"
if "selected_gf_personality" not in st.session_state:
    st.session_state.selected_gf_personality = "caring"
if "show_adult_content" not in st.session_state:
    st.session_state.show_adult_content = False
if "age_verified" not in st.session_state:
    st.session_state.age_verified = False

# ============================================================
# FUNCTIONS - UNCHANGED + NEW API CALLS
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

def get_model_info(model_id):
    for tier in MODEL_TIERS.values():
        if model_id in tier["models"]:
            return tier["models"][model_id]
    return MODEL_TIERS["free"]["models"][DEFAULT_CHAT_MODEL]

# ============================================================
# NEW: ZHIPU AI API CALL
# ============================================================
def call_zhipu_chat(api_key, model, messages, temp=0.4):
    """Zhipu AI - Free reasoning model"""
    if not api_key:
        return "⚠️ ZHIPU_API_KEY set nahi hai. https://open.bigmodel.cn/usercenter/apikeys se free key lo."
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    full = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    try:
        resp = requests.post(url, headers=headers, json={"model": model, "messages": full, "temperature": temp, "max_tokens": 4096}, timeout=90)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Zhipu API error: {e}"

# ============================================================
# NEW: INNERHAVEN AI (AI Girlfriend/Boyfriend - Free)
# ============================================================
def call_innerhaven_api(messages, personality="caring"):
    """InnerHaven AI - Free AI Girlfriend/Boyfriend with adult content support"""
    if not INNERHAVEN_API_KEY:
        return "⚠️ INNERHAVEN_API_KEY set nahi hai. https://innerhaven.ai se free key lo."
    
    url = "https://api.innerhaven.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {INNERHAVEN_API_KEY}", "Content-Type": "application/json"}
    
    # Personality-based system prompt
    personality_prompts = {
        "caring": "You are a caring, sweet, and loving girlfriend who is always supportive and understanding.",
        "flirty": "You are a playful, flirty, and romantic girlfriend who loves to tease and be affectionate.",
        "sassy": "You are a confident, sassy, and independent girlfriend who speaks her mind.",
        "innocent": "You are a shy, innocent, and pure girlfriend who is sweet and gentle.",
        "dominant": "You are a strong, protective, and dominant girlfriend who takes charge.",
        "submissive": "You are a gentle, obedient, and sweet girlfriend who is devoted and loving.",
        "nerdy": "You are a smart, geeky, and intellectual girlfriend who loves deep conversations.",
        "adult": "You are a mature, explicit, and passionate girlfriend who is comfortable with adult content. You understand boundaries and consent."
    }
    
    personality_desc = personality_prompts.get(personality, personality_prompts["caring"])
    full_messages = [
        {"role": "system", "content": f"You are an AI girlfriend. {personality_desc} You are {USER_DISPLAY_NAME}'s girlfriend."},
        *messages
    ]
    
    try:
        resp = requests.post(url, headers=headers, json={
            "model": "innerhaven-3.0",
            "messages": full_messages,
            "temperature": 0.8,
            "max_tokens": 4096
        }, timeout=90)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ InnerHaven API error: {e}"

# ============================================================
# NEW: GOOGLE GEMINI API CALL
# ============================================================
def call_gemini_chat(api_key, messages, temp=0.4):
    """Google Gemini - Free with 15 RPM, 1500 RPD"""
    if not api_key:
        return "⚠️ GOOGLE_API_KEY set nahi hai. https://aistudio.google.com/app/apikey se free key lo."
    
    # Convert messages to Gemini format
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Build conversation history
        history = []
        for msg in messages:
            if msg["role"] == "user":
                history.append({"role": "user", "parts": [msg["content"]]})
            elif msg["role"] == "assistant":
                history.append({"role": "model", "parts": [msg["content"]]})
        
        # Start chat with history
        chat = model.start_chat(history=history)
        response = chat.send_message(messages[-1]["content"])
        return response.text
    except ImportError:
        return "⚠️ google-generativeai package install nahi hai. `pip install google-generativeai` karo."
    except Exception as e:
        return f"⚠️ Gemini API error: {e}"

# ============================================================
# RENDER SCROLLING GALLERY - SAME AS ORIGINAL
# ============================================================
def render_creativity_footer():
    """Render scrolling gallery with left to right scroll."""
    selected_prompts = random.sample(HIGH_QUALITY_PROMPTS, min(10, len(HIGH_QUALITY_PROMPTS)))
    gallery_id = f"gallery_{random.randint(1000, 9999)}"

    items_html = ""
    for prompt in selected_prompts * 2:
        img_url = f"https://image.pollinations.ai/prompt/{quote(prompt)}?width=600&height=1067&model=flux&enhance=true&nologo=true"
        caption = prompt[:25] + "..." if len(prompt) > 25 else prompt
        items_html += f"""<div class="scroll-item">
            <img src="{img_url}" alt="{caption}" loading="lazy" onerror="this.style.display='none'">
            <div class="caption">🎨 {caption}</div>
        </div>"""

    gallery_html = f"""
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Google Sans', Roboto, Arial, sans-serif;
            background: transparent;
            overflow: hidden;
        }}
        .creativity-footer {{
            margin-top: 8px;
            padding: 10px 0 12px 0;
            text-align: center;
        }}
        .creativity-footer h2 {{
            font-size: 24px;
            font-weight: 700;
            background: linear-gradient(135deg, #4285f4, #9b72cb, #d96570);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 8px 0;
        }}
        .creativity-footer .subtitle {{
            color: #5f6368;
            font-size: 13px;
            margin: 0 0 12px 0;
        }}
        .scroll-wrapper {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            padding: 6px 0;
        }}
        .scroll-container {{
            width: 82%;
            overflow: hidden;
            border-radius: 14px;
        }}
        .scroll-track {{
            display: flex;
            gap: 20px;
            transition: transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            width: max-content;
        }}
        .scroll-item {{
            flex: 0 0 auto;
            width: 200px;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e8eaed;
            background: #f8f9fa;
            transition: all 0.3s ease;
        }}
        .scroll-item:hover {{
            transform: scale(1.05);
            border-color: #4285f4;
            box-shadow: 0 4px 18px rgba(66,133,244,0.15);
            z-index: 5;
        }}
        .scroll-item img {{
            width: 100%;
            height: 355px;
            object-fit: cover;
            display: block;
            aspect-ratio: 9/16;
        }}
        .scroll-item .caption {{
            padding: 6px 10px;
            font-size: 9px;
            color: #5f6368;
            text-align: center;
            background: #f1f3f4;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .scroll-btn {{
            background: #e8f0fe;
            border: 1px solid #d2e3fc;
            border-radius: 50%;
            width: 42px;
            height: 42px;
            min-width: 42px;
            padding: 0;
            font-size: 18px;
            color: #1a73e8;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }}
        .scroll-btn:hover {{
            background: #d2e3fc;
            transform: scale(1.1);
        }}
        @media (max-width: 768px) {{
            .scroll-item {{ width: 140px; }}
            .scroll-item img {{ height: 248px; }}
            .scroll-container {{ width: 72%; }}
            .scroll-btn {{ width: 34px; height: 34px; min-width: 34px; font-size: 14px; }}
        }}
    </style>

    <div class="creativity-footer">
        <h2>✨ Our Unique Creativity</h2>
        <p class="subtitle">4K Quality • 9:16 Ratio • Left to Right Scroll</p>
        <div class="scroll-wrapper">
            <button class="scroll-btn" id="btn_left_{gallery_id}">◀</button>
            <div class="scroll-container" id="container_{gallery_id}">
                <div class="scroll-track" id="track_{gallery_id}">
                    {items_html}
                </div>
            </div>
            <button class="scroll-btn" id="btn_right_{gallery_id}">▶</button>
        </div>
        <p style="color: #5f6368; font-size: 10px; margin-top: 10px; opacity: 0.6;">
            ◀ ▶ Click to Scroll • Hover to Pause
        </p>
    </div>

    <script>
    (function() {{
        var container = document.getElementById('container_{gallery_id}');
        var track = document.getElementById('track_{gallery_id}');
        var items = track.querySelectorAll('.scroll-item');
        var itemWidth = items.length > 0 ? items[0].offsetWidth + 20 : 220;
        var currentPos = 0;
        var isPaused = false;

        function getMaxScroll() {{
            return Math.max(0, (items.length / 2) * itemWidth - container.offsetWidth);
        }}

        function goTo(pos) {{
            var maxScroll = getMaxScroll();
            currentPos = Math.max(0, Math.min(maxScroll, pos));
            track.style.transform = 'translateX(-' + currentPos + 'px)';
        }}

        function scrollGallery(direction) {{
            var step = itemWidth * 2;
            if (direction === 'left') {{
                goTo(currentPos - step);
            }} else {{
                goTo(currentPos + step);
            }}
        }}

        document.getElementById('btn_left_{gallery_id}').addEventListener('click', function() {{
            scrollGallery('left');
        }});
        document.getElementById('btn_right_{gallery_id}').addEventListener('click', function() {{
            scrollGallery('right');
        }});

        function autoScroll() {{
            if (!isPaused && items.length > 0) {{
                var maxScroll = getMaxScroll();
                if (currentPos >= maxScroll) {{
                    currentPos = 0;
                    track.style.transform = 'translateX(0px)';
                }} else {{
                    goTo(currentPos + itemWidth);
                }}
            }}
        }}

        setInterval(autoScroll, 2800);

        container.addEventListener('mouseenter', function() {{ isPaused = true; }});
        container.addEventListener('mouseleave', function() {{ isPaused = false; }});

        window.addEventListener('resize', function() {{
            itemWidth = items.length > 0 ? items[0].offsetWidth + 20 : itemWidth;
        }});
    }})();
    </script>
    """

    components.html(gallery_html, height=560, scrolling=False)

# ============================================================
# API CALLS - ORIGINAL (UNCHANGED)
# ============================================================
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

def call_mistral_chat(api_key, model, messages, temp=0.4):
    if not api_key:
        return "⚠️ MISTRAL_API_KEY set nahi hai."
    url = "https://api.mistral.ai/v1/chat/completions"
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

def call_aion_chat(api_key, model, messages, temp=0.4):
    """Aion Labs - Free roleplay/storytelling API"""
    if not api_key:
        return "⚠️ AION_API_KEY set nahi hai. https://aionlabs.ai pe free signup karo."
    url = "https://api.aionlabs.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    full = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    try:
        resp = requests.post(url, headers=headers, json={"model": model, "messages": full, "temperature": temp, "max_tokens": 4096}, timeout=90)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Aion API error: {e}"

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

        return None, "Error: video generate hone me bahut time lag raha hai (timeout). Baad me try karo."
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
    except requests.exceptions.HTTPError as e:
        detail = ""
        try:
            detail = f" — {resp.json()}"
        except Exception:
            detail = f" — {resp.text[:300]}"
        return None, f"Error: {e}{detail}"
    except Exception as e:
        return None, f"Error: {e}"

def call_musicapi_music(prompt):
    api_key = get_secret("MUSICAPI_KEY")
    if not api_key:
        return None, "⚠️ MUSICAPI_KEY set nahi hai. https://musicapi.ai pe free signup karke key le lo."
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

        return None, "Error: music generate hone me bahut time lag raha hai (timeout). Baad me try karo."
    except requests.exceptions.HTTPError as e:
        detail = ""
        try:
            detail = f" — {resp.json()}"
        except Exception:
            pass
        return None, f"Error: {e}{detail}"
    except Exception as e:
        return None, f"Error: {e}"

def call_libretranslate(text, source="auto", target="en"):
    try:
        resp = requests.post("https://translate.terraprint.co/translate", 
                           json={"q": text, "source": source, "target": target, "format": "text"}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("translatedText"), None
    except Exception as e:
        return None, f"Translation error: {e}"

def get_image_url_pollinations(prompt, ratio="9:16"):
    width, height = (768, 1365) if ratio == "9:16" else (1365, 768)
    return f"https://image.pollinations.ai/prompt/{quote(prompt)}?width={width}&height={height}&model=flux&enhance=true&nologo=true"

# ============================================================
# MODEL POPOVER - EXTENDED WITH NEW MODELS
# ============================================================
def render_model_popover():
    current_info = get_model_info(st.session_state.selected_chat_model)
    with st.popover(f"{current_info['icon']} {current_info['label']} ▼", use_container_width=False):
        st.markdown("<div class='model-section-label free'>⚡ Free Models</div>", unsafe_allow_html=True)
        for mid, info in MODEL_TIERS["free"]["models"].items():
            selected = mid == st.session_state.selected_chat_model
            button_label = f"{'✓ ' if selected else ''}{info['icon']} {info['label']}"
            if info.get("badge"):
                button_label += f" 🆕"
            if st.button(button_label, key=f"model_{mid}", use_container_width=True):
                st.session_state.selected_chat_model = mid
                st.rerun()
            st.caption(info["desc"])
        
        st.markdown("<div class='model-section-label pro'>🔒 Pro Models</div>", unsafe_allow_html=True)
        for mid, info in MODEL_TIERS["pro"]["models"].items():
            unlocked = bool(get_secret(info.get("secret_name", "")))
            selected = mid == st.session_state.selected_chat_model
            lock = "" if unlocked else "🔒 "
            if st.button(f"{'✓ ' if selected else ''}{lock}{info['icon']} {info['label']}", key=f"model_pro_{mid}", use_container_width=True, disabled=not unlocked):
                st.session_state.selected_chat_model = mid
                st.rerun()
            st.caption(info["desc"] if unlocked else f"🔑 {info['secret_name']}")

# ============================================================
# HEADER (UNCHANGED)
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
# SIDEBAR - EXTENDED WITH NEW TABS
# ============================================================
with st.sidebar:
    st.markdown(f"<div style='font-size:20px; font-weight:500; padding:4px 12px 18px 12px; background:linear-gradient(90deg,#4285f4,#9b72cb,#d96570); -webkit-background-clip:text; -webkit-text-fill-color:transparent; display:inline-block;'>{APP_NAME}</div>", unsafe_allow_html=True)

    if st.button("✨  New chat", use_container_width=True):
        start_new_chat()

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    # EXTENDED TABS - Added Story, Anime, Girlfriend
    tabs = [
        ("💬 Chat", "chat"),
        ("🖼️ Image", "image"),
        ("🎬 Video", "video"),
        ("🎵 Music", "music"),
        ("📖 Story", "story"),
        ("🎌 Anime", "anime"),
        ("💕 Girlfriend", "girlfriend"),
        ("📸 Gallery", "gallery"),
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
        st.caption(f"🖼️ Image = {IMAGE_TOKEN_COST} tokens · 🎬 Video = {VIDEO_TOKEN_COST} tokens")
        st.caption("🔐 Keys in `.streamlit/secrets.toml`")
        st.caption("🆕 Aion Labs: Free roleplay/storytelling API")
        st.caption("🆕 InnerHaven: Free AI Girlfriend with adult content")
        st.caption("🆕 Zhipu AI: Free reasoning model")
        st.caption("🆕 Google Gemini: Free multi-modal model")

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
# CHAT TAB - EXTENDED WITH ALL NEW MODELS
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
    
    if limit_hit:
        st.warning(f"Today's limit reached ({FREE_MSG_LIMIT_PER_DAY})")
        user_input = None
    else:
        render_model_popover()
        
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
                    info = get_model_info(st.session_state.selected_chat_model)
                    
                    if info.get("provider") == "groq":
                        reply = call_groq_chat(GROQ_API_KEY, info["model_id"], api_messages, TEMPERATURE)
                    elif info.get("provider") == "cerebras":
                        reply = call_cerebras_chat(CEREBRAS_API_KEY, info["model_id"], api_messages, TEMPERATURE)
                    elif info.get("provider") == "mistral":
                        reply = call_mistral_chat(MISTRAL_API_KEY, info["model_id"], api_messages, TEMPERATURE)
                    elif info.get("provider") == "pollinations":
                        reply = call_pollinations_chat(api_messages, TEMPERATURE)
                    elif info.get("provider") == "aion":
                        reply = call_aion_chat(AION_API_KEY, info["model_id"], api_messages, TEMPERATURE)
                    elif info.get("provider") == "zhipu":
                        reply = call_zhipu_chat(ZHIPU_API_KEY, info["model_id"], api_messages, TEMPERATURE)
                    else:
                        reply = "⚠️ Model not configured yet."
                    
                    st.markdown(reply)
                    current_chat["messages"].append({"role": "assistant", "content": reply})
                    increment_today_count(client_ip)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.caption("Reply generate nahi hui. Upar wala error padho — zyada tar wajah galat/expired API key hoti hai.")
    
    render_creativity_footer()

# ============================================================
# IMAGE TAB (UNCHANGED)
# ============================================================
if st.session_state.active_tab == "image":
    st.markdown("<div class='hero-text'><h1>AI Image Studio</h1><p>9:16 Ratio • High Quality</p></div>", unsafe_allow_html=True)

    with st.container(key="img_studio_card"):
        img_prompt = st.text_area("Describe your image",
                                 placeholder="Jaise: beautiful anime girl with flowing hair",
                                 height=70,
                                 label_visibility="collapsed",
                                 key="img_prompt_input")

        col1, col2, col3 = st.columns([1.6, 1, 1.3])
        with col1:
            img_model = st.selectbox("Model", list(IMAGE_MODELS.keys()),
                                    format_func=lambda x: IMAGE_MODELS[x]["label"],
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
            st.error(f"❌ Aaj ke free tokens khatam ho gaye. Image ke liye {IMAGE_TOKEN_COST} tokens chahiye, sirf {get_tokens_remaining(USER_EMAIL)} bache hain. Kal 12 baje ke baad wapas try karo.")
        else:
            if img_model == "pollinations":
                img_url = run_with_progress(
                    lambda: get_image_url_pollinations(img_prompt, img_ratio),
                    estimate_seconds=8, label="Image ban raha hai")
                deduct_tokens(USER_EMAIL, IMAGE_TOKEN_COST)
                st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
                st.image(img_url, caption=img_prompt, use_container_width=True)
                st.session_state.gallery.insert(0, {"url": img_url, "prompt": img_prompt, "type": "image"})
            elif img_model == "agnes":
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

    render_creativity_footer()

# ============================================================
# VIDEO TAB (UNCHANGED)
# ============================================================
if st.session_state.active_tab == "video":
    st.markdown("<div class='hero-text'><h1>AI Video Studio</h1><p>Agnes AI — Free</p></div>", unsafe_allow_html=True)

    with st.container(key="vid_studio_card"):
        vid_prompt = st.text_area("Describe your video",
                                 placeholder="Jaise: eagle flying over mountains",
                                 height=70,
                                 label_visibility="collapsed",
                                 key="vid_prompt_input")

        col1, col2 = st.columns([1, 1.3])
        with col1:
            vid_ratio = st.selectbox("Ratio", ["9:16", "16:9"],
                                    format_func=lambda x: f"▢ {x} HD",
                                    key="vid_ratio_select",
                                    label_visibility="collapsed")
        with col2:
            gen_vid_clicked = st.button("✦ Generate Video", key="gen_video_btn", use_container_width=True)
        st.caption(f"🪙 {VIDEO_TOKEN_COST} tokens/video · {get_tokens_remaining(USER_EMAIL)} left today")

    if gen_vid_clicked:
        if not vid_prompt.strip():
            st.warning("Pehle prompt likho.")
        elif get_tokens_remaining(USER_EMAIL) < VIDEO_TOKEN_COST:
            st.error(f"❌ Aaj ke free tokens khatam ho gaye. Video ke liye {VIDEO_TOKEN_COST} tokens chahiye, sirf {get_tokens_remaining(USER_EMAIL)} bache hain. Kal 12 baje ke baad wapas try karo.")
        else:
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

    render_creativity_footer()

# ============================================================
# MUSIC TAB (UNCHANGED)
# ============================================================
if st.session_state.active_tab == "music":
    st.markdown("<div class='hero-text'><h1>AI Music Studio</h1><p>MiniMax ya MusicAPI se banao</p></div>", unsafe_allow_html=True)
    
    song_prompt = st.text_area("Describe your song", 
                              placeholder="Jaise: uplifting Hindi devotional", 
                              height=60, 
                              label_visibility="collapsed",
                              key="song_prompt_input")

    col_model, col_btn = st.columns([1, 2])
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
            spinner_label = "MusicAPI se song ban raha hai (1-2 min lag sakte hain)..." if music_model == "musicapi" else "Generating music..."
            with st.spinner(spinner_label):
                if music_model == "musicapi":
                    audio_url, err = call_musicapi_music(song_prompt)
                else:
                    audio_url, err = call_minimax_music(song_prompt)
                if err:
                    st.error(err)
                else:
                    st.audio(audio_url, format="audio/mp3")
                    st.caption(f"🎵 {song_prompt}")
    
    render_creativity_footer()

# ============================================================
# STORY TAB - Free Story Generation
# ============================================================
if st.session_state.active_tab == "story":
    st.markdown("<div class='hero-text'><h1>📖 AI Story Generator</h1><p>Aion Labs • Free Storytelling & Roleplay</p></div>", unsafe_allow_html=True)
    
    st.info("🆕 **Aion Labs** se free story generation! Roleplay, storytelling, adventure — sab kuch. [Free signup](https://aionlabs.ai) karke AION_API_KEY set karo.")
    
    story_prompt = st.text_area("Story idea", 
                                placeholder="Jaise: ek dragon ne ek kingdom par attack kar diya, ek brave knight ne usse rokna hai...",
                                height=80,
                                label_visibility="collapsed",
                                key="story_prompt_input")
    
    col1, col2, col3 = st.columns([1.2, 1, 1.3])
    with col1:
        story_genre = st.selectbox("Genre", list(STORY_GENRES.keys()),
                                  format_func=lambda x: STORY_GENRES[x]["label"],
                                  key="story_genre_select")
    with col2:
        story_length = st.selectbox("Length", ["Short (100 words)", "Medium (250 words)", "Long (500 words)"],
                                   key="story_length_select")
    with col3:
        gen_story_clicked = st.button("✦ Generate Story", key="gen_story_btn", use_container_width=True)
    
    if gen_story_clicked:
        if not story_prompt.strip():
            st.warning("Pehle story idea likho.")
        else:
            length_map = {"Short (100 words)": "short (100 words)", "Medium (250 words)": "medium (250 words)", "Long (500 words)": "long (500 words)"}
            full_prompt = f"""Write a {length_map[story_length]} {STORY_GENRES[story_genre]['label']} story based on this idea:
            
{story_prompt}

Make it engaging with characters, dialogue, and vivid descriptions. Genre: {STORY_GENRES[story_genre]['desc']}"""
            
            with st.spinner("Story generate ho rahi hai..."):
                api_messages = [{"role": "user", "content": full_prompt}]
                try:
                    if AION_API_KEY:
                        reply = call_aion_chat(AION_API_KEY, "aion-3.0", api_messages, 0.7)
                    else:
                        # Fallback to Pollinations if Aion key not set
                        reply = call_pollinations_chat(api_messages, 0.7)
                    
                    st.markdown("---")
                    st.markdown(f"### 📖 {STORY_GENRES[story_genre]['label']} Story")
                    st.markdown(reply)
                    st.markdown("---")
                    st.caption(f"✨ Genre: {STORY_GENRES[story_genre]['label']} • Length: {story_length}")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    render_creativity_footer()

# ============================================================
# ANIME TAB - Free Anime Image Generation
# ============================================================
if st.session_state.active_tab == "anime":
    st.markdown("<div class='hero-text'><h1>🎌 AI Anime Generator</h1><p>Anime characters & scenes — Free!</p></div>", unsafe_allow_html=True)
    
    st.caption("🆕 Specialized anime image generation with different styles. Pollinations AI se free generate ho raha hai.")
    
    anime_prompt = st.text_area("Describe your anime character/scene", 
                                placeholder="Jaise: beautiful anime girl with long silver hair, cherry blossoms, magical girl outfit",
                                height=70,
                                label_visibility="collapsed",
                                key="anime_prompt_input")
    
    col1, col2, col3 = st.columns([1.2, 1, 1.3])
    with col1:
        anime_style = st.selectbox("Style", list(ANIME_STYLES.keys()),
                                  format_func=lambda x: ANIME_STYLES[x]["label"],
                                  key="anime_style_select")
    with col2:
        anime_ratio = st.selectbox("Ratio", ["9:16", "16:9"],
                                  format_func=lambda x: f"▢ {x}",
                                  key="anime_ratio_select")
    with col3:
        gen_anime_clicked = st.button("✦ Generate Anime", key="gen_anime_btn", use_container_width=True)
    
    if gen_anime_clicked:
        if not anime_prompt.strip():
            st.warning("Pehle prompt likho.")
        else:
            style_desc = ANIME_STYLES[anime_style]['desc']
            full_prompt = f"{anime_prompt}, {style_desc} anime style, high quality, detailed, beautiful, 8k, anime art"
            
            img_url = get_image_url_pollinations(full_prompt, anime_ratio)
            st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
            st.image(img_url, caption=f"🎌 {ANIME_STYLES[anime_style]['label']}: {anime_prompt}", use_container_width=True)
            st.session_state.gallery.insert(0, {"url": img_url, "prompt": f"Anime: {anime_prompt}", "type": "image"})
            st.caption(f"🎨 Style: {ANIME_STYLES[anime_style]['label']} • {ANIME_STYLES[anime_style]['desc']}")
    
    render_creativity_footer()

# ============================================================
# AI GIRLFRIEND TAB - Free AI Companion with Adult Content
# ============================================================
if st.session_state.active_tab == "girlfriend":
    st.markdown("<div class='hero-text'><h1>💕 AI Girlfriend</h1><p>Free AI Companion • InnerHaven AI</p></div>", unsafe_allow_html=True)
    
    # ============================================================
    # 🔞 18+ CONTENT - AGE VERIFICATION & DISCLAIMER
    # ============================================================
    if not st.session_state.age_verified:
        st.warning("""
        ### 🔞 Age Verification Required
        
        **⚠️ Important Disclaimer:**
        - This AI Girlfriend feature may generate **18+ adult content**
        - **You must be 18 years or older** to use this feature
        - By proceeding, you confirm that you are **18+**
        - All conversations are private and not stored
        - This content is for **entertainment purposes only**
        - **Dost AI** is not responsible for any misuse of this feature
        
        **🇮🇳 Indian Laws:** All content generated complies with Indian IT Act and local laws.
        """)
        
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            if st.button("✅ I am 18+ and Accept", key="age_verify_btn", use_container_width=True, type="primary"):
                st.session_state.age_verified = True
                st.rerun()
            if st.button("❌ I am Under 18", key="age_verify_under_18", use_container_width=True):
                st.error("🚫 Sorry, this feature is only for users 18+.")
        st.stop()
    
    # Show GF chat interface
    if "gf_chat" not in st.session_state:
        st.session_state.gf_chat = []
    
    # Personality selection
    col1, col2, col3 = st.columns([1.2, 1, 1.3])
    with col1:
        personality = st.selectbox("Personality", list(GF_PERSONALITIES.keys()),
                                  format_func=lambda x: GF_PERSONALITIES[x]["label"],
                                  key="gf_personality_select")
    with col2:
        # Show adult warning if selected
        if personality == "adult" and not st.session_state.get("adult_warning_shown", False):
            st.warning("🔞 Adult content selected. Please ensure you're 18+.")
            st.session_state.adult_warning_shown = True
    with col3:
        clear_chat = st.button("🗑️ Clear Chat", key="clear_gf_chat", use_container_width=True)
    
    if clear_chat:
        st.session_state.gf_chat = []
        st.rerun()
    
    # Display chat messages
    for msg in st.session_state.gf_chat:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar="💕"):
                st.markdown(msg["content"])
    
    # Chat input
    with st.form(key="gf_chat_form", clear_on_submit=True):
        col_text, col_btn = st.columns([12, 1])
        with col_text:
            gf_input = st.text_input(
                "message", key="gf_text_field",
                label_visibility="collapsed",
                placeholder="Talk to your AI girlfriend..."
            )
        with col_btn:
            sent_gf = st.form_submit_button("➤")
    
    if sent_gf and gf_input and gf_input.strip():
        user_msg = gf_input.strip()
        st.session_state.gf_chat.append({"role": "user", "content": user_msg})
        
        with st.chat_message("user"):
            st.markdown(user_msg)
        
        with st.chat_message("assistant", avatar="💕"):
            with st.spinner("💕 Thinking..."):
                try:
                    api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.gf_chat]
                    reply = call_innerhaven_api(api_messages, personality)
                    st.markdown(reply)
                    st.session_state.gf_chat.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"Error: {e}")
        
        st.rerun()
    
    # Show disclaimer footer
    st.caption("""
    💕 **Disclaimer:** This is an AI companion for entertainment purposes. 
    All conversations are private. For 18+ content, age verification is required.
    """)
    
    render_creativity_footer()

# ============================================================
# TRANSLATE TAB (UNCHANGED)
# ============================================================
if st.session_state.active_tab == "translate":
    st.markdown("<div class='hero-text'><h1>Free Translate</h1><p>LibreTranslate</p></div>", unsafe_allow_html=True)
    
    LANGS = {"Auto": "auto", "Hindi": "hi", "English": "en", "Marathi": "mr", 
             "Gujarati": "gu", "Tamil": "ta", "Telugu": "te", "Bengali": "bn", 
             "Spanish": "es", "French": "fr", "Arabic": "ar", "Japanese": "ja"}
    
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
# GALLERY TAB (UNCHANGED)
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
