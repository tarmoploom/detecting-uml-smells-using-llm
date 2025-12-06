import json
import sys
import os
from datetime import datetime, timezone

# ==========================================
# INPUT VARIABLES
# ==========================================

# 1. Your JSON input variable
json_input_text = """
{  
  "file_name": "test",
  "smell_analysis": [
    {
      "rule_id": "G5.1",
      "detected": false,
      "justification": "No empty diagrams were found."
    },
    {
      "rule_id": "G5.2",
      "detected": false,
      "justification": "All packages in the diagram are connected."
    },
    {
      "rule_id": "G8.1",
      "detected": true,
      "justification": "Found inconsistent naming conventions."
    }
  ]
}
"""

# The list to check against
check_list = ["G5.1", "G5.2", "G8.1"]

# Output configuration
output_directory_path = "/Users/home/Projects/Bakatoo/Results/Gemini/Oppejoud" 
llm_model_name = "gemini3.0"

# ==========================================
# LOGIC
# ==========================================

def main():
    print("--- Starting Validation Process ---")

    # Parse the input JSON
    try:
        data = json.loads(json_input_text)
    except json.JSONDecodeError as e:
        sys.exit(f"Error: Invalid JSON format. {e}")

    # Check if key exists
    if "file_name" not in data:
        sys.exit("Error: Input JSON is missing the required key 'file_name'.")
        
    filename = data["file_name"]

    # Check if value is valid
    if not filename or not isinstance(filename, str):
        sys.exit("Error: The value for 'file_name' is empty or invalid.")

    # Combine path with extracted name (appending .json)
    full_output_path = os.path.join(output_directory_path, f"{filename}.json")
    
    print(f"Target output file: {full_output_path}")

    # 2. Find the content list (dynamic key search)
    target_list = None
    original_key_name = ""
    
    for key, value in data.items():
        if isinstance(value, list):
            target_list = value
            original_key_name = key
            break
    
    if target_list is None:
        sys.exit("Error: No array/list found in the input JSON.")

    print(f"Found list under key: '{original_key_name}'")

    # 3.3 Check the count of smell list against check_list total
    if len(target_list) != len(check_list):
        sys.exit(f"Error (Condition 3.3): Smell count mismatch. Expected {len(check_list)}, found {len(target_list)}.")

    # iterate through the list to perform checks 3.1 and 3.2
    # We collect found IDs to verify 3.1 fully after the loop
    found_ids = []

    for index, item in enumerate(target_list):
        # We assume the structure matches: key 1, key 2, key 3.
        values = list(item.values())
        keys = list(item.keys())

        # 3.2 Part A: Check total of 3 keys
        if len(keys) != 3:
            sys.exit(f"Error (Condition 3.2): Item at index {index} does not have exactly 3 keys.")

        # 3.2 Part B: None of the key values are empty or empty string
        for k, v in item.items():
            if v is None or v == "":
                sys.exit(f"Error (Condition 3.2): Found empty value for key '{k}' at index {index}.")

        # 3.2 Part C: Check does the second key (2) value is boolean
        if not isinstance(values[1], bool):
            sys.exit(f"Error (Condition 3.2): The second value (key: '{keys[1]}') at index {index} is not a boolean.")

        # Collect ID for 3.1 check
        found_ids.append(values[0])

    # 3.1 Check if check_list values are present in the "smell_analysis"
    for check_val in check_list:
        if check_val not in found_ids:
            sys.exit(f"Error (Condition 3.1): Required ID '{check_val}' not found in the input data.")

    print("--- All Validation Checks Passed ---")

    # 6. Create new JSON structure
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ') # Generate timestamp (UTC)

    final_output = {
        "file_name": filename,
        "timestamp": current_time,
        "llm_model": llm_model_name,
        "smell_analysis": target_list # Using the list we extracted
    }

    # 8. Save to path, does not overwrite if exists
    if os.path.exists(full_output_path):
        sys.exit(f"Error (Condition 8): The file '{full_output_path}' already exists. Operation aborted.")
    
    try:
        # 'x' mode for exclusive mode: new file
        with open(full_output_path, 'x', encoding='utf-8') as f:
            json.dump(final_output, f, indent=2)
            print(f"Success: File saved as '{full_output_path}'")
            
    except FileExistsError:
        sys.exit(f"Error (Condition 8): The file '{full_output_path}' already exists.")
    except Exception as e:
        # Catches missing directories (FileNotFoundError) and other I/O issues
        sys.exit(f"Error: Could not save file. {e}")

if __name__ == "__main__":
    main()
