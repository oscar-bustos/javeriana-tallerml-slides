import os
import shutil

# Semantic mapping of old folder names to compact Git-friendly names without session numbers
FOLDER_MAP = {
    "Sesión_1___Intro_IA (1)": "intro_ia",
    "Sesión_2___Modelos_Lineales": "modelos_lineales",
    "Sesión_3___Máquinas_de_Vectores_de_Soporte": "svm",
    "Sesión_4___Árboles_de_Decisión": "arboles_decision",
    "Sesión_5___Ensambles": "ensambles",
    "Sesión_6___Redes_Neuronales (1)": "redes_neuronales",
    "Sesión_7___Aprendizaje_Profundo": "aprendizaje_profundo",
    "Sesión_8___LLM_y_modelos_Pre_entrenados": "llms",
    "Sesión_9___Clustering": "clustering",
    "Sesión___Redes_Neuronales_Convolucionales (1)": "cnn"
}

def organize():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    quarto_root = os.path.join(script_dir, 'quarto')
    
    if not os.path.exists(quarto_root):
        print(f"Error: quarto directory not found at {quarto_root}")
        return
        
    print(f"Organizing folders in: {quarto_root}\n")
    for old_name, new_name in FOLDER_MAP.items():
        old_path = os.path.join(quarto_root, old_name)
        new_path = os.path.join(quarto_root, new_name)
        
        if os.path.exists(old_path):
            print(f"Renaming '{old_name}' -> '{new_name}'...")
            # Delete destination if it already exists to avoid errors
            if os.path.exists(new_path):
                shutil.rmtree(new_path)
            shutil.move(old_path, new_path)
        else:
            print(f"Folder '{old_name}' not found (already renamed or doesn't exist).")
            
    print("\nFinished organizing folders.")

if __name__ == '__main__':
    organize()
