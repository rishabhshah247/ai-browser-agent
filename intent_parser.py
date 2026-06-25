import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# 1. Setup: Load API Key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# 2. Schema: Isse Agent ko pata chalta hai ki output JSON mein hi dena hai
class ActionStep(BaseModel):
    step_description: str
    element_type: Optional[str] = None

class BrowserAction(BaseModel):
    action: Literal["fill_form", "navigate", "email", "summarize", "click", "clarification_needed"]
    target_url: Optional[str] = None
    data: Optional[dict] = None
    steps: List[ActionStep] = []
    clarifying_question: Optional[str] = None

# 3. System Prompt: Agent ka 'Dimag'
system_prompt = """You are a browser agent. Your task is to output STRICT JSON.
- If the command is clear, provide a detailed 'steps' list where each step describes a specific action.
- If the command is vague (e.g., 'buy it'), set 'action' to 'clarification_needed' and provide a 'clarifying_question' in the JSON field.
- DO NOT output any text outside the JSON block."""

# 4. API Client Setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def parse_intent(user_command: str):
    print(f"\n[Agent] Processing: '{user_command}'...")
    
    response = client.chat.completions.create(
        model="meta-llama/llama-3-8b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Command: {user_command}\n\nSchema: {BrowserAction.model_json_schema()}"}
        ],
        extra_headers={"HTTP-Referer": "https://browserautomationtool.pages.dev/", "X-Title": "Agent"}
    )
    
    return json.loads(response.choices[0].message.content)

# 5. Execution Block: Assignment ke saare commands yahan test honge
if __name__ == "__main__":
    # Tumhari 10 commands ki list (Assignment requirement)
    commands = [
        "Go to youtube and search for MS Dhoni",
        "Buy it",
        "Email my boss about the meeting",
        "Fill the login form with my name",
        "Summarize this page",
        "Close all tabs",
        "Navigate to google.com",
        "Click the subscribe button",
        "What is the price?",
        "Do it now"
    ]
    
    # Folder check
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    
    for cmd in commands:
        result = parse_intent(cmd)
        
        # File save logic
        file_name = f"outputs/result_{cmd.replace(' ', '_')[:10]}.json"
        with open(file_name, "w") as f:
            json.dump(result, f, indent=2)
            
        print(f"-> Saved: {file_name}")