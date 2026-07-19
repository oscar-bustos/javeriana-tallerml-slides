import os
import shutil

FOLDER_MAP = {
    "sesion_1_comprension_datos": "comprension_datos",
    "sesion_2_limpieza_datos": "limpieza_datos",
    "sesion_3_vista_minable": "vista_minable",
    "sesion_4_extraccion_datos_tabular": "extraccion_datos_tabular",
    "sesion_5_fuentes_jerarquicas": "fuentes_jerarquicas",
    "sesion_6_big_data_sin_estructura": "big_data_sin_estructura",
    "sesion_7_big_data_grandes_volumenes": "big_data_grandes_volumenes",
    # Also support raw names just in case
    "Sesión_1___Comprensión_de_los_datos": "comprension_datos",
    "Sesión_2___Limpieza_de_Datos (2)": "limpieza_datos",
    "Sesión_3___Vista_Minable": "vista_minable",
    "Sesión_4___Extracción_de_Información_Data_Tabular": "extraccion_datos_tabular",
    "Sesión_5__Fuentes_Jerarquicas": "fuentes_jerarquicas",
    "Sesión_6___Big_Data___Información_Sin_Estructura": "big_data_sin_estructura",
    "Sesión_7___Big_Data___Grandes_Volúmenes (1)": "big_data_grandes_volumenes"
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
            # Only print if they are not already clean, to avoid spamming already-done messages
            pass
            
    print("\nFinished organizing folders.")

if __name__ == '__main__':
    organize()
