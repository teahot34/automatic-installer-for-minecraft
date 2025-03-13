import json
import os
import requests
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

CURRENT_VERSION = "v1"

# Dictionnaire des resource packs (nom affiché : URL)
resource_packs = {
    "WASD Resource Pack": "https://www.dropbox.com/scl/fi/5d87rctheyoxca7w8oyto/WASD-Resource-Pack-V7.6.0-MC_1.21.4.zip?rlkey=e8qh4idp4flvrm7ymxsuxp1ex&st=k5wk8hmo&dl=1",
    "Night vision": "https://www.curseforge.com/api/v1/mods/429113/files/3550486/download",
    "Fresh Animation": "https://www.curseforge.com/api/v1/mods/453763/files/6001123/download",
    "Autre... ": ""  # Option personnalisée
}




def check_for_updates():
    try:
        # Configuration de la requête
        repo_owner = "teahot34"
        repo_name = "automatic-installer-for-minecraft"
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

        headers = {
            "User-Agent": "MinecraftInstaller/1.0",
            "Accept": "application/vnd.github.v3+json"
        }

        # Exécution de la requête
        response = requests.get(api_url, headers=headers, timeout=15)

        # Analyse des codes d'état HTTP
        if response.status_code == 200:
            release_data = response.json()

            # Vérification de la structure des données
            if "tag_name" not in release_data:
                messagebox.showerror("Erreur", "Réponse API invalide : clé 'tag_name' manquante")
                return

            latest_version = release_data["tag_name"].lower().lstrip('v')
            current_version = CURRENT_VERSION.lower().lstrip('v')

            # Comparaison numérique des versions
            if latest_version > current_version:
                changelog = release_data.get("body", "Aucune description disponible")
                messagebox.showinfo(
                    "Mise à jour disponible",
                    f"Version actuelle: v{current_version}\n"
                    f"Nouvelle version: v{latest_version}\n\n"
                    f"Notes de version:\n{changelog}\n\n"
                    f"Téléchargement: {release_data['html_url']}"
                )
            else:
                messagebox.showinfo("À jour", "Vous utilisez déjà la dernière version !")

        elif response.status_code == 404:
            messagebox.showerror(
                "Erreur 404",
                "Dépôt non trouvé ! Vérifiez :\n"
                f"- L'orthographe ({repo_owner}/{repo_name})\n"
                "- Que le dépôt existe et est public\n"
                "- Que vous avez bien créé une Release"
            )

        elif response.status_code == 403:
            messagebox.showerror(
                "Limite API dépassée",
                "Limite de requêtes GitHub atteinte !\n"
                "Réessayez plus tard ou utilisez un token d'API."
            )

        else:
            messagebox.showerror(
                "Erreur inconnue",
                f"Code d'état HTTP: {response.status_code}\n"
                f"Réponse: {response.text[:200]}..."
            )

    except requests.exceptions.RequestException as e:
        error_message = f"Erreur réseau : {str(e)}"
        if isinstance(e, requests.exceptions.Timeout):
            error_message += "\nLe délai d'attente est dépassé (15s)"
        messagebox.showerror("Erreur de connexion", error_message)

    except json.JSONDecodeError:
        messagebox.showerror("Erreur API", "Réponse API invalide (JSON corrompu)")

    except Exception as e:
        messagebox.showerror(
            "Erreur inattendue",
            f"Type: {type(e).__name__}\n"
            f"Message: {str(e)}"
        )


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

root = tk.Tk()
root.title("Installateur de Resource Packs")
root.geometry("400x300")  # Augmenter la hauteur

# Cadre principal
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True, fill='both')

# Ajouter le bouton de vérification des mises à jour DANS LE CADRE PRINCIPAL
check_update_button = ttk.Button(
    main_frame,  # <-- Changement ici
    text="Vérifier les mises à jour",
    command=check_for_updates
)
check_update_button.pack(pady=10, fill='x')  # <-- Avant le menu déroulant

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
