import os
import subprocess
import sys

def find_quarto():
    """Locate the Quarto binary on the system."""
    # Check if quarto is in PATH
    try:
        result = subprocess.run(["quarto", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if result.returncode == 0:
            return "quarto"
    except Exception:
        pass
    
    # Check common Windows installation paths
    common_paths = [
        r"C:\Program Files\Quarto\bin\quarto.exe",
        r"C:\Program Files\Quarto\bin\quarto.cmd",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Quarto\bin\quarto.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Quarto\bin\quarto.cmd"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Programs\Quarto\bin\quarto.exe"),
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
            
    return None

def compile_file(file_path, quarto_bin):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return False
        
    file_abs = os.path.abspath(file_path)
    file_dir = os.path.dirname(file_abs)
    file_name = os.path.basename(file_abs)
    
    print(f"\n==================================================")
    print(f"Compiling: {file_abs}")
    print(f"==================================================")
    
    try:
        # Run quarto render inside the directory of the qmd file so relative paths resolve correctly
        # Use shell=True to support .cmd wrappers and PATH resolution on Windows
        result = subprocess.run(
            [quarto_bin, "render", file_name],
            cwd=file_dir,
            shell=True
        )
        if result.returncode == 0:
            print("-> Successfully compiled.")
            
            # Reubicar el HTML compilado a la carpeta docs/ y limpiar el temporal local
            dir_name = os.path.basename(file_dir)
            workspace_root = os.path.dirname(os.path.dirname(file_dir))
            docs_dir = os.path.join(workspace_root, 'docs')
            
            if not os.path.exists(docs_dir):
                os.makedirs(docs_dir)
                
            local_html = os.path.join(file_dir, 'index.html')
            if os.path.exists(local_html):
                dest_file = os.path.join(docs_dir, f"{dir_name}.html")
                import shutil
                import time
                
                max_retries = 10
                for attempt in range(max_retries):
                    try:
                        shutil.copy2(local_html, dest_file)
                        os.remove(local_html)
                        print(f"-> Output HTML moved to: docs/{dir_name}.html")
                        break
                    except Exception as e:
                        if attempt == max_retries - 1:
                            print(f"-> Failed to move file: {e}")
                            return False
                        time.sleep(0.5)
                
            return True
        else:
            print(f"-> Error: Quarto exited with code {result.returncode}")
            return False
    except Exception as e:
        print(f"-> Exception occurred: {e}")
        return False

def compile_all(quarto_bin):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(os.path.dirname(script_dir))
    quarto_root = os.path.join(workspace_root, 'quarto')
    
    if not os.path.exists(quarto_root):
        print(f"Error: Directory '{quarto_root}' does not exist. Please run the conversion script first.")
        sys.exit(1)
        
    compiled_count = 0
    for root, dirs, files in os.walk(quarto_root):
        for file in files:
            if file.endswith('.qmd'):
                qmd_path = os.path.join(root, file)
                if compile_file(qmd_path, quarto_bin):
                    compiled_count += 1
                    
    print(f"\nCompilation process finished. Compiled {compiled_count} presentations.")

if __name__ == '__main__':
    quarto_bin = find_quarto()
    if not quarto_bin:
        print("Error: Quarto is not installed or could not be found.")
        print("Please download and install Quarto from: https://quarto.org/docs/get-started/")
        print("If already installed, make sure it is added to your system environment variables (PATH) or restart your editor/terminal.")
        sys.exit(1)
        
    print(f"Using Quarto binary: {quarto_bin}")
    
    if len(sys.argv) > 1:
        target = sys.argv[1]
        success = compile_file(target, quarto_bin)
        sys.exit(0 if success else 1)
    else:
        compile_all(quarto_bin)
