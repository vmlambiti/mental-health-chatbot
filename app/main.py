import streamlit as st
from data_loader import load_resources, load_encryption_key
from chatbot_logic import conversation_chat, initialize_session_state, collect_user_profile, display_faqs

# Initialize resources
data, index, model, g_model = load_resources()
cipher = load_encryption_key()

# Streamlit app configuration
st.set_page_config(
    page_title="Mental Health Support Chatbot",
    page_icon="🧠",
    layout="wide",
)

def display_chat_history():
    collect_user_profile(cipher)
    display_faqs()

    # Greet user after personalization details are filled
    user_profile = st.session_state.get("user_profile", {})
    if not st.session_state['greeted'] and user_profile.get("name") and user_profile.get("specific_concern"):
        name = user_profile["name"]
        specific_concern = user_profile["specific_concern"]
        st.session_state['history'].append(("Chatbot", f"Hello {name}! I see you’re here about {specific_concern}. How can I assist you?"))
        st.session_state['greeted'] = True

    st.header("Chat with the Mental Health Support Bot")
    
    # Create a placeholder for the chat history
    chat_placeholder = st.container()

    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input("Your Question:", placeholder="Ask about your mental health", key='input')
        submit_button = st.form_submit_button(label="Send")

        if submit_button and user_input:
            response = conversation_chat(user_input, data, index, model, g_model)
            st.session_state['history'].append(("You", user_input))
            st.session_state['history'].append(("Chatbot", response))

    # Update the placeholder with the latest chat history
    with chat_placeholder:
        if st.session_state['history']:
            for sender, message in st.session_state['history']:
                st.markdown(f"**{sender}:** {message}")
                st.markdown("---")

    # Automatically scroll to the bottom of the chat
    st.write("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)


def main():
    initialize_session_state()
    display_chat_history()
    st.markdown("---")
    st.write("Note: This chatbot is for informational purposes and is not a substitute for professional mental health advice.")

if __name__ == "__main__":
    main()
