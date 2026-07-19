---
name: Compile Presentation
description: Triggers when the user asks to compile, build, render, or generate the current presentation or file.
---

When this skill is triggered, you must follow these instructions:
1. Locate the currently active document from the `ADDITIONAL_METADATA` (`Active Document`).
2. Verify if the active document is a `.qmd` file.
3. If it is a `.qmd` file:
   - Run the compilation script from the workspace root targeting only this file:
     - `CommandLine`: `python .agents/scripts/compile_quarto.py "<absolute_path_to_active_document>"`
     - `Cwd`: Workspace root (`c:\Users\olbus\Git\Javeriana\javeriana-tallerml-slides`)
   - If the user denies the command or it fails due to permissions, print the exact command they can run in their own terminal:
     `python .agents/scripts/compile_quarto.py "<relative_path_to_active_document>"`
4. If no `.qmd` file is active:
   - Politely ask the user which file they would like to compile, and mention that you can run `python .agents/scripts/compile_quarto.py` to compile all slides in the workspace.
