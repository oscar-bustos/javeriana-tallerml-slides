import os
import re

def configure_all_qmd():
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
                
                parts = content.split('---', 2)
                if len(parts) < 3:
                    continue
                    
                frontmatter = parts[1]
                body = parts[2]
                
                original_frontmatter = frontmatter
                
                frontmatter = re.sub(r'(?m)^theme:\s*default', '    theme: default', frontmatter)
                
                revealjs_match = re.search(r'revealjs:(.*?)(?=\n\S|\n---)', frontmatter, re.DOTALL)
                if revealjs_match:
                    inner_content = revealjs_match.group(1)
                    lines = [line.strip() for line in inner_content.split('\n') if line.strip()]
                    
                    # Ensure embed-resources: true
                    if 'embed-resources: true' not in lines:
                        lines.insert(0, 'embed-resources: true')
                        
                    # Revert width and height, remove smaller: true
                    new_lines = []
                    for line in lines:
                        if line.startswith('smaller: true'):
                            continue
                        elif line.startswith('width:'):
                            new_lines.append('width: 1050')
                        elif line.startswith('height:'):
                            new_lines.append('height: 700')
                        else:
                            new_lines.append(line)
                            
                    new_revealjs_block = 'revealjs:\n' + '\n'.join(f'    {line}' for line in new_lines)
                    frontmatter = frontmatter.replace(f"revealjs:{revealjs_match.group(1)}", new_revealjs_block)
                
                if frontmatter != original_frontmatter:
                    new_content = f"---{frontmatter}---{body}"
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated settings for: {file_path}")
                    updated_files += 1
                else:
                    print(f"Already configured: {file_path}")
                        
    print(f"\nConfiguration updates finished. Updated {updated_files} files.")

if __name__ == '__main__':
    configure_all_qmd()
