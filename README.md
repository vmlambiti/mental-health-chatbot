# Mental Health Chatbot

## Overview
The **Mental Health Chatbot** is an AI-powered support tool designed to provide empathetic, personalized, and evidence-based guidance for mental health concerns. Built using cutting-edge technologies like Streamlit, FAISS, and Google's Generative AI, this chatbot delivers a secure and tailored experience for users seeking mental well-being support.

---

## Features
- **Personalized Support**: Tailored responses based on user age group and specific concerns (e.g., work stress, anxiety, sleep).
- **Secure Data Handling**: Uses encryption to securely store user concerns and maintains HIPAA-level privacy compliance.
- **Context-Aware Responses**: Integrates previous user interactions and "Your Previous Concerns" to provide consistent, context-driven replies.
- **Few-Shot Learning**: Leverages examples to improve chatbot accuracy and understand nuanced questions.
- **FAQ Integration**: Includes a dynamic FAQ section for quick answers to common mental health queries.
- **User Data Management**: Users can save their concerns and delete their data at any time, ensuring complete control over personal information.

---

## Project Structure

```plaintext
mental_health_chatbot/
│
├── app/                 # Application code
│   ├── chatbot_logic.py  # Core chatbot logic and processing
│   ├── config.py         # Configuration and prompt definitions
│   ├── data_loader.py    # Resource loading and setup
│   ├── main.py           # Streamlit interface
├── data/                # Data files and resources
│   ├── counselchat_with_embeddings.pkl
│   ├── faiss_index.bin
│   ├── faqs.csv
│   ├── encryption_key.key
│   ├── user_memory.json
├── setup.py             # Setup script for easy installation
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── README.md            # Project documentation
└── .gitignore           # Ignored files
