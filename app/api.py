

from fastapi import FastAPI
from pydantic import BaseModel
from data_loader import load_resources, load_encryption_key
from config import SYSTEM_PROMPT_GENERAL, FEW_SHOT_EXAMPLES
import google.generativeai as genai

# Load resources (these will be reused for every API request)
data, index, model, g_model = load_resources()
cipher = load_encryption_key()

app = FastAPI(title="Mental Health Chatbot API")

# Define the expected request body
class ChatRequest(BaseModel):
    username: str
    age_group: str
    specific_concern: str
    query: str
    previous_concerns: list = []  # Optional list of previous concerns

def get_similar_responses_api(query: str, data, index, model, top_k: int = 3):
    """
    Retrieve similar responses using the FAISS index.
    """
    query_embedding = model.encode(query).astype('float32').reshape(1, -1)
    distances, indices = index.search(query_embedding, top_k)
    similar_responses = data.iloc[indices[0]]['answerText'].tolist()
    return similar_responses

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    API endpoint that receives a chat request and returns a chatbot response.
    """
    # Build few-shot prompt section using predefined examples
    few_shot_prompt = "\n".join([
        f"User: {example['user_question']}\nBot: {example['bot_response']}"
        for example in FEW_SHOT_EXAMPLES
    ])
    
    # In the API, we don't maintain a persistent chat history,
    # so we leave that section empty or you could optionally allow it via the request.
    chat_history = ""
    
    # Retrieve context from similar responses using the FAISS index
    retrieved_responses = get_similar_responses_api(request.query, data, index, model, top_k=3)
    retrieved_context = "\n".join([f"Response {i+1}: {response}" 
                                   for i, response in enumerate(retrieved_responses)])
    
    # Construct the prompt by merging system instructions, few-shot examples, and user data
    prompt = f"""
    {SYSTEM_PROMPT_GENERAL}
    
    Few-Shot Examples:
    {few_shot_prompt}
    
    User Profile:
    - Name: {request.username}
    - Age Group: {request.age_group}
    - Specific Concern: {request.specific_concern}
    
    User's Previous Concerns:
    {', '.join(request.previous_concerns) if request.previous_concerns else "None"}
    
    User's Question: {request.query}
    
    Relevant responses:
    {retrieved_context}
    
    Please provide an empathetic and helpful response tailored to the user's profile, concerns, and question.
    """
    
    # Generate the response using the Gemini API model
    response = g_model.generate_content(prompt)
    validated_response = response.text.strip()
    
    return {"response": validated_response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
