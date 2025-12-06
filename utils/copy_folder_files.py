import os
import shutil

# ==========================================
# CONFIGURATION: Copies files + adds prefix
# ==========================================

# Path to the folder containing your files
target_folder = "/path/to/your/target_folder" 

# The prefix you want to add
prefix_to_add = "s_"

# SAFETY SWITCH: 
# Set to True to ONLY print what would happen.
# Set to False to ACTUALLY copy the files.
dry_run = True

# ==========================================
# LOGIC
# ==========================================

def main():
    # 1. Check if directory exists
    if not os.path.exists(target_folder):
        print(f"Error: Directory not found: {target_folder}")
        return

    print(f"--- Processing folder: {target_folder} ---")
    if dry_run:
        print("!!! DRY RUN MODE: No files will be created !!!")
    else:
        print("!!! LIVE MODE: Creating copies with new names !!!")
    print("-" * 40)

    count_copied = 0
    
    # 2. Iterate over files
    for filename in os.listdir(target_folder):
        
        # Construct full path
        old_path = os.path.join(target_folder, filename)

        # Skip if it's a directory
        if not os.path.isfile(old_path):
            continue

        # 3. Check Conditions
        # Condition A: Does it start with the prefix already?
        if filename.startswith(prefix_to_add):
            continue

        # Condition B: Does it start with a number? (01.pdf, 02.txt)
        if filename[0].isdigit():
            
            new_filename = f"{prefix_to_add}{filename}"
            new_path = os.path.join(target_folder, new_filename)

            if dry_run:
                print(f"[Preview Copy] '{filename}'  -->  '{new_filename}'")
            else:
                try:
                    # copy2 preserves file metadata (timestamps, etc.)
                    shutil.copy2(old_path, new_path)
                    print(f"[Success Copy] '{filename}'  -->  '{new_filename}'")
                except OSError as e:
                    print(f"[Error] Could not copy '{filename}': {e}")

            count_copied += 1
        else:
            # Ignored files (readme.txt, script.py, etc.)
            pass

    print("-" * 40)
    if dry_run:
        print(f"Process complete. {count_copied} files WOULD be copied.")
    else:
        print(f"Process complete. {count_copied} new files created.")

if __name__ == "__main__":
    main()
