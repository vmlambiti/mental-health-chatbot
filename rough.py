def conversation_chat(query, data, index, model, g_model):
    user_profile = st.session_state.get("user_profile", {})
    age_group = user_profile.get("age_group", "Not specified")
    specific_concern = user_profile.get("specific_concern", "General support")

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

    # Prompt construction
    prompt = f"""
    {SYSTEM_PROMPT_GENERAL}

    Few-Shot Examples:
    {few_shot_prompt}

    Chat History:
    {chat_history}

    User Profile:
    - Age Group: {age_group}
    - Specific Concern: {specific_concern}

    User's Question: {query}

    Please provide an empathetic and helpful response tailored to the user's profile.
    """
    response = g_model.generate_content(prompt)
    st.session_state['chat_memory'].append({"user": query, "bot": response.text})
    return response.text