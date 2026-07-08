import os
import re

def remove_backslashes():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    quarto_root = os.path.join(script_dir, 'quarto')
    
    if not os.path.exists(quarto_root):
        print(f"Error: Directory '{quarto_root}' does not exist.")
        return
        
    updated_files = 0
    
    for root, dirs, files in os.walk(quarto_root):
        for file in files:
            if file.endswith('.qmd'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace \\ at the end of a line (or with spaces around it) with a simple markdown line break <br> or just remove it if on its own line
                
                # If it's a line with just \\
                new_content = re.sub(r'(?m)^\s*\\\\s*$', '', content)
                # If it's at the end of a line (like after an image)
                new_content = re.sub(r'(?m)\s*\\\\\s*$', '<br>', new_content)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Cleaned backslashes in: {file_path}")
                    updated_files += 1
                        
    print(f"\nCleanup finished. Fixed {updated_files} files.")

if __name__ == '__main__':
    remove_backslashes()
