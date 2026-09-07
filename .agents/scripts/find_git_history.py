import subprocess

res = subprocess.run(
    ["git", "show", "c1f401630414f9ad4462f57b1a995100694e6a3d~1:quarto/clustering/index.qmd"],
    capture_output=True,
    text=True,
    encoding="utf-8"
)

with open(r"c:\Users\olbus\Git\Javeriana\javeriana-tallerml-slides\.agents\previous_clustering_index.qmd", "w", encoding="utf-8") as f:
    f.write(res.stdout)

print(f"Written previous index.qmd: {len(res.stdout)} chars")

# Search in previous_clustering_index.qmd
for line in res.stdout.splitlines():
    if any(w in line.lower() for w in ["arbol", "árbol", "tree", "interpretar", "sustituto", "surrogate"]):
        print("MATCH:", line)
