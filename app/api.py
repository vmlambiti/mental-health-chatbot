from fastapi import FastAPI
from pydantic import BaseModel
from data_loader import load_resources, load_encryption_key
from config import SYSTEM_PROMPT_GENERAL, FEW_SHOT_EXAMPLES
import google.generativeai as genai
import google.api_core.exceptions

# === Load shared resources ===
data, index, model, g_model = load_resources()
cipher = load_encryption_key()

app = FastAPI(title="Mental Health Chatbot API")

class ChatRequest(BaseModel):
    username: str
    age_group: str
    specific_concern: str
    query: str
    previous_concerns: list = []
    chat_history: list = []  # 👈 NEW: optional chat memory from client

def get_similar_responses(query: str, data, index, model, top_k: int = 3):
    query_embedding = model.encode(query).astype('float32').reshape(1, -1)
    distances, indices = index.search(query_embedding, top_k)
    similar_responses = data.iloc[indices[0]]['answerText'].tolist()
    return similar_responses

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    This is the backend API for your chatbot.
    It uses Gemini + FAISS to craft a context-aware response.
    """

    # === Build few-shot prompt ===
    few_shot_prompt = "\n".join([
        f"User: {example['user_question']}\nBot: {example['bot_response']}"
        for example in FEW_SHOT_EXAMPLES
    ])

    # === Chat history (from frontend or previous API calls) ===
    chat_history = "\n".join([
        f"User: {entry['user']}\nBot: {entry['bot']}"
        for entry in request.chat_history
    ])

    # === Retrieve context from FAISS ===
    retrieved_responses = get_similar_responses(request.query, data, index, model, top_k=3)
    retrieved_context = "\n".join([
        f"Response {i+1}: {r}" for i, r in enumerate(retrieved_responses)
    ])

    # === Final prompt ===
    prompt = f"""
    {SYSTEM_PROMPT_GENERAL}

    Few-Shot Examples:
    {few_shot_prompt}

    Chat History:
    {chat_history}

    User Profile:
    - Name: {request.username}
    - Age Group: {request.age_group}
    - Specific Concern: {request.specific_concern}

    User's Previous Concerns:
    {', '.join(request.previous_concerns) if request.previous_concerns else "None"}

    User's Question: {request.query}

    Relevant Responses:
    {retrieved_context}

    Please provide an empathetic and helpful response tailored to the user's profile, concerns, and question.
    """

    # === Call Gemini with timeout ===
    try:
        response = g_model.generate_content(
            prompt,
            request_options={"timeout": 30}
        )
        if hasattr(response, 'text'):
            validated_response = response.text.strip()
        elif hasattr(response, 'candidates'):
            validated_response = response.candidates[0].content.parts[0].text.strip()
        else:
            validated_response = str(response).strip()

    except google.api_core.exceptions.DeadlineExceeded:
        validated_response = "Sorry, my answer took too long. Please try again."

    except Exception as e:
        validated_response = f"Oops! Something went wrong: {e}"

    return {"response": validated_response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
