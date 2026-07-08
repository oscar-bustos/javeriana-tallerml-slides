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

def compile_all():
    quarto_bin = find_quarto()
    if not quarto_bin:
        print("Error: Quarto is not installed or could not be found.")
        print("Please download and install Quarto from: https://quarto.org/docs/get-started/")
        print("If already installed, make sure it is added to your system environment variables (PATH) or restart your editor/terminal.")
        sys.exit(1)
        
    print(f"Using Quarto binary: {quarto_bin}")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    quarto_root = os.path.join(script_dir, 'quarto')
    
    if not os.path.exists(quarto_root):
        print(f"Error: Directory '{quarto_root}' does not exist. Please run the conversion script first.")
        sys.exit(1)
        
    compiled_count = 0
    for root, dirs, files in os.walk(quarto_root):
        for file in files:
            if file.endswith('.qmd'):
                qmd_path = os.path.join(root, file)
                print(f"\n==================================================")
                print(f"Compiling: {qmd_path}")
                print(f"==================================================")
                
                try:
                    # Run quarto render inside the directory of the qmd file so relative paths resolve correctly
                    # Use shell=True to support .cmd wrappers and PATH resolution on Windows
                    result = subprocess.run(
                        [quarto_bin, "render", file],
                        cwd=root,
                        shell=True
                    )
                    if result.returncode == 0:
                        print("-> Successfully compiled.")
                        compiled_count += 1
                    else:
                        print(f"-> Error: Quarto exited with code {result.returncode}")
                except Exception as e:
                    print(f"-> Exception occurred: {e}")
                    
    print(f"\nCompilation process finished. Compiled {compiled_count} presentations.")

if __name__ == '__main__':
    compile_all()
