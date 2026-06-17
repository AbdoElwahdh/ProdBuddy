import os
import time
import base64
from typing import Optional, List, Dict
from libs.GeminiWrapper.GeminiWrapper import GeminiWrapper
from libs.GeminiWrapper.models import InputParams, TextParams

# Simple in-memory storage for chat history. 
# Key: user_id (str), Value: List of messages (Dicts with role and parts).
CHAT_HISTORY: Dict[str, List[Dict[str, str]]] = {}
MAX_HISTORY_LENGTH = 5  # Keep last 5 messages per user

# Set up a temporary directory to store audio files
TEMP_AUDIO_DIR = os.path.join(os.getcwd(), "temp_audio")
if not os.path.exists(TEMP_AUDIO_DIR):
    os.makedirs(TEMP_AUDIO_DIR)

def transcribe_audio(audio_base64: str) -> str:
    """
    Takes base64 audio, sends it to Gemini GenAI client directly for transcription,
    and returns the transcribed text.
    """
    from google import genai
    from google.genai import types
    
    # Omit api_key to let it auto-resolve from environment, matching GeminiWrapper
    client = genai.Client()
    audio_data = base64.b64decode(audio_base64)
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                "Please transcribe this audio exactly as spoken in its original language. Return only the transcription, no additional commentary.",
                types.Part.from_bytes(
                    data=audio_data,
                    mime_type='audio/webm',
                )
            ]
        )
        return response.text.strip()
    except Exception as e:
        print(f"Transcription error: {e}")
        return "Sorry, I couldn't understand the audio."

def get_chat_response(message: str, user_id: str = "default_user") -> str:
    """
    Passes a user text message to the Gemini API with history.
    """
    wrapper = GeminiWrapper()
    
    # Update History
    if user_id not in CHAT_HISTORY:
        CHAT_HISTORY[user_id] = []
        
    history = CHAT_HISTORY[user_id]
            
    # Build a combined prompt containing history for context
    history_context = ""
    if history:
        history_context = "Previous Conversation History:\n"
        for msg in history:
            history_context += f"[{msg['role']}]: {msg['content']}\n"
        history_context += "\nCurrent Message from User: "
        
    final_prompt = history_context + message
    
    # Set up parameters
    input_params = InputParams(
        prompt=final_prompt,
        system_instruction="You are a helpful productivity assistant named ProdBuddy. You help the user manage their tasks and time effectively. Keep responses concise.",
    )
    
    result = wrapper.generate_text(input_params=input_params)
    
    if result["success"]:
        ai_reply = result["content"]
        
        # Save to history
        # We append the user message and AI reply
        history.append({"role": "User", "content": message})
        history.append({"role": "ProdBuddy", "content": ai_reply})
        
        # Trim history
        # Since each turn adds 2 entries, 5 full messages means 10 entries max
        if len(history) > MAX_HISTORY_LENGTH * 2:
            CHAT_HISTORY[user_id] = history[-(MAX_HISTORY_LENGTH * 2):]
            
        return ai_reply
    else:
        return f"Sorry, I encountered an error: {result['error']}"
