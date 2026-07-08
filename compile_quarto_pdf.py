import os
import subprocess
import sys
import argparse

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

def compile_all(output_format="typst"):
    quarto_bin = find_quarto()
    if not quarto_bin:
        print("Error: Quarto is not installed or could not be found.")
        print("Please download and install Quarto from: https://quarto.org/docs/get-started/")
        sys.exit(1)
        
    print(f"Using Quarto binary: {quarto_bin}")
    print(f"Target format: {output_format}")
    
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
                print(f"Compiling: {qmd_path} to PDF (via {output_format})")
                print(f"==================================================")
                
                try:
                    # Run quarto render inside the directory of the qmd file so relative paths resolve correctly
                    result = subprocess.run(
                        [quarto_bin, "render", file, "--to", output_format],
                        cwd=root,
                        shell=True
                    )
                    if result.returncode == 0:
                        print("-> Successfully compiled to PDF.")
                        compiled_count += 1
                    else:
                        print(f"-> Error: Quarto exited with code {result.returncode}")
                        if output_format == "pdf" and "No TeX installation was detected" in getattr(result, "stderr", b"").decode(errors="ignore"):
                            print("   Suggestion: Try running with '--format typst' which does not require a TeX installation.")
                except Exception as e:
                    print(f"-> Exception occurred: {e}")
                    
    print(f"\nCompilation process finished. Compiled {compiled_count} presentations to PDF.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compile Quarto slides to PDF.")
    parser.add_argument(
        "--format", 
        choices=["typst", "pdf", "beamer"], 
        default="typst",
        help="The engine/format used to generate the PDF. 'typst' is recommended as it has no external dependencies (does not require LaTeX)."
    )
    args = parser.parse_args()
    
    compile_all(args.format)
