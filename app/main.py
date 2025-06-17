# ===============================
# ✅ 1️⃣  IMPORTS & FIREBASE SETUP
# ===============================
import firebase_admin
from firebase_admin import credentials, db

import streamlit as st
from data_loader import load_resources, load_encryption_key
from chatbot_logic import conversation_chat, collect_user_profile, display_faqs

import json

# ✅ Firebase Admin SDK setup — USE SECRETS ONLY for Cloud
if not firebase_admin._apps:
    # Load Firebase credentials from Streamlit secrets (secure!)
    firebase_key = dict(st.secrets["firebase"])
    cred = credentials.Certificate(firebase_key)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://mental-chatbot-f0047-default-rtdb.firebaseio.com/'
    })

# ✅ Load NLP resources
data, index, model, g_model = load_resources()
cipher = load_encryption_key()

# ✅ Streamlit page config
st.set_page_config(
    page_title="Mental Health Support Chatbot",
    page_icon="🧠",
    layout="wide",
)

# ===============================
# ✅ 2️⃣  FIREBASE SAVE & LOAD
# ===============================
def save_chat_history(user_id, history):
    ref = db.reference(f'chats/{user_id}')
    ref.set(history)

def load_chat_history(user_id):
    ref = db.reference(f'chats/{user_id}')
    data = ref.get()
    return data if data else []

# ===============================
# ✅ 3️⃣  MAIN CHAT LOGIC
# ===============================
def display_chat_history():
    # ✅ Ensure needed session keys exist
    if 'user_profile' not in st.session_state:
        st.session_state['user_profile'] = {}
    if 'greeted' not in st.session_state:
        st.session_state['greeted'] = False

    # ✅ Step 1: Collect user profile to get user_id
    collect_user_profile(cipher)
    user_profile = st.session_state['user_profile']
    user_id = user_profile.get("name", "anonymous").replace(" ", "_").lower()

    # ✅ Step 2: Load chat history from Firebase ONCE
    if 'history' not in st.session_state:
        st.session_state['history'] = load_chat_history(user_id)

    # ✅ Step 3: Display FAQs
    display_faqs()

    # ✅ Step 4: Greet once if needed
    if not st.session_state['greeted'] and user_profile.get("name") and user_profile.get("specific_concern"):
        name = user_profile['name']
        concern = user_profile['specific_concern']
        st.session_state['history'].append(("Chatbot", f"Hello {name}! I see you’re here about {concern}. How can I assist you?"))
        st.session_state['greeted'] = True
        save_chat_history(user_id, st.session_state['history'])

    # ✅ Step 5: Chat UI
    st.header("Chat with Rianess Bot")
    chat_placeholder = st.container()

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Your Question:", placeholder="Ask about your mental health")
        submit_button = st.form_submit_button(label="Send")

        if submit_button and user_input:
            response = conversation_chat(user_input, data, index, model, g_model, cipher)
            st.session_state['history'].append(("You", user_input))
            st.session_state['history'].append(("Chatbot", response))
            save_chat_history(user_id, st.session_state['history'])

    with chat_placeholder:
        for sender, message in st.session_state['history']:
            st.markdown(f"**{sender}:** {message}")
            st.markdown("---")

    st.write("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)

# ===============================
# ✅ 4️⃣  APP ENTRY POINT
# ===============================
def main():
    display_chat_history()
    st.markdown("---")
    st.write("Note: This chatbot is for informational purposes and is created by vmlambiti.")

if __name__ == "__main__":
    main()
