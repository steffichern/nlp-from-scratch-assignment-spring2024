import os

def remove_nul_characters(input_dir):
    # Iterate through all files in the specified directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"): # Check if the file is a .txt file
            file_path = os.path.join(input_dir, filename)
            # Open the file, read the contents and remove NUL characters
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                file_content = file.read()
                clean_content = file_content.replace('\x00', '')

            # Write the clean content back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(clean_content)
            print(f'Processed {filename}')

# Specify the directory containing your text files
input_dir = "./data/faculty_papers/"
remove_nul_characters(input_dir)