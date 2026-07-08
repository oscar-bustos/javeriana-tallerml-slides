import os
import zipfile

def extract_zip_files():
    # Use absolute path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    old_dir = os.path.join(script_dir, 'old')
    
    if not os.path.exists(old_dir):
        print(f"Error: Directory '{old_dir}' does not exist.")
        return

    print(f"Scanning directory: {old_dir}")
    zip_files = [f for f in os.listdir(old_dir) if f.lower().endswith('.zip')]
    
    if not zip_files:
        print("No .zip files found in the 'old' directory.")
        return

    print(f"Found {len(zip_files)} zip file(s) to extract.\n")
    
    for file in zip_files:
        file_path = os.path.join(old_dir, file)
        # Create a directory with the same name as the ZIP (minus .zip)
        extract_folder_name = os.path.splitext(file)[0]
        extract_path = os.path.join(old_dir, extract_folder_name)
        
        print(f"Extracting '{file}' to '{extract_folder_name}'...")
        try:
            os.makedirs(extract_path, exist_ok=True)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            print(f"-> Successfully extracted.\n")
        except Exception as e:
            print(f"-> Error extracting {file}: {e}\n")

if __name__ == '__main__':
    extract_zip_files()
