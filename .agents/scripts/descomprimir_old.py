import os
import zipfile
import shutil

def extract_zip_files():
    # Use absolute path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    old_dir = os.path.join(script_dir, 'old')
    
    # Create old directory if it doesn't exist
    os.makedirs(old_dir, exist_ok=True)
    
    # 1. Scan root directory for zip files and move them to 'old' directory
    print(f"Scanning root directory for zip files to move to '{old_dir}'...")
    root_zip_files = [f for f in os.listdir(script_dir) if f.lower().endswith('.zip') and f != 'old']
    
    for file in root_zip_files:
        src_path = os.path.join(script_dir, file)
        dest_path = os.path.join(old_dir, file)
        print(f"Moving '{file}' to '{old_dir}'...")
        try:
            shutil.move(src_path, dest_path)
        except Exception as e:
            print(f"Error moving {file}: {e}")

    # 2. Extract ZIP files inside 'old' directory
    print(f"\nScanning directory: {old_dir}")
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
