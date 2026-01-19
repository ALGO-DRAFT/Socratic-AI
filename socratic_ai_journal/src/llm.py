import ollama
from typing import Generator, List, Dict
from src.config import OLLAMA_MODEL, SOCRATIC_SYSTEM_PROMPT
import time

def stream_chat_response(messages: List[Dict[str, str]]) -> Generator[str, None, None]:
    """
    Yields chunks of text from the Ollama model.
    Injects the system prompt if not present.
    Includes retry logic for connection issues.
    """
    # Defensive copy to avoid mutating the state directly in the generator
    conversation = list(messages)
    
    # Prepend System Prompt 
    if not conversation or conversation[0]['role'] != 'system':
        conversation.insert(0, {'role': 'system', 'content': SOCRATIC_SYSTEM_PROMPT})
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Call Ollama API with streaming enabled 
            stream = ollama.chat(
                model=OLLAMA_MODEL,
                messages=conversation,
                stream=True,
            )
            
            for chunk in stream:
                content = chunk['message']['content']
                if content:
                    yield content
            
            return  # Success, exit
                
        except Exception as e:
            retry_count += 1
            error_msg = str(e)
            
            if retry_count < max_retries:
                yield f"\n\n⏳ Connection interrupted. Retrying ({retry_count}/{max_retries})...\n\n"
                time.sleep(2)  # Wait 2 seconds before retry
            else:
                # Final attempt failed
                yield f"\n\n**⚠️ Error:** Could not connect to Ollama after {max_retries} attempts.\n\n"
                yield "**Troubleshooting:**\n"
                yield "1. Ensure 'ollama serve' is running in a terminal\n"
                yield "2. Check that the llama3 model is available: `ollama list`\n"
                yield f"3. Details: {error_msg}\n\n"
                yield "For now, you can still journal and explore your emotional trajectory. AI responses will be available once Ollama reconnects."