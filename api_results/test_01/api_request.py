import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2] 
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# --- Import your prompt dictionaries from utils.prompt_loader ---
from utils.prompt_loader import load_prompt_as_dict


prompt = load_prompt_as_dict("prompt_1.yaml")

# --- Use the imported prompt dictionaries using string-based key access ---
print("--- Using Prompt ---")
print("Name:", prompt['name']) # Accessing via string key
print("Version:", prompt['version'])
print("System Message:", prompt['system_message'])
