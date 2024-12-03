import streamlit as st
import pandas as pd
from data_loader import load_user_memory, save_user_memory, encrypt_data, decrypt_data
from config import SYSTEM_PROMPT_GENERAL, FEW_SHOT_EXAMPLES
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATA_PATH = os.getenv("DATA_PATH", "data/")
FAQS_PATH = os.path.join(DATA_PATH, "faqs.csv")
genai.configure(api_key=GEMINI_API_KEY)

def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    if 'greeted' not in st.session_state:
        st.session_state['greeted'] = False
    if 'chat_memory' not in st.session_state:
        st.session_state['chat_memory'] = []

def collect_user_profile(cipher):
    st.sidebar.markdown("## Personalize Your Experience")
    username = st.sidebar.text_input("Enter your name", key="username")
    age_group = st.sidebar.selectbox(
        "Select Your Age Group",
        ["Teen", "Young Adult", "Adult", "Senior"],
        key="age_group"
    )
    specific_concern = st.sidebar.text_input("What area would you like help with? (e.g., work stress, anxiety, sleep)")

    # Save Concern Button
    if st.sidebar.button("Save Concern"):
        if specific_concern.strip():
            encrypted_concern = encrypt_data(specific_concern, cipher)
            user_memory = load_user_memory()
            user_memory.setdefault(username, []).append(encrypted_concern)
            save_user_memory(user_memory)
            st.sidebar.success(f"Thank you, {username}! Your concern has been saved securely.")
            # Set user profile in session state
            st.session_state["user_profile"] = {
                "name": username,
                "age_group": age_group,
                "specific_concern": specific_concern
            }
            st.session_state['greeted'] = False  # Reset greeting status

    # Display Previous Concerns & Option to Clear Data
    if username:
        user_memory = load_user_memory()
        concerns = user_memory.get(username, [])
        if concerns:
            st.sidebar.markdown("### Your Previous Concerns:")
            for i, concern in enumerate([decrypt_data(c, cipher) for c in concerns], 1):
                st.sidebar.write(f"{i}. {concern}")

            # Add Delete My Data Button
            if st.sidebar.button("Delete My Data"):
                delete_user_data(username)
                st.sidebar.success("Your data has been deleted.")
                st.session_state['greeted'] = False  # Reset greeting on deletion

            # Add End Session Button
            if st.sidebar.button("End Session"):
                st.session_state['history'] = []  # Clear session history
                st.session_state['chat_memory'] = []  # Clear chat memory
                st.sidebar.success("Session ended successfully.")
        else:
            st.sidebar.info("You have no saved concerns.")

def delete_user_data(username):
    user_memory = load_user_memory()
    if username in user_memory:
        del user_memory[username]
        save_user_memory(user_memory)
    else:
        st.sidebar.warning("No data found for this user.")

def conversation_chat(query, data, index, model, g_model, cipher):
    user_profile = st.session_state.get("user_profile", {})
    username = user_profile.get("name", "User")
    age_group = user_profile.get("age_group", "Not specified")
    specific_concern = user_profile.get("specific_concern", "General support")

    # Load previous concerns
    user_memory = load_user_memory()
    encrypted_concerns = user_memory.get(username, [])
    previous_concerns = [decrypt_data(c, cipher) for c in encrypted_concerns]

    # Few-shot examples
    few_shot_prompt = "\n".join([
        f"User: {example['user_question']}\nBot: {example['bot_response']}"
        for example in FEW_SHOT_EXAMPLES
    ])

    # Chat history
    chat_history = "\n".join([
        f"User: {entry['user']}\nBot: {entry['bot']}"
        for entry in st.session_state['chat_memory']
    ])

    # Construct the prompt
    prompt = f"""
    {SYSTEM_PROMPT_GENERAL}

    Few-Shot Examples:
    {few_shot_prompt}

    Chat History:
    {chat_history}

    User Profile:
    - Name: {username}
    - Age Group: {age_group}
    - Specific Concern: {specific_concern}

    User's Previous Concerns:
    {', '.join(previous_concerns) if previous_concerns else "None"}

    User's Question: {query}

    Please provide an empathetic and helpful response tailored to the user's profile, concerns, and question.
    """

    # Generate response
    response = g_model.generate_content(prompt)
    validated_response = response.text.strip()

    # Save to session state (only in memory)
    st.session_state['chat_memory'].append({"user": query, "bot": validated_response})
    return validated_response

def display_faqs():
    st.sidebar.markdown("## Frequently Asked Questions")
    try:
        faqs = pd.read_csv(FAQS_PATH)
        for _, row in faqs.iterrows():
            with st.sidebar.expander(row['Question']):
                st.write(row['Answer'])
    except FileNotFoundError:
        st.sidebar.error("FAQs file not found. Please upload 'faqs.csv' to the specified directory.")
