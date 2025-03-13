import os
import requests
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

# Dictionnaire des resource packs (nom affiché : URL)
resource_packs = {
    "WASD Resource Pack": "https://www.dropbox.com/scl/fi/5d87rctheyoxca7w8oyto/WASD-Resource-Pack-V7.6.0-MC_1.21.4.zip?rlkey=e8qh4idp4flvrm7ymxsuxp1ex&st=k5wk8hmo&dl=1",
    "Night vision": "https://www.curseforge.com/api/v1/mods/429113/files/3550486/download",
    "Fresh Animation": "https://www.curseforge.com/api/v1/mods/453763/files/6001123/download",
    "Autre...": ""  # Option personnalisée
}

def download_and_install_resource_pack():
    selected_pack = selected_pack_var.get()
    custom_url = custom_url_entry.get()

    # Gestion de l'URL selon la sélection
    if selected_pack == "Autre...":
        if not custom_url:
            messagebox.showerror("Erreur", "Veuillez entrer une URL valide !")
            return
        pack_url = custom_url
    else:
        pack_url = resource_packs.get(selected_pack)

    if not pack_url:
        messagebox.showerror("Erreur", "URL du resource pack introuvable !")
        return

    minecraft_folder = os.path.expanduser("~/AppData/Roaming/.minecraft/resourcepacks")
    os.makedirs(minecraft_folder, exist_ok=True)

    try:
        response = requests.get(pack_url)
        response.raise_for_status()

        # Générer un nom de fichier unique
        base_name = selected_pack.replace(' ', '_') if selected_pack != "Autre..." else "Custom_Pack"
        file_name = f"{base_name}.zip"
        counter = 1
        while os.path.exists(os.path.join(minecraft_folder, file_name)):
            file_name = f"{base_name}_{counter}.zip"
            counter += 1

        file_path = os.path.join(minecraft_folder, file_name)

        with open(file_path, 'wb') as file:
            file.write(response.content)

        messagebox.showinfo("Succès", f"Resource pack installé avec succès!\nEmplacement : {file_path}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Échec de l'installation : {str(e)}")

def open_youtube_tutorial(event):
    webbrowser.open("https://youtu.be/exemple_tutoriel")

# Création de l'interface
root = tk.Tk()
root.title("Installateur de Resource Packs")
root.geometry("400x220")

# Cadre principal
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True, fill='both')

# Menu déroulant
selected_pack_var = tk.StringVar()
pack_selector = ttk.Combobox(
    main_frame,
    textvariable=selected_pack_var,
    values=list(resource_packs.keys()),
    state='readonly'
)
pack_selector.pack(pady=5, fill='x')
pack_selector.current(0)

# Bouton d'installation
install_btn = ttk.Button(
    main_frame,
    text="Installer le pack sélectionné",
    command=download_and_install_resource_pack
)
install_btn.pack(pady=10, fill='x')

# Séparateur
ttk.Separator(main_frame).pack(fill='x', pady=5)

# Zone d'URL personnalisée
custom_url_frame = ttk.Frame(main_frame)
custom_url_frame.pack(fill='x')

ttk.Label(custom_url_frame, text="URL personnalisée :").pack(anchor='w')
custom_url_entry = ttk.Entry(custom_url_frame)
custom_url_entry.pack(fill='x', pady=5)

# Lien d'aide
help_label = tk.Label(
    main_frame,
    text="Comment obtenir l'URL ? Clique ici",
    fg="blue",
    cursor="hand2"
)
help_label.pack(pady=5)
help_label.bind("<Button-1>", open_youtube_tutorial)

root.mainloop()
