import os
import shutil
import subprocess

def main():
    # Obtener el directorio donde está este script (.agents/scripts/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # La raíz del workspace está dos niveles arriba de .agents/scripts/
    workspace_root = os.path.dirname(os.path.dirname(script_dir))
    
    quarto_dir = os.path.join(workspace_root, 'quarto')
    docs_dir = os.path.join(workspace_root, 'docs')

    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)

    # 1. Compile all presentations using compile_quarto.py
    print("Compiling presentations...")
    subprocess.run(["python", "compile_quarto.py"], cwd=script_dir)

    # 2. Compile step now automatically places HTML in docs/ and cleans up.
    print("\nOrganizing docs/ folder (already done by compiler)...")

    # 3. Create the premium docs/index.html
    index_path = os.path.join(docs_dir, 'index.html')
    
    # Definition of modules and presentations in the correct order
    modules = [
        {
            "title": "Módulo 1: Aprendizaje Supervisado Clásico",
            "items": [
                {
                    "id": "intro_ia",
                    "num": "Clase 01",
                    "title": "Introducción a la IA",
                    "description": "Fundamentos de la IA, aprendizaje supervisado y no supervisado, y conceptos clave de modelado.",
                    "badge": "Introducción",
                    "badge_class": "badge-intro",
                    "icon_class": "icon-gray",
                    "icon_svg": '<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z" /></svg>'
                },
                {
                    "id": "modelos_lineales",
                    "num": "Clase 02",
                    "title": "Modelos Lineales",
                    "description": "Regresión lineal, regresión logística y optimización mediante descenso de gradiente.",
                    "badge": "Supervisado",
                    "badge_class": "badge-tabular",
                    "icon_class": "icon-blue",
                    "icon_svg": '<svg viewBox="0 0 24 24"><path d="M4 19h16v-2H4v2zm0-4h16v-2H4v2zm0-4h16V9H4v2zm0-6v2h16V5H4z"/></svg>'
                },
                {
                    "id": "arboles_decision",
                    "num": "Clase 03",
                    "title": "Árboles de Decisión",
                    "description": "Estructura de árboles de decisión, criterios de división (Gini, Entropía) y regularización.",
                    "badge": "Supervisado",
                    "badge_class": "badge-tabular",
                    "icon_class": "icon-green",
                    "icon_svg": '<svg viewBox="0 0 24 24"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>'
                },
                {
                    "id": "ensambles",
                    "num": "Clase 04",
                    "title": "Métodos de Ensamble",
                    "description": "Combinación de modelos débiles: Bagging, Random Forests y algoritmos de Boosting.",
                    "badge": "Supervisado",
                    "badge_class": "badge-tabular",
                    "icon_class": "icon-purple",
                    "icon_svg": '<svg viewBox="0 0 24 24"><path d="M20 13H4c-1.11 0-2 .89-2 2v4c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2v-4c0-1.11-.89-2-2-2zm-1 5H5v-2h14v2zm1-13H4c-1.11 0-2 .89-2 2v4c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V7c0-1.11-.89-2-2-2zm-1 5H5V8h14v2z"/></svg>'
                },
                {
                    "id": "svm",
                    "num": "Clase 05",
                    "title": "Máquinas de Soporte Vectorial",
                    "description": "Clasificación con margen máximo, truco del kernel y regularización.",
                    "badge": "Supervisado",
                    "badge_class": "badge-tabular",
                    "icon_class": "icon-orange",
                    "icon_svg": '<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm0-4h-2V7h2v8z"/></svg>'
                }
            ]
        },
        {
            "title": "Módulo 2: Aprendizaje No Supervisado",
            "items": [
                {
                    "id": "clustering",
                    "num": "Clase 06",
                    "title": "Clustering / Agrupamiento",
                    "description": "Aprendizaje no supervisado con K-Means, agrupamiento jerárquico y métricas de evaluación.",
                    "badge": "No Supervisado",
                    "badge_class": "badge-intro",
                    "icon_class": "icon-blue",
                    "icon_svg": '<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>'
                }
            ]
        },
        {
            "title": "Módulo 3: Aprendizaje Profundo y Modelos Modernos",
            "items": [
                {
                    "id": "redes_neuronales",
                    "num": "Clase 07",
                    "title": "Redes Neuronales",
                    "description": "Perceptrón multicapa, propagación hacia adelante (forward propagation) y retropropagación (backpropagation).",
                    "badge": "Redes Neuronales",
                    "badge_class": "badge-tabular",
                    "icon_class": "icon-purple",
                    "icon_svg": '<svg viewBox="0 0 24 24"><path d="M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm-2-7v-2H8v2h2zm4 0v-2h-2v2h2zm2-4V9h-2v2h2zm-8 0V9H6v2h2zm4 0V9h-2v2h2z"/></svg>'
                },
                {
                    "id": "aprendizaje_profundo",
                    "num": "Clase 08",
                    "title": "Aprendizaje Profundo",
                    "description": "Fundamentos del Deep Learning, funciones de activación, optimizadores y regularización profunda.",
                    "badge": "Deep Learning",
                    "badge_class": "badge-deep",
                    "icon_class": "icon-blue",
                    "icon_svg": '<svg viewBox="0 0 24 24"><path d="M12 3c-4.97 0-9 4.03-9 9 0 2.12.74 4.07 1.97 5.61L4.35 19.4c-.39.39-.39 1.02 0 1.41.39.39 1.02.39 1.41 0l1.9-1.9C9.17 19.58 10.53 20 12 20c4.97 0 9-4.03 9-9s-4.03-9-9-9zm0 15c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z"/></svg>'
                },
                {
                    "id": "cnn",
                    "num": "Clase 09",
                    "title": "Redes Convolucionales (CNN)",
                    "description": "Procesamiento de imágenes mediante capas convolucionales, pooling y arquitecturas CNN populares.",
                    "badge": "Deep Learning",
                    "badge_class": "badge-deep",
                    "icon_class": "icon-green",
                    "icon_svg": '<svg viewBox="0 0 24 24"><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg>'
                },
                {
                    "id": "llms",
                    "num": "Clase 10",
                    "title": "Modelos de Lenguaje Grandes",
                    "description": "Arquitectura Transformer, autoatención, LLMs y aplicaciones en Procesamiento del Lenguaje Natural.",
                    "badge": "Deep Learning",
                    "badge_class": "badge-deep",
                    "icon_class": "icon-orange",
                    "icon_svg": '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/></svg>'
                }
            ]
        }
    ]

    # Generate grid content HTML
    grid_html = ""
    for module in modules:
        grid_html += f'\n            <h2 class="section-title">{module["title"]}</h2>'
        for item in module["items"]:
            grid_html += f"""
            <div class="card">
                <div class="card-icon-header {item["icon_class"]}">
                    {item["icon_svg"]}
                </div>
                <div class="card-body">
                    <span class="badge {item["badge_class"]}">{item["badge"]}</span>
                    <h3 class="card-title">{item["num"]}: {item["title"]}</h3>
                    <p class="card-text">{item["description"]}</p>
                </div>
                <div class="card-footer">
                    <a href="{item["id"]}.html" class="btn" target="_blank">Ver Presentación</a>
                </div>
            </div>"""

    html_content = f"""<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taller de Machine Learning - Javeriana</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        /* --- Estilos Generales y Tema --- */
        :root {{
            --primary-color: #003576;
            --accent-color: #3498db;
            --bg-color: #f8f9fa;
            --card-bg: #ffffff;
            --text-color: #333;
            --section-header: #003576;
            --shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
            --transition: all 0.3s ease;
        }}

        body {{
            font-family: 'Poppins', sans-serif;
            margin: 0;
            padding: 0;
            background-color: var(--bg-color);
            color: var(--text-color);
        }}

        /* --- Header / Título Principal --- */
        header {{
            background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
            color: white;
            padding: 40px 20px;
            text-align: center;
            margin-bottom: 40px;
            box-shadow: var(--shadow);
        }}

        header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 600;
        }}

        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        /* --- Contenedor Principal (Grid) --- */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px 50px;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }}

        /* --- Tarjetas (Cards) del Menú --- */
        .card {{
            background-color: var(--card-bg);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: var(--transition);
            position: relative;
            display: flex;
            flex-direction: column;
            border: 1px solid #eee;
        }}

        .card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
        }}

        /* Iconos visuales en la parte superior de la tarjeta */
        .card-icon-header {{
            height: 120px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #eef2f7;
        }}

        .card-icon-header svg {{
            width: 60px;
            height: 60px;
            fill: var(--primary-color);
            opacity: 0.8;
        }}

        /* Colores específicos para los iconos */
        .icon-blue {{
            background: #d6eaf8;
        }}
        .icon-blue svg {{
            fill: #3498db;
        }}

        .icon-green {{
            background: #d5f5e3;
        }}
        .icon-green svg {{
            fill: #2ecc71;
        }}

        .icon-purple {{
            background: #e8daef;
        }}
        .icon-purple svg {{
            fill: #8e44ad;
        }}

        .icon-orange {{
            background: #fdebd0;
        }}
        .icon-orange svg {{
            fill: #e67e22;
        }}

        .icon-gray {{
            background: #ebedef;
        }}
        .icon-gray svg {{
            fill: #7f8c8d;
        }}

        /* Contenido de la tarjeta */
        .card-body {{
            padding: 25px;
            flex-grow: 1;
            text-align: center;
        }}

        .card-title {{
            font-size: 1.3em;
            margin: 10px 0;
            color: var(--primary-color);
            font-weight: 600;
        }}

        .card-text {{
            color: #555;
            font-size: 0.95em;
            line-height: 1.6;
        }}

        /* Botones */
        .card-footer {{
            padding: 20px;
            background-color: transparent;
            text-align: center;
        }}

        .btn {{
            display: inline-block;
            padding: 12px 30px;
            background-color: var(--primary-color);
            color: white;
            text-decoration: none;
            border-radius: 30px;
            font-weight: 600;
            transition: var(--transition);
            border: none;
            cursor: pointer;
        }}

        .btn:hover {{
            background-color: #2980b9;
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
        }}

        /* --- Secciones --- */
        .section-title {{
            grid-column: 1 / -1;
            font-size: 1.6rem;
            color: var(--section-header);
            margin-top: 40px;
            margin-bottom: 20px;
            border-bottom: 2px solid #ddd;
            padding-bottom: 10px;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-bottom: 10px;
            color: white;
        }}

        .badge-tabular {{
            background-color: #e67e22;
        }}

        .badge-intro {{
            background-color: #95a5a6;
        }}

        .badge-deep {{
            background-color: #8e44ad;
        }}

        /* Logo Styles */
        .header-content {{
            display: flex;
            align-items: center;
            justify-content: center;
            flex-wrap: wrap;
            gap: 20px;
        }}

        .javeriana-logo {{
            height: 80px;
            width: auto;
            background-color: white;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .header-text {{
            text-align: left;
        }}

        .footer {{
            margin-top: 60px;
            text-align: center;
            color: #7f8c8d;
            padding: 30px 20px;
            border-top: 1px solid #eee;
            background: #fff;
        }}

        @media (max-width: 768px) {{
            .header-text {{
                text-align: center;
            }}
        }}
    </style>
</head>

<body>

    <div class="container">
        <header>
            <div class="header-content">
                <img src="assets/logo_RGB.png" alt="Logo PUJ" class="javeriana-logo">
                <div class="header-text">
                    <h1>Taller de Machine Learning</h1>
                    <p class="subtitle">Pontificia Universidad Javeriana - Facultad de Ingeniería</p>
                </div>
            </div>
            <p style="text-align:center; max-width:800px; margin: 20px auto 0; color:rgba(255,255,255,0.9);">
                Material de clase y presentaciones interactivas del curso, organizado por módulos de aprendizaje.
            </p>
        </header>

        <div class="grid">
            {grid_html}
        </div>

        <div class="footer">
            <p style="font-weight: 600; color: var(--primary-color);">Pontificia Universidad Javeriana - Facultad de Ingeniería</p>
            <p>Generado por la IA Gemini y Oscar Bustos</p>
            <p><small style="color: #95a5a6;">Licenciado bajo Apache License 2.0</small></p>
        </div>
    </div>

</body>

</html>"""

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"Created index page at docs/index.html")
    print("Done! The repository is ready for GitHub Pages (serving from /docs).")

if __name__ == "__main__":
    main()
