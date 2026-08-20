"""
🧡 Dost AI — ULTIMATE FREE AI MODELS
Duniya bhar ke 30+ free AI models ek jagah
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
import json
import random
from datetime import date
from urllib.parse import quote
import streamlit.components.v1 as components
from huggingface_hub import InferenceClient

# ============================================================
# 🔐 SECURE SECRETS
# ============================================================
def get_secret(name):
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
HF_API_KEY = get_secret("HF_API_KEY")
AGNES_API_KEY = get_secret("AGNES_API_KEY")
MUSICAPI_KEY = get_secret("MUSICAPI_KEY")
REPLICATE_API_KEY = get_secret("REPLICATE_API_KEY")
TOGETHER_API_KEY = get_secret("TOGETHER_API_KEY")

# ============================================================
# CONFIG
# ============================================================
APP_NAME = "Dost AI"
TEMPERATURE = 0.4
FREE_MSG_LIMIT_PER_DAY = 40
TOKEN_LIMIT_PER_DAY = 1000
IMAGE_TOKEN_COST = 20
VIDEO_TOKEN_COST = 100
MUSIC_TOKEN_COST = 30

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
# 🎨 COMPLETE FREE MODELS - 30+ MODELS
# ============================================================

# --- 15 IMAGE MODELS ---
IMAGE_MODELS = {
    # POLLINATIONS - No key needed
    "pollinations": {"label": "Pollinations AI", "icon": "🖼️", "provider": "pollinations"},
    
    # AGNES - Free API
    "agnes": {"label": "Agnes Image", "icon": "🤖", "provider": "agnes"},
    
    # HUGGING FACE FLUX MODELS
    "flux_schnell": {"label": "FLUX.1-schnell", "icon": "⚡", "provider": "huggingface", "model": "black-forest-labs/FLUX.1-schnell"},
    "flux_dev": {"label": "FLUX.1-dev", "icon": "🎨", "provider": "huggingface", "model": "black-forest-labs/FLUX.1-dev"},
    
    # STABLE DIFFUSION MODELS
    "sdxl": {"label": "SDXL", "icon": "🌈", "provider": "huggingface", "model": "stabilityai/stable-diffusion-xl-base-1.0"},
    "sd35": {"label": "SD 3.5", "icon": "✨", "provider": "huggingface", "model": "stabilityai/stable-diffusion-3.5-large"},
    "playground": {"label": "Playground v2.5", "icon": "📸", "provider": "huggingface", "model": "playgroundai/playground-v2.5-1024px-aesthetic"},
    "dreamshaper": {"label": "DreamShaper", "icon": "🌟", "provider": "huggingface", "model": "Lykon/dreamshaper-8"},
    "realistic": {"label": "Realistic Vision", "icon": "👤", "provider": "huggingface", "model": "SG161222/Realistic_Vision_V4.0"},
    "openjourney": {"label": "OpenJourney", "icon": "🎨", "provider": "huggingface", "model": "prompthero/openjourney-v4"},
    
    # NEW FREE MODELS
    "kandinsky": {"label": "Kandinsky 2.2", "icon": "🎭", "provider": "huggingface", "model": "kandinsky-community/kandinsky-2-2-decoder"},
    "wuerstchen": {"label": "Wuerstchen", "icon": "🐇", "provider": "huggingface", "model": "warp-ai/wuerstchen"},
    "hunyuandit": {"label": "Hunyuan DiT", "icon": "🐉", "provider": "huggingface", "model": "Tencent-Hunyuan/Hunyuan-DiT"},
}

# --- 8 VIDEO MODELS ---
VIDEO_MODELS = {
    # AGNES - Free
    "agnes": {"label": "Agnes Video", "icon": "🎬", "provider": "agnes"},
    
    # HUGGING FACE VIDEO MODELS
    "cogvideox": {"label": "CogVideoX", "icon": "🎥", "provider": "huggingface_video", "model": "THUDM/CogVideoX-5b"},
    "modelscope": {"label": "ModelScope", "icon": "🏔️", "provider": "huggingface_video", "model": "damo/ModelScope"},
    "svd": {"label": "Stable Video Diffusion", "icon": "📹", "provider": "huggingface_video", "model": "stabilityai/stable-video-diffusion-img2vid"},
    "pyramid": {"label": "Pyramid Flow", "icon": "🔺", "provider": "huggingface_video", "model": "PYRAMID-FLOW/pyramid-flow"},
    "mochi": {"label": "Mochi-1", "icon": "🌀", "provider": "huggingface_video", "model": "genmo/mochi-1"},
    
    # NEW FREE VIDEO MODELS
    "wan": {"label": "Wan 2.2", "icon": "🌊", "provider": "huggingface_video", "model": "Wan-AI/Wan2.2-T2V-A14B"},
    "opensora": {"label": "Open-Sora 2.0", "icon": "🎞️", "provider": "huggingface_video", "model": "HPC-AI/Open-Sora"},
}

# --- 4 MUSIC MODELS ---
MUSIC_MODELS = {
    "musicgen": {"label": "MusicGen", "icon": "🎵", "provider": "huggingface_music", "model": "facebook/musicgen-large"},
    "audiocraft": {"label": "AudioCraft", "icon": "🎶", "provider": "huggingface_music", "model": "facebook/audiocraft"},
    "musicapi": {"label": "MusicAPI Sonic", "icon": "🎼", "provider": "musicapi"},
    "minimax": {"label": "MiniMax Music", "icon": "🎵", "provider": "minimax"},
}

# --- 10 CHAT MODELS ---
CHAT_MODELS = {
    # GROQ MODELS
    "groq_llama_8b": {"label": "Llama 3 8B", "icon": "⚡", "provider": "groq", "model_id": "llama3-8b-8192"},
    "groq_llama_70b": {"label": "Llama 3 70B", "icon": "💪", "provider": "groq", "model_id": "llama3-70b-8192"},
    "groq_mixtral": {"label": "Mixtral 8x7B", "icon": "🌪️", "provider": "groq", "model_id": "mixtral-8x7b-32768"},
    "groq_gemma": {"label": "Gemma 2 9B", "icon": "✨", "provider": "groq", "model_id": "gemma2-9b-it"},
    
    # POLLINATIONS
    "pollinations": {"label": "Pollinations Chat", "icon": "🌐", "provider": "pollinations"},
    
    # TOGETHER AI (Free tier)
    "together": {"label": "Together AI", "icon": "🤝", "provider": "together", "model_id": "meta-llama/Llama-3.3-70B-Instruct-Turbo"},
    
    # HUGGING FACE CHAT
    "hf_deepseek": {"label": "DeepSeek V3", "icon": "💎", "provider": "huggingface_chat", "model_id": "deepseek-ai/DeepSeek-V3"},
    "hf_qwen": {"label": "Qwen 2.5", "icon": "🐉", "provider": "huggingface_chat", "model_id": "Qwen/Qwen2.5-72B-Instruct"},
    "hf_phi": {"label": "Phi-3.5", "icon": "📚", "provider": "huggingface_chat", "model_id": "microsoft/Phi-3.5-mini-instruct"},
    "hf_llama": {"label": "Llama 3.2 3B", "icon": "🦙", "provider": "huggingface_chat", "model_id": "meta-llama/Llama-3.2-3B-Instruct"},
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

# ============================================================
# 🎨 CSS STYLING
# ============================================================
st.markdown("""
<style>
* { margin: 0; padding: 0; }
body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3d 100%); color: #fff; }

.main { background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3d 100%); padding: 1rem; }
.stApp { background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3d 100%); }

.stContainer { background: rgba(255,255,255,0.05); border-radius: 12px; padding: 2rem; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }
.stTextArea { background: rgba(255,255,255,0.08) !important; border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 8px !important; color: #fff !important; }
.stSelectbox { background: rgba(255,255,255,0.08) !important; }
.stSelectbox div { background: rgba(255,255,255,0.08) !important; border: 1px solid rgba(255,255,255,0.2) !important; border-radius: 6px !important; }
.stButton button { background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important; border: none !important; border-radius: 8px !important; color: white !important; font-weight: 600 !important; padding: 0.6rem 1.5rem !important; transition: all 0.3s ease !important; }
.stButton button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4) !important; }

.hero-text { text-align: center; margin: 2rem 0; }
.hero-text h1 { font-size: 2.5rem; background: linear-gradient(135deg, #6366f1, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 800 !important; }
.hero-text p { font-size: 1.1rem; color: #a0aec0; margin-top: 0.5rem; }

.gallery-item { border-radius: 12px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); transition: transform 0.3s ease, box-shadow 0.3s ease; }
.gallery-item:hover { transform: translateY(-8px); box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3); }

.footer { text-align: center; margin-top: 3rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.1); color: #a0aec0; font-size: 0.9rem; }
.footer a { color: #6366f1; text-decoration: none; transition: color 0.3s; }
.footer a:hover { color: #8b5cf6; }

/* FIX SELECTBOX DROPDOWN WIDTH */
.stSelectbox { width: 100% !important; }
.stSelectbox > div { width: 100% !important; }

/* FIX BUTTON ALIGNMENT */
.stButton { width: 100% !important; }
.stButton > button { width: 100% !important; }

/* PROPER COLUMN SPACING */
[data-testid="column"] { padding: 0.5rem !important; }

/* CAPTION STYLING */
.stCaption { color: #a0aec0 !important; font-size: 0.85rem !important; text-align: center !important; }

/* PREVENT OVERFLOW */
.stContainer { overflow: visible !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "chat"
if "gallery" not in st.session_state:
    st.session_state.gallery = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "user_email" not in st.session_state:
    st.session_state.user_email = f"user_{st.session_state.session_id[:8]}@dost.ai"

USER_EMAIL = st.session_state.user_email

# ============================================================
# DUMMY FUNCTIONS (Keep existing implementations)
# ============================================================

def get_tokens_remaining(email):
    return TOKEN_LIMIT_PER_DAY

def deduct_tokens(email, amount):
    pass

def run_with_progress(func, estimate_seconds=5, label="Processing"):
    return func()

def call_groq_chat(msg, model_id):
    return "Response from Groq"

def get_image_url_pollinations(prompt, ratio):
    return "https://via.placeholder.com/400x600"

def call_agnes_image(prompt, ratio):
    return "https://via.placeholder.com/400x600", None

def call_huggingface_image(prompt, model_id, ratio):
    return b"fake_image_bytes", None

def call_agnes_video(prompt, ratio):
    return "https://via.placeholder.com/video.mp4", None

def call_huggingface_video(prompt, model_id, ratio):
    return "https://via.placeholder.com/video.mp4", None

def call_huggingface_music(prompt, model_id):
    return b"fake_audio", None

def call_musicapi_music(prompt):
    return "https://via.placeholder.com/audio.mp3", None

def call_minimax_music(prompt):
    return "https://via.placeholder.com/audio.mp3", None

def call_libretranslate(text, src, tgt):
    return f"Translated: {text}", None

def render_creativity_footer():
    st.markdown("""<div class='footer'>
    <p>🎨 Made with ❤️ by Dost AI • Donate to support free AI</p>
    </div>""", unsafe_allow_html=True)

# ============================================================
# MAIN NAVIGATION
# ============================================================
st.markdown("<div class='stContainer'>", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown(f"<div style='text-align:center; margin: 1rem 0;'><img src='{DOST_LOGO_AVATAR}' width='60'></div>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center;'>{APP_NAME}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Tab Buttons
    cols = st.columns(2)
    with cols[0]:
        if st.button("💬 Chat", use_container_width=True, key="tab_chat"):
            st.session_state.active_tab = "chat"
    with cols[1]:
        if st.button("🖼️ Image", use_container_width=True, key="tab_image"):
            st.session_state.active_tab = "image"
    
    cols = st.columns(2)
    with cols[0]:
        if st.button("🎬 Video", use_container_width=True, key="tab_video"):
            st.session_state.active_tab = "video"
    with cols[1]:
        if st.button("🎵 Music", use_container_width=True, key="tab_music"):
            st.session_state.active_tab = "music"
    
    cols = st.columns(2)
    with cols[0]:
        if st.button("🌐 Translate", use_container_width=True, key="tab_translate"):
            st.session_state.active_tab = "translate"
    with cols[1]:
        if st.button("📸 Gallery", use_container_width=True, key="tab_gallery"):
            st.session_state.active_tab = "gallery"
    
    st.markdown("---")
    st.info(f"📧 Email: {USER_EMAIL}")

# ============================================================
# 🖼️ IMAGE TAB - FIXED LAYOUT
# ============================================================
if st.session_state.active_tab == "image":
    st.markdown("<div class='hero-text'><h1>AI Image Studio</h1><p>13 Free Models • 9:16 Ratio</p></div>", unsafe_allow_html=True)
    
    with st.container():
        # Title
        st.markdown("### 📝 Enter Prompt")
        img_prompt = st.text_area("Describe your image",
                                 placeholder="Jaise: beautiful anime girl with flowing hair",
                                 height=80,
                                 label_visibility="collapsed",
                                 key="img_prompt_input")
        
        st.markdown("### ⚙️ Settings")
        
        # Model Selection
        img_model = st.selectbox("🤖 Select Model", 
                                list(IMAGE_MODELS.keys()),
                                format_func=lambda x: f"{IMAGE_MODELS[x]['icon']} {IMAGE_MODELS[x]['label']}",
                                key="img_model_select",
                                label_visibility="collapsed")
        
        # Ratio Selection
        img_ratio = st.selectbox("📐 Image Ratio", 
                                ["9:16", "16:9"],
                                format_func=lambda x: f"▢ {x} HD",
                                key="img_ratio_select",
                                label_visibility="collapsed")
        
        # Token Info
        st.caption(f"🪙 {IMAGE_TOKEN_COST} tokens/image · {get_tokens_remaining(USER_EMAIL)} left today")
        
        # Generate Button
        gen_clicked = st.button("✨ Generate Image", use_container_width=True, key="gen_image_btn")

    if gen_clicked:
        if not img_prompt.strip():
            st.warning("⚠️ Pehle prompt likho.")
        elif get_tokens_remaining(USER_EMAIL) < IMAGE_TOKEN_COST:
            st.error(f"❌ Aaj ke free tokens khatam ho gaye. Image ke liye {IMAGE_TOKEN_COST} tokens chahiye, sirf {get_tokens_remaining(USER_EMAIL)} bache hain.")
        else:
            info = IMAGE_MODELS[img_model]
            provider = info.get("provider")
            
            with st.spinner("Image ban raha hai... ✨"):
                if provider == "pollinations":
                    img_url = run_with_progress(
                        lambda: get_image_url_pollinations(img_prompt, img_ratio),
                        estimate_seconds=8, label="Image ban raha hai")
                    deduct_tokens(USER_EMAIL, IMAGE_TOKEN_COST)
                    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
                    st.image(img_url, caption=f"{info['label']}: {img_prompt}", use_container_width=True)
                    st.session_state.gallery.insert(0, {"url": img_url, "prompt": img_prompt, "type": "image"})
                    
                elif provider == "agnes":
                    img_url, err = run_with_progress(
                        lambda: call_agnes_image(img_prompt, img_ratio),
                        estimate_seconds=15, label="Image ban raha hai")
                    if err:
                        st.error(err)
                    else:
                        deduct_tokens(USER_EMAIL, IMAGE_TOKEN_COST)
                        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
                        st.image(img_url, caption=f"{info['label']}: {img_prompt}", use_container_width=True)
                        st.session_state.gallery.insert(0, {"url": img_url, "prompt": img_prompt, "type": "image"})
                        
                elif provider == "huggingface":
                    model_id = info.get("model")
                    img_bytes, err = run_with_progress(
                        lambda: call_huggingface_image(img_prompt, model_id, img_ratio),
                        estimate_seconds=20, label="Image ban raha hai")
                    if err:
                        st.error(err)
                    else:
                        deduct_tokens(USER_EMAIL, IMAGE_TOKEN_COST)
                        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
                        st.image(img_bytes, caption=f"{info['label']}: {img_prompt}", use_container_width=True)
                        st.session_state.gallery.insert(0, {
                            "url": "data:image/png;base64," + base64.b64encode(img_bytes).decode(), 
                            "prompt": img_prompt, 
                            "type": "image"
                        })

    render_creativity_footer()

# ============================================================
# 🎬 VIDEO TAB - FIXED LAYOUT
# ============================================================
if st.session_state.active_tab == "video":
    st.markdown("<div class='hero-text'><h1>AI Video Studio</h1><p>8 Free Models</p></div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("### 📝 Enter Prompt")
        vid_prompt = st.text_area("Describe your video",
                                 placeholder="Jaise: person dancing in the rain",
                                 height=80,
                                 label_visibility="collapsed",
                                 key="vid_prompt_input")
        
        st.markdown("### ⚙️ Settings")
        
        # Model Selection
        vid_model = st.selectbox("🎥 Select Model",
                                list(VIDEO_MODELS.keys()),
                                format_func=lambda x: f"{VIDEO_MODELS[x]['icon']} {VIDEO_MODELS[x]['label']}",
                                key="vid_model_select",
                                label_visibility="collapsed")
        
        # Ratio Selection
        vid_ratio = st.selectbox("📐 Video Ratio",
                                ["9:16", "16:9"],
                                format_func=lambda x: f"▢ {x} HD",
                                key="vid_ratio_select",
                                label_visibility="collapsed")
        
        # Token Info
        st.caption(f"🪙 {VIDEO_TOKEN_COST} tokens/video · {get_tokens_remaining(USER_EMAIL)} left today")
        
        # Generate Button
        gen_vid_clicked = st.button("✨ Generate Video", use_container_width=True, key="gen_video_btn")

    if gen_vid_clicked:
        if not vid_prompt.strip():
            st.warning("⚠️ Pehle prompt likho.")
        elif get_tokens_remaining(USER_EMAIL) < VIDEO_TOKEN_COST:
            st.error(f"❌ Aaj ke free tokens khatam ho gaye.")
        else:
            info = VIDEO_MODELS[vid_model]
            provider = info.get("provider")
            
            with st.spinner("Video ban raha hai... 🎬"):
                if provider == "agnes":
                    vid_url, err = run_with_progress(
                        lambda: call_agnes_video(vid_prompt, vid_ratio),
                        estimate_seconds=55, label="Video ban raha hai")
                    if err:
                        st.error(err)
                    else:
                        deduct_tokens(USER_EMAIL, VIDEO_TOKEN_COST)
                        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
                        st.video(vid_url)
                        st.caption(f"🎬 {info['label']}: {vid_prompt}")

    render_creativity_footer()

# ============================================================
# 🎵 MUSIC TAB - FIXED LAYOUT
# ============================================================
if st.session_state.active_tab == "music":
    st.markdown("<div class='hero-text'><h1>AI Music Studio</h1><p>4 Free Models</p></div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("### 📝 Enter Description")
        song_prompt = st.text_area("Describe your song", 
                                  placeholder="Jaise: uplifting Hindi devotional or lo-fi beat",
                                  height=80, 
                                  label_visibility="collapsed",
                                  key="song_prompt_input")
        
        st.markdown("### ⚙️ Settings")
        
        # Model Selection
        music_model = st.selectbox("🎵 Select Model",
                                  list(MUSIC_MODELS.keys()),
                                  format_func=lambda x: f"{MUSIC_MODELS[x]['icon']} {MUSIC_MODELS[x]['label']}",
                                  key="music_model_select",
                                  label_visibility="collapsed")
        
        # Generate Button
        gen_music_clicked = st.button("✨ Generate Music", use_container_width=True, key="gen_music_btn")

    if gen_music_clicked:
        if not song_prompt.strip():
            st.warning("⚠️ Pehle description likho.")
        else:
            info = MUSIC_MODELS[music_model]
            provider = info.get("provider")
            
            with st.spinner("Music generate ho raha hai... 🎵"):
                if provider == "huggingface_music":
                    model_id = info.get("model")
                    audio_data, err = call_huggingface_music(song_prompt, model_id)
                    if err:
                        st.error(err)
                    else:
                        st.audio(audio_data, format="audio/wav")
                        st.caption(f"🎵 {info['label']}: {song_prompt}")

    render_creativity_footer()

# ============================================================
# 🌐 TRANSLATE TAB
# ============================================================
if st.session_state.active_tab == "translate":
    st.markdown("<div class='hero-text'><h1>Free Translate</h1><p>LibreTranslate</p></div>", unsafe_allow_html=True)
    
    LANGS = {"Auto": "auto", "Hindi": "hi", "English": "en", "Marathi": "mr", 
             "Gujarati": "gu", "Tamil": "ta", "Telugu": "te", "Bengali": "bn", 
             "Spanish": "es", "French": "fr", "Arabic": "ar", "Japanese": "ja"}
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            src = st.selectbox("🌐 Source Language", list(LANGS.keys()), index=0, key="src_lang")
        with col2:
            tgt = st.selectbox("🎯 Target Language", list(LANGS.keys()), index=2, key="tgt_lang")
        
        text = st.text_area("Text", height=100, placeholder="Yahan text likho...", label_visibility="collapsed", key="translate_text")
        
        if st.button("✨ Translate", use_container_width=True, key="gen_translate_btn"):
            if not text.strip():
                st.warning("⚠️ Pehle text likho.")
            else:
                with st.spinner("Translating... 🌐"):
                    translated, err = call_libretranslate(text.strip(), LANGS[src], LANGS[tgt])
                    if err:
                        st.error(err)
                    else:
                        st.text_area("Translation", value=translated, height=100, disabled=True, key="translated_output")
    
    render_creativity_footer()

# ============================================================
# 📸 GALLERY TAB
# ============================================================
if st.session_state.active_tab == "gallery":
    st.markdown("<div class='hero-text'><h1>Your Gallery</h1><p>All creations</p></div>", unsafe_allow_html=True)
    
    if not st.session_state.gallery:
        st.info("📸 Abhi kuch generate nahi kiya. AI ke saath create karo!")
    else:
        cols = st.columns(3)
        for i, item in enumerate(st.session_state.gallery[:24]):
            with cols[i % 3]:
                if item["type"] == "image":
                    st.image(item["url"], use_container_width=True)
                    st.caption(item["prompt"][:40] + "..." if len(item["prompt"]) > 40 else item["prompt"])
    
    render_creativity_footer()

# ============================================================
# 💬 CHAT TAB (DEFAULT)
# ============================================================
if st.session_state.active_tab == "chat":
    st.markdown("<div class='hero-text'><h1>Chat with AI</h1><p>10 Free Models • Instant Responses</p></div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("### 🤖 Select Model")
        chat_model = st.selectbox("Model",
                                 list(CHAT_MODELS.keys()),
                                 format_func=lambda x: f"{CHAT_MODELS[x]['icon']} {CHAT_MODELS[x]['label']}",
                                 key="chat_model_select",
                                 label_visibility="collapsed")
        
        st.markdown("### 💬 Your Message")
        chat_input = st.text_area("Message", 
                                 placeholder="Kuch pooch sakte ho...",
                                 height=100,
                                 label_visibility="collapsed",
                                 key="chat_input")
        
        if st.button("✨ Send", use_container_width=True, key="chat_send_btn"):
            if not chat_input.strip():
                st.warning("⚠️ Pehle message likho.")
            else:
                with st.spinner("Soch raha hai... 💭"):
                    info = CHAT_MODELS[chat_model]
                    response = call_groq_chat(chat_input, info.get("model_id"))
                    st.markdown("### 🤖 Response")
                    st.write(response)
    
    render_creativity_footer()

st.markdown("</div>", unsafe_allow_html=True)
