from pathlib import Path

# ==========================================
# SETTINGS
# ==========================================

# 1. path to folder containing files
target_folder = "/path/to/your/target_folder" 

# 2. name of the file to save
result_file = "file_list.txt"

# exclusions = "Hoonete_typoloogia, Kaubad_turuplatsil, Kobarkino, Kultuurireisid, Labor, Lennufirma, Myygid, Padel, Tarkvaraarenduse_tellimused, Tooaeg"


def list_file_names(folder_path, output_file_name, ext_type='.pdf'):
    source_folder = Path(folder_path)
    output_file = Path(output_file_name)

    if not source_folder.exists():
        print(f"Error: The folder '{source_folder}' does not exist.")
        return

    collected_names = []
    try:
        count = 0
        # iterate over ALL files in the directory
        for file_path in source_folder.iterdir():
            # Check if it is a file (not a folder) AND if extension is ext_type
            if file_path.is_file() and file_path.suffix.lower() == ext_type:
                    
                # .stem gets the name without extension
                name_only = file_path.stem

                # Check if this name is in our exclusion list
                # if name_only in exclusions:
                #     continue

                collected_names.append(name_only)

        # 2. Sort the collected names (A-Z)
        collected_names.sort() 

        # 3. Write sorted names to the file
        with open(output_file, 'w', encoding='utf-8') as f:
            for name in collected_names:
                f.write(name + '\n')
                count += 1
                    
        
        print(f"Success! Found {count} {ext_type} files.")
        print(f"List saved to: {output_file.absolute()}")

    except Exception as e:
        print(f"An error occurred: {e}")



# Run the function
if __name__ == "__main__":
    list_file_names(target_folder, result_file)
