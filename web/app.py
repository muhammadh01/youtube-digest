import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "https://api.durak.dev")

st.set_page_config(page_title="durak — YouTube Digest", page_icon="🎬", layout="centered")

st.title("🎬 youtube-digest")
st.caption("Paste a YouTube URL. Get a structured summary in seconds.")

url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
go = st.button("Summarize", type="primary", use_container_width=True)

if go:
    if not url.strip():
        st.warning("Please enter a YouTube URL.")
    else:
        with st.spinner("Fetching transcript and summarizing..."):
            try:
                response = requests.post(f"{API_URL}/summarize", json={"url": url.strip()}, timeout=180)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("cached"):
                        st.success("⚡ Cached result")
                    else:
                        st.success("✅ Fresh summary")
                    st.markdown(data["summary"])
                else:
                    st.error(f"API error {response.status_code}: {response.json().get('detail', 'unknown')}")
            except requests.exceptions.Timeout:
                st.error("Request timed out. Try a shorter video.")
            except Exception as exc:
                st.error(f"Error: {exc}")

st.divider()
st.caption("Built with FastAPI, Redis, nginx, and Streamlit · github.com/muhammadh01/youtube-digest")
