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
  "file_name": "test_script",
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

# The smell list to check against
check_list = ["G5.1", "G5.2", "G8.1"]

# Path Configuration
end_folder = "Oppejoud"
llm_model_name = "gemini3.0"

# Calculate absolute paths based on script location
script_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Output Folder Path
output_path = os.path.join(script_dir, "Results/Gemini", end_folder)

# 2. Ground Truth Folder Path
ground_truth_path = os.path.join(script_dir, "Data", end_folder)


# ==========================================
# LOGIC
# ==========================================

def main():
    print("--- Starting Validation Process ---")

    # -------------------------------------------------
    # 1. Parse JSON and Extract Filename
    # -------------------------------------------------
    try:
        data = json.loads(json_input_text)
    except json.JSONDecodeError as e:
        sys.exit(f"Error: Invalid JSON format. {e}")

    if "file_name" not in data:
        sys.exit("Error: Input JSON is missing the required key 'file_name'.")
        
    filename = data["file_name"]

    if not filename or not isinstance(filename, str):
        sys.exit("Error: The value for 'file_name' is empty or invalid.")

    # -------------------------------------------------
    # 2. Setup and Check Paths (Strict Mode)
    # -------------------------------------------------
    full_output_path = os.path.join(output_path, f"{filename}.json")
    full_ground_truth_path = os.path.join(ground_truth_path, f"{filename}.txt")

    print(f"Target Output:       {full_output_path}")
    print(f"Target Ground Truth: {full_ground_truth_path}")

    # Ensure Output Directory Exists
    if not os.path.exists(output_path):
        sys.exit(f"Error: Output directory does not exist: {output_path}")

    # Ensure Output File does NOT exist
    if os.path.exists(full_output_path):
        sys.exit(f"Error (Condition 8): The output file '{full_output_path}' already exists. Operation aborted.")

    # Ensure Ground Truth File Exists
    if not os.path.exists(full_ground_truth_path):
        sys.exit(f"Error: Ground truth file not found: {full_ground_truth_path}")

    # -------------------------------------------------
    # 3. Read Ground Truth Content
    # -------------------------------------------------
    gt_content = ""
    try:
        with open(full_ground_truth_path, 'r', encoding='utf-8') as f:
            gt_content = f.read()
        print("Success: Ground truth file read.")
    except Exception as e:
        sys.exit(f"Error: Could not read ground truth file. {e}")

    # -------------------------------------------------
    # 4. Find Target List in JSON
    # -------------------------------------------------
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

    # -------------------------------------------------
    # 5. Perform Validation Checks
    # -------------------------------------------------

    # 1 Check Count
    if len(target_list) != len(check_list):
        sys.exit(f"Error (Condition 1): Smell count mismatch. Expected {len(check_list)}, found {len(target_list)}.")

    found_ids = []

    for index, item in enumerate(target_list):
        values = list(item.values())
        keys = list(item.keys())

        # 2.1 Part A: 3 Keys exactly
        if len(keys) != 3:
            sys.exit(f"Error (Condition 2.1): Item at index {index} does not have exactly 3 keys.")

        # 2.2 Part B: No empty values
        for k, v in item.items():
            if v is None or v == "":
                sys.exit(f"Error (Condition 2.2): Found empty value for key '{k}' at index {index}.")

        # 2.3 Part C: 2nd Value is Boolean
        if not isinstance(values[1], bool):
            sys.exit(f"Error (Condition 2.3): The second value (key: '{keys[1]}') at index {index} is not a boolean.")

        # ID Collection for condition 3
        current_rule_id = values[0]
        found_ids.append(current_rule_id)

        # -------------------------------------------------
        # Compare against Ground Truth & Reorder Keys (Index Based)
        # -------------------------------------------------
        
        # Calculate ground truth (if present -> True, else False)
        is_present = current_rule_id in gt_content

        # Create a new, ordered dictionary
        ordered_item = {}
        
        # Iterate over keys by index
        for i, k in enumerate(keys):
            # Add existing key/value
            ordered_item[k] = item[k]
            # at index 0, we inject "actual" immediately after
            if i == 0:
                ordered_item["actual"] = is_present
        
        # Replace the item in the list with the new ordered dictionary
        target_list[index] = ordered_item
        # -------------------------------------------------

    # 3 check_list against found_ids
    for val in check_list:
        if val not in found_ids:
            sys.exit(f"Error (Condition 3): Required rule_id '{val}' not found in the input data.")

    print("--- All Validation Checks Passed ---")

    # -------------------------------------------------
    # 6. Save Final Output
    # -------------------------------------------------
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    final_output = {
        "file_name": filename,
        "timestamp": current_time,
        "llm_model": llm_model_name,
        "smell_analysis": target_list 
    }
    
    try:
        # 'x' mode ensures we don't overwrite, though we check os.path.exists above too.
        with open(full_output_path, 'x', encoding='utf-8') as f:
            json.dump(final_output, f, indent=2)
            print(f"Success: File saved as '{full_output_path}'")
            
    except FileExistsError:
        sys.exit(f"Error (Condition 8): The file '{full_output_path}' already exists.")
    except Exception as e:
        sys.exit(f"Error: Could not save file. {e}")

if __name__ == "__main__":
    main()
