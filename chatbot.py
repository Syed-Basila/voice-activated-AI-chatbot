import streamlit as st
import requests
import speech_recognition as sr

# API Key
API_KEY = "42d6f53544cbfc0f803b79b6f2563e45d64b1e5258c559189cdf94727af801ef"

# API Call Function
def call_together_api(prompt_text):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "You're Basi's helpful assistant."},
            {"role": "user", "content": prompt_text}
        ],
    }

    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200:
        return res.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {res.status_code} - {res.text}"

# Recognizer
recognizer = sr.Recognizer()

# Page Config
st.set_page_config(page_title="AI Chat", layout="wide")

# Custom CSS for doodle background, fonts, mic button, and bubbles
st.markdown("""
    <style>
        html, body {
            background-image: url("https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1740&q=80");
        background-size: cover;
            font-family: 'Segoe UI', sans-serif;
        }
        .chat-container {
            max-width: 900px;
            margin: auto;
        }
        .chat-bubble {
            padding: 15px 20px;
            margin: 8px 0;
            border-radius: 20px;
            width: fit-content;
            max-width: 80%;
            font-size: 16px;
            line-height: 1.6;
        }
        .user {
            background-color: #d2f8d2;
            align-self: flex-start;
            margin-left: 0;
        }
        .assistant {
            background-color: #e6e6e6;
            align-self: flex-end;
            margin-left: auto;
        }
        .mic-button {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background-color: #25d366;
            border: none;
            border-radius: 50%;
            width: 70px;
            height: 70px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            cursor: pointer;
        }
        .mic-button:hover {
            background-color: #20ba5a;
        }
        .mic-icon {
            color: white;
            font-size: 30px;
        }
        .mic-label {
            position: fixed;
            bottom: 110px;
            right: 15px;
            font-weight: bold;
            color: #25d366;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Voice-Activated AI Chat</h1>", unsafe_allow_html=True)

# Session state for messages
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Mic UI
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

mic_clicked = st.button("🎤", key="mic-button")

if mic_clicked:
    st.markdown("<div class='mic-label'>Start Speaking</div>", unsafe_allow_html=True)
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            voice_input = recognizer.recognize_google(audio)
            st.session_state.history.append({"role": "user", "content": voice_input})
            response = call_together_api(voice_input)
            st.session_state.history.append({"role": "assistant", "content": response})
        except sr.UnknownValueError:
            st.session_state.history.append({"role": "assistant", "content": "Sorry, I couldn't understand your speech."})
        except sr.RequestError:
            st.session_state.history.append({"role": "assistant", "content": "Service unavailable. Please try again later."})

# Render chat messages
for msg in st.session_state['history']:
    role = "user" if msg["role"] == "user" else "assistant"
    bubble_class = f"chat-bubble {role}"
    st.markdown(f"<div class='{bubble_class}'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Floating mic icon
st.markdown("""
    <script>
        const btn = window.parent.document.querySelector('button[k="mic-button"]');
        if (btn) {
            btn.classList.add('mic-button');
            btn.innerHTML = '<span class="mic-icon">🎤</span>';
        }
    </script>
""", unsafe_allow_html=True)
