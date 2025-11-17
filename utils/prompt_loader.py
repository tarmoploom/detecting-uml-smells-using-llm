import yaml
from pathlib import Path

# --- Helper to find the project root ---
# This function helps locate the 'prompts' directory relative to the project root
# when prompt_loader.py is imported from anywhere within the project.
def _find_project_root_for_prompts():
    current_script_path = Path(__file__).resolve()
    # Walk up the directory tree to find the common parent that contains both 'prompts' and 'utils'
    for parent in current_script_path.parents:
        if (parent / "prompts").is_dir() and (parent / "utils").is_dir():
            return parent
    raise FileNotFoundError(
        "Could not find the project root. Ensure 'prompts' and 'utils' "
        "directories are siblings under the project root."
    )

_project_root = _find_project_root_for_prompts()
_PROMPT_DIR = _project_root / "prompts"

# --- Function to load a single YAML prompt file as a dictionary ---
def load_prompt_as_dict(file_name: str) -> dict:
    """
    Loads a single YAML prompt file by its name (e.g., "prompt_1.yaml")
    from the 'prompts' directory and returns its content as a Python dictionary.
    """
    prompt_file_path = _PROMPT_DIR / file_name
    
    if not prompt_file_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file_path}")

    with open(prompt_file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


# Uncomment loading here, if load_prompt_as_dict(file_name) used dynamically
# prompt_1 = load_prompt_as_dict("prompt_1.yaml")
