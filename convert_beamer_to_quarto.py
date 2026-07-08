import os
import re
import sys

def clean_braces(text):
    """Remove outer braces if present."""
    if text.startswith('{') and text.endswith('}'):
        return text[1:-1].strip()
    return text.strip()

def parse_metadata(content):
    """Extract standard presentation metadata."""
    title_match = re.search(r'\\title(?:\[.*?\])?\{((?:[^{}]|\{[^{}]*\})*)\}', content)
    subtitle_match = re.search(r'\\subtitle(?:\[.*?\])?\{((?:[^{}]|\{[^{}]*\})*)\}', content)
    author_match = re.search(r'\\author(?:\[.*?\])?\{((?:[^{}]|\{[^{}]*\})*)\}', content)
    date_match = re.search(r'\\date(?:\[.*?\])?\{((?:[^{}]|\{[^{}]*\})*)\}', content)
    bib_match = re.search(r'\\addbibresource\{([^{}]+)\}', content)

    title = title_match.group(1) if title_match else "Presentation"
    subtitle = subtitle_match.group(1) if subtitle_match else ""
    author = author_match.group(1) if author_match else ""
    date = date_match.group(1) if date_match else ""
    bib = bib_match.group(1) if bib_match else ""

    # Clean LaTeX macros in metadata
    for pattern, repl in [
        (r'\\href\{[^}]*\}\{([^}]*)\}', r'\1'),
        (r'\\url\{([^}]*)\}', r'\1'),
        (r'\\texttt\{([^}]*)\}', r'\1'),
        (r'\\textbf\{([^}]*)\}', r'\1'),
        (r'\\textit\{([^}]*)\}', r'\1'),
    ]:
        title = re.sub(pattern, repl, title)
        subtitle = re.sub(pattern, repl, subtitle)
        author = re.sub(pattern, repl, author)
        date = re.sub(pattern, repl, date)

    return {
        "title": title.strip(),
        "subtitle": subtitle.strip(),
        "author": author.strip(),
        "date": date.strip(),
        "bibliography": bib.strip()
    }

def clean_inline_formatting(line):
    """Replace common LaTeX inline commands with Markdown equivalents."""
    # Handle custom \hrefcol
    line = re.sub(r'\\hrefcol\{([^}]+)\}\{([^}]+)\}', r'[\2](\1)', line)
    
    # Standard \href and \url
    line = re.sub(r'\\href\{([^}]+)\}\{([^}]+)\}', r'[\2](\1)', line)
    line = re.sub(r'\\url\{([^}]+)\}', r'[\1](\1)', line)
    
    # Text formatting (run multiple times to handle nesting)
    for _ in range(5):
        line = re.sub(r'\\textbf\{([^{}]+)\}', r'**\1**', line)
        line = re.sub(r'\\textit\{([^{}]+)\}', r'*\1*', line)
        line = re.sub(r'\\texttt\{([^{}]+)\}', r'`\1`', line)
        line = re.sub(r'\\emph\{([^{}]+)\}', r'*\1*', line)

    # Citations
    line = re.sub(r'\\cite\{([^}]+)\}', r'[@\1]', line)

    # Convert \pause to . . .
    line = re.sub(r'\\pause\b', '\n. . .\n', line)

    # Strip formatting tags/commands
    line = re.sub(r'\\centering\b', '', line)
    line = re.sub(r'\\hfill\b', ' ', line)
    line = re.sub(r'\\small\b', '', line)
    line = re.sub(r'\\large\b', '', line)
    line = re.sub(r'\\Large\b', '', line)
    line = re.sub(r'\\scriptsize\b', '', line)
    line = re.sub(r'\\tiny\b', '', line)
    line = re.sub(r'\\bfseries\b', '', line)
    line = re.sub(r'\\itshape\b', '', line)
    
    # Handle vspace
    line = re.sub(r'\\vspace\*?\{[^}]*\}', '\n', line)

    # Image adjustments: \includegraphics[options]{path}
    img_match = re.search(r'\\includegraphics\[([^\]]*)\]\{([^}]+)\}', line)
    if img_match:
        options = img_match.group(1)
        path = img_match.group(2)
        
        # Determine width percentage
        width_pct = "100%"
        width_match = re.search(r'width\s*=\s*(0\.\d+|1)?\s*\\textwidth', options)
        if width_match:
            val = width_match.group(1)
            if val:
                width_pct = f"{int(float(val) * 100)}%"
        else:
            # Check for general width
            width_match_any = re.search(r'width\s*=\s*([^,\s]+)', options)
            if width_match_any:
                width_val = width_match_any.group(1)
                if '\\' in width_val: # e.g. 0.5\linewidth
                    num_match = re.match(r'(0\.\d+|1)?', width_val)
                    if num_match and num_match.group(1):
                        width_pct = f"{int(float(num_match.group(1)) * 100)}%"
        
        line = re.sub(r'\\includegraphics\[[^\]]*\]\{[^}]+\}', f'![]({path}){{width="{width_pct}"}}', line)

    return line

def convert_latex_to_qmd(content):
    """Parse Beamer LaTeX and convert it to Quarto Reveal.js QMD."""
    # Pre-process content globally for multiline graphics and maketitle removal
    content = re.sub(r'\\maketitle\b', '', content)
    
    # Match \includegraphics[options]{path} potentially spanning newlines
    img_pattern = r'\\includegraphics\s*(?:\[([^\]]*)\])?\s*\{([^}]+)\}'
    def replace_img(match):
        options = match.group(1) or ""
        path = match.group(2).strip().replace('\n', '').replace('\r', '')
        
        # Determine width percentage
        width_pct = "100%"
        if options:
            width_match = re.search(r'width\s*=\s*(0\.\d+|1)?\s*\\textwidth', options)
            if width_match:
                val = width_match.group(1)
                if val:
                    width_pct = f"{int(float(val) * 100)}%"
            else:
                width_match_any = re.search(r'width\s*=\s*([^,\s\]\n]+)', options)
                if width_match_any:
                    width_val = width_match_any.group(1)
                    if '\\' in width_val: # e.g. 0.5\linewidth or \textwidth
                        num_match = re.match(r'(0\.\d+|1)?', width_val)
                        if num_match and num_match.group(1):
                            width_pct = f"{int(float(num_match.group(1)) * 100)}%"
        return f'![]({path}){{width="{width_pct}"}}'
    
    content = re.sub(img_pattern, replace_img, content, flags=re.DOTALL)
    
    metadata = parse_metadata(content)
    
    # YAML Front Matter
    qmd_lines = [
        "---",
        f'title: "{metadata["title"]}"',
    ]
    if metadata["subtitle"]:
        qmd_lines.append(f'subtitle: "{metadata["subtitle"]}"')
    if metadata["author"]:
        qmd_lines.append(f'author: "{metadata["author"]}"')
    if metadata["date"]:
        qmd_lines.append(f'date: "{metadata["date"]}"')
    
    # Add slide formatting defaults
    qmd_lines.extend([
        "format:",
        "  revealjs:",
        "    theme: default",
        "    slide-number: true",
        "    show-slide-number: all",
        "    transition: slide",
        "    chalkboard: true",
        "    width: 1050",
        "    height: 700",
    ])
    
    if metadata["bibliography"]:
        qmd_lines.append(f'bibliography: {metadata["bibliography"]}')
        
    qmd_lines.append("---\n")

    # Environment stacks and status trackers
    env_stack = []
    in_document = False
    column_open = False
    
    # Process line by line
    raw_lines = content.splitlines()
    i = 0
    while i < len(raw_lines):
        line = raw_lines[i].strip()
        
        # Skip commented lines entirely
        if line.startswith('%'):
            i += 1
            continue

        # Document structure check
        if '\\begin{document}' in line:
            in_document = True
            i += 1
            continue
        if '\\end{document}' in line:
            in_document = False
            break

        if not in_document:
            i += 1
            continue

        # Handle Sections
        section_match = re.match(r'\\section\{([^}]+)\}', line)
        if section_match:
            sec_title = section_match.group(1)
            qmd_lines.append(f"\n# {sec_title}\n")
            i += 1
            continue

        # Handle Subsections
        subsection_match = re.match(r'\\subsection\{([^}]+)\}', line)
        if subsection_match:
            subsec_title = subsection_match.group(1)
            qmd_lines.append(f"\n## {subsec_title}\n")
            i += 1
            continue

        # Handle Frames
        frame_match = re.match(r'\\begin\{frame\}(?:\[.*?\])?(?:\{([^}]*)\})?', line)
        if frame_match:
            env_stack.append('frame')
            title = frame_match.group(1) or ""
            # Look ahead for \frametitle if title is empty
            if not title and i + 1 < len(raw_lines):
                next_line = raw_lines[i+1].strip()
                ft_match = re.match(r'\\frametitle\{([^}]+)\}', next_line)
                if ft_match:
                    title = ft_match.group(1)
                    i += 1  # Skip the next line as we consumed it
            
            qmd_lines.append(f"\n## {title}\n")
            i += 1
            continue

        if '\\end{frame}' in line:
            if 'frame' in env_stack:
                env_stack.remove('frame')
            # Close columns if any are still open
            if column_open:
                qmd_lines.append(":::")
                column_open = False
            if 'columns' in env_stack:
                qmd_lines.append("::::")
                env_stack.remove('columns')
            qmd_lines.append("\n")
            i += 1
            continue

        # Handle Columns Container
        if '\\begin{columns}' in line:
            env_stack.append('columns')
            qmd_lines.append("\n:::: {.columns}\n")
            i += 1
            continue

        if '\\end{columns}' in line:
            if column_open:
                qmd_lines.append(":::")
                column_open = False
            if 'columns' in env_stack:
                env_stack.remove('columns')
            qmd_lines.append("::::\n")
            i += 1
            continue

        # Handle Column elements
        col_begin_match = re.match(r'\\begin\{column\}(?:\[.*?\])?\{([^}]+)\}', line)
        col_direct_match = re.match(r'\\column\{([^}]+)\}', line)
        
        if col_begin_match or col_direct_match:
            width_expr = col_begin_match.group(1) if col_begin_match else col_direct_match.group(1)
            # Parse width (e.g. 0.5\textwidth)
            width_pct = "50%"
            width_num_match = re.match(r'(0\.\d+|1)?', width_expr)
            if width_num_match and width_num_match.group(1):
                width_pct = f"{int(float(width_num_match.group(1)) * 100)}%"
            
            if column_open:
                qmd_lines.append(":::")
            
            qmd_lines.append(f"\n::: {{.column width=\"{width_pct}\"}}")
            column_open = True
            
            if col_begin_match:
                env_stack.append('column')
            i += 1
            continue

        if '\\end{column}' in line:
            if 'column' in env_stack:
                env_stack.remove('column')
            qmd_lines.append(":::\n")
            column_open = False
            i += 1
            continue

        # Handle Lists (itemize/enumerate)
        if '\\begin{itemize}' in line:
            env_stack.append('itemize')
            i += 1
            continue
        if '\\end{itemize}' in line:
            if 'itemize' in env_stack:
                env_stack.remove('itemize')
            i += 1
            continue
        if '\\begin{enumerate}' in line:
            env_stack.append('enumerate')
            i += 1
            continue
        if '\\end{enumerate}' in line:
            if 'enumerate' in env_stack:
                env_stack.remove('enumerate')
            i += 1
            continue

        if line.startswith('\\item'):
            # Calculate nesting depth based on list environments in stack
            list_envs = [e for e in env_stack if e in ('itemize', 'enumerate')]
            depth = len(list_envs)
            indent = "  " * max(0, depth - 1)
            
            item_text = line[len('\\item'):].strip()
            # Clean item text inline formatting
            item_text = clean_inline_formatting(item_text)
            
            list_type = list_envs[-1] if list_envs else 'itemize'
            bullet = "1. " if list_type == 'enumerate' else "- "
            
            qmd_lines.append(f"{indent}{bullet}{item_text}")
            i += 1
            continue

        # Handle Callout blocks (theorem, definition, block, alertblock, exampleblock)
        block_match = re.match(r'\\begin\{(block|alertblock|exampleblock|definition|theorem|example)\}(?:\{([^}]*)\})?', line)
        if block_match:
            block_type = block_match.group(1)
            block_title = block_match.group(2) or block_type.capitalize()
            env_stack.append('block')
            
            # Map type to Quarto callout type
            callout_class = "note"
            if block_type in ('alertblock', 'theorem'):
                callout_class = "important"
            elif block_type in ('exampleblock', 'example', 'definition'):
                callout_class = "tip"
                
            qmd_lines.append(f"\n::: {{.callout-{callout_class}}}")
            qmd_lines.append(f"## {block_title}")
            i += 1
            continue

        if any(f'\\end{{{b}}}' in line for b in ('block', 'alertblock', 'exampleblock', 'definition', 'theorem', 'example')):
            if 'block' in env_stack:
                env_stack.remove('block')
            qmd_lines.append(":::\n")
            i += 1
            continue

        # Handle Tabular (Tables)
        if '\\begin{tabular}' in line:
            table_lines = []
            i += 1
            while i < len(raw_lines) and '\\end{tabular}' not in raw_lines[i]:
                t_line = raw_lines[i].strip()
                # Strip \hline
                t_line = t_line.replace(r'\hline', '').strip()
                if t_line:
                    table_lines.append(t_line)
                i += 1
            
            # Parse tabular content
            if table_lines:
                markdown_table = []
                for row_idx, t_row in enumerate(table_lines):
                    # Remove trailing LaTeX newline \\
                    t_row_clean = re.sub(r'\\\\.*$', '', t_row).strip()
                    if not t_row_clean:
                        continue
                    
                    # Split cells by &
                    cells = [clean_inline_formatting(c.strip()) for c in t_row_clean.split('&')]
                    markdown_row = "| " + " | ".join(cells) + " |"
                    markdown_table.append(markdown_row)
                    
                    # Insert header divider after first row
                    if row_idx == 0:
                        divs = ["---"] * len(cells)
                        markdown_table.append("| " + " | ".join(divs) + " |")
                        
                qmd_lines.append("\n" + "\n".join(markdown_table) + "\n")
            
            i += 1  # Skip the \end{tabular}
            continue

        # Standard lines (non-structural)
        cleaned_line = clean_inline_formatting(line)
        
        # Check list depth for normal paragraphs inside lists to keep indentation alignment
        list_envs = [e for e in env_stack if e in ('itemize', 'enumerate')]
        if list_envs and cleaned_line:
            depth = len(list_envs)
            indent = "  " * depth
            qmd_lines.append(f"{indent}{cleaned_line}")
        else:
            if cleaned_line:
                qmd_lines.append(cleaned_line)
            else:
                qmd_lines.append("") # keep empty line for spacing

        i += 1

    return "\n".join(qmd_lines)

import shutil

FOLDER_MAPPING = {
    "Sesión_1___Intro_IA (1)": "sesion_1_intro_ia",
    "Sesión_2___Modelos_Lineales": "sesion_2_modelos_lineales",
    "Sesión_3___Máquinas_de_Vectores_de_Soporte": "sesion_3_svm",
    "Sesión_4___Árboles_de_Decisión": "sesion_4_arboles_decision",
    "Sesión_5___Ensambles": "sesion_5_ensambles",
    "Sesión_6___Redes_Neuronales (1)": "sesion_6_redes_neuronales",
    "Sesión_7___Aprendizaje_Profundo": "sesion_7_aprendizaje_profundo",
    "Sesión_8___LLM_y_modelos_Pre_entrenados": "sesion_8_llms",
    "Sesión_9___Clustering": "sesion_9_clustering",
    "Sesión___Redes_Neuronales_Convolucionales (1)": "sesion_cnn"
}

def process_directory(directory_path):
    """Find all javeriana.tex (or any .tex) files, convert them, and copy resources to a quarto folder."""
    print(f"Scanning directory: {directory_path}")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    quarto_root = os.path.join(script_dir, 'quarto')
    
    # Delete existing quarto directory for a clean slate
    if os.path.exists(quarto_root):
        print(f"Cleaning existing directory: {quarto_root}")
        shutil.rmtree(quarto_root, ignore_errors=True)
        
    os.makedirs(quarto_root, exist_ok=True)
    
    converted_count = 0
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.tex'):
                tex_path = os.path.join(root, file)
                
                # Get the relative path of the directory containing the .tex file from the directory_path
                rel_dir = os.path.relpath(root, directory_path)
                
                # Semantic mapping
                clean_rel_dir = FOLDER_MAPPING.get(rel_dir, rel_dir)
                
                # Destination directory inside quarto
                dest_dir = os.path.join(quarto_root, clean_rel_dir)
                os.makedirs(dest_dir, exist_ok=True)
                
                qmd_name = os.path.splitext(file)[0] + '.qmd'
                if file == 'javeriana.tex':
                    qmd_name = 'index.qmd'
                
                qmd_path = os.path.join(dest_dir, qmd_name)
                print(f"Converting '{tex_path}' -> '{qmd_path}'...")
                
                try:
                    with open(tex_path, 'r', encoding='utf-8', errors='ignore') as f:
                        tex_content = f.read()
                    
                    qmd_content = convert_latex_to_qmd(tex_content)
                    
                    with open(qmd_path, 'w', encoding='utf-8') as f:
                        f.write(qmd_content)
                        
                    print("-> Successfully converted.")
                    converted_count += 1
                    
                    # Copy other files and directories (like assets, references.bib)
                    for item in os.listdir(root):
                        if item.endswith('.tex') or item == qmd_name or item == 'index.qmd':
                            continue
                        
                        src_item = os.path.join(root, item)
                        dest_item = os.path.join(dest_dir, item)
                        
                        if os.path.isdir(src_item):
                            if os.path.exists(dest_item):
                                shutil.rmtree(dest_item)
                            shutil.copytree(src_item, dest_item)
                        else:
                            shutil.copy2(src_item, dest_item)
                    print(f"-> Resources copied to '{dest_dir}'.")
                            
                except Exception as e:
                    print(f"-> Error converting '{tex_path}': {e}")
                    
    print(f"\nFinished. Converted {converted_count} files into '{quarto_root}'.")

if __name__ == '__main__':
    # Default to scanning 'old' directory if no arguments passed
    target_dir = sys.argv[1] if len(sys.argv) > 1 else 'old'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    abs_target_dir = os.path.join(script_dir, target_dir) if not os.path.isabs(target_dir) else target_dir
    
    process_directory(abs_target_dir)
