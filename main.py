import tkinter as tk
from tkinter import filedialog, PhotoImage, messagebox

# Taille de la grille et des assets
CELL_SIZE = 64
ROWS, COLS = 10, 15  # Ajuste selon besoin

# Grille initiale vide
grid = [["0" for _ in range(COLS)] for _ in range(ROWS)]

# Dictionnaire des images chargées
images = {}
char_to_asset = {}

# Fonction pour demander les chemins des assets
def ask_asset_paths():
    """Demande à l'utilisateur de choisir les assets pour chaque caractère."""
    asset_keys = ["1 (Wall)", "0 (Empty)", "C (Item)", "P (Player)", "E (Exit)"]
    keys_mapping = ["1", "0", "C", "P", "E"]
    
    for key, char in zip(asset_keys, keys_mapping):
        path = filedialog.askopenfilename(
            title=f"Choisissez l'asset (.png) pour {key}",
            filetypes=[("PNG Files", "*.png")]
        )
        if not path:
            messagebox.showerror("Erreur", f"Asset pour '{key}' non sélectionné. Veuillez réessayer.")
            return False
        char_to_asset[char] = path
    
    load_assets()
    return True

# Fonction pour charger les assets
def load_assets():
    """Charge les assets en mémoire."""
    for char, path in char_to_asset.items():
        try:
            images[char] = PhotoImage(file=path)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger l'asset {path}: {e}")

# Fonction pour sauvegarder la map
def save_map():
    """Sauvegarde la grille actuelle en fichier .ber."""
    filename = filedialog.asksaveasfilename(defaultextension=".ber", filetypes=[("Map Files", "*.ber")])
    if filename:
        with open(filename, "w") as file:
            for row in grid:
                file.write("".join(row) + "\n")
        print(f"Map sauvegardée dans {filename}")

# Fonction pour créer la grille
def create_grid(canvas):
    """Dessine la grille avec les assets."""
    canvas.delete("all")
    for i in range(ROWS):
        for j in range(COLS):
            x, y = j * CELL_SIZE, i * CELL_SIZE
            char = grid[i][j]
            if char in images:
                canvas.create_image(x, y, anchor="nw", image=images[char])
            else:
                canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, outline="gray")

# Fonction pour gérer le clic
def on_click(event):
    """Place un élément sélectionné sur la cellule cliquée."""
    col, row = event.x // CELL_SIZE, event.y // CELL_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS and selected_asset.get():
        grid[row][col] = selected_asset.get()
        create_grid(canvas)

# Interface principale
root = tk.Tk()
root.title("Map Editor - so_long")

# Demander les chemins des assets
if not ask_asset_paths():
    root.destroy()  # Quitter si les assets ne sont pas chargés correctement

# Variables
selected_asset = tk.StringVar(value="1")  # Par défaut, '1' (Wall)

# Canvas pour la grille
canvas = tk.Canvas(root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="white")
canvas.pack()

# Menu de sélection des assets
frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Sélectionnez l'asset à placer :").pack(side=tk.LEFT)
for char, name in [("1", "Wall"), ("0", "Empty"), ("C", "Item"), ("P", "Player"), ("E", "Exit")]:
    tk.Radiobutton(frame, text=name, variable=selected_asset, value=char).pack(side=tk.LEFT)

# Bouton de sauvegarde
save_button = tk.Button(root, text="Save Map", command=save_map)
save_button.pack()

# Dessiner la grille
create_grid(canvas)
canvas.bind("<Button-1>", on_click)

root.mainloop()
