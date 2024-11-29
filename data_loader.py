import os
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import json
import google.generativeai as genai
# Load environment variables
load_dotenv()

FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH")
DATA_PATH = os.getenv("DATA_PATH")
ENCRYPTION_KEY_PATH = os.getenv("ENCRYPTION_KEY_PATH")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


def load_resources():
    index = faiss.read_index(FAISS_INDEX_PATH)
    data = pd.read_pickle(DATA_PATH)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    g_model = genai.GenerativeModel("gemini-1.5-flash")
    return data, index, model, g_model

def load_encryption_key():
    with open(ENCRYPTION_KEY_PATH, "rb") as file:
        return Fernet(file.read())

def encrypt_data(data, cipher):
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(data, cipher):
    return cipher.decrypt(data.encode()).decode()

def load_user_memory():
    try:
        with open("user_memory.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_user_memory(user_memory):
    with open("user_memory.json", "w") as file:
        json.dump(user_memory, file)
