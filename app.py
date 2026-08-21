import streamlit as st
import os
from dotenv import load_dotenv

from prompts import (
    SUB_AGENT_PROMPTS,
    SUB_AGENT_NAMES,
    get_subagent_prompt,
    get_full_dossier_prompt,
)
from gemini_client import generate_heyteck_output

load_dotenv()

st.set_page_config(
    page_title="HeyTeck AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown('<h1 style="color: #FF4B4B;">⚡ HeyTeck AI</h1>', unsafe_allow_html=True)
st.markdown('### Master Performance & UGC Operations Engine')

with st.sidebar:
    st.header("⚙️ Configuration")
    env_api_key = os.environ.get("GEMINI_API_KEY", "")
    user_api_key = st.text_input("🔑 Gemini API Key", value=env_api_key, type="password")
    selected_model = st.selectbox("🧠 AI Model", options=["gemini-3.6-flash", "gemini-1.5-flash"], index=0)
    mode = st.radio("Select Mode:", options=["⚡ Single Sub-Agent", "🔀 Multi-Select Mode", "🚀 Full Dossier Mode [FULL]"])

col_input, col_output = st.columns([1, 1])

DEFAULT_SAMPLE = """Product: AquaGlow Hydrating Vitamin C Serum
Target Audience: Women 22-38 dealing with dull skin, acne scars.
Core Offer: Buy 1 Get 1 Free + Free Shipping.
Goal: High-converting Meta UGC Ad campaign."""

with col_input:
    st.subheader("📝 Product Brief")
    product_brief = st.text_area("Product Details:", value=DEFAULT_SAMPLE, height=250)

    if mode == "⚡ Single Sub-Agent":
        selected_agent = st.selectbox("Select Sub-Agent:", options=list(SUB_AGENT_PROMPTS.keys()))
        trigger_btn = st.button(f"⚡ Run [{selected_agent}]", type="primary", use_container_width=True)
    else:
        trigger_btn = st.button("🚀 Run Full Dossier [FULL]", type="primary", use_container_width=True)

with col_output:
    st.subheader("📊 Output")
    if trigger_btn and user_api_key:
        with st.spinner("Executing HeyTeck AI..."):
            prompt = get_full_dossier_prompt(product_brief) if mode != "⚡ Single Sub-Agent" else get_subagent_prompt(selected_agent, product_brief)
            output = generate_heyteck_output(prompt, api_key=user_api_key, model_name=selected_model)
            st.markdown(output)
