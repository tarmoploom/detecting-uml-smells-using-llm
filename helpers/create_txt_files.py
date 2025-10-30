import os

# source folder containing .xmi files
source_folder = '/path/to/your/source_folder'
# destination folder for new .txt files
destination_folder = '/path/to/your/destination_folder'

# Create destination folder
os.makedirs(destination_folder, exist_ok=True)

# Loop files ending with .xmi
for filename in os.listdir(source_folder):
    if filename.endswith('.xmi'):
        new_filename = os.path.splitext(filename)[0] + '.txt'
        # Full path for new file
        new_file_path = os.path.join(destination_folder, new_filename)
        # Create empty .txt file
        with open(new_file_path, 'w') as f:
            pass
