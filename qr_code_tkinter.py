import tkinter as tk  # Définit "tk"
from tkinter import (
    filedialog,  # Bibliotheque permettant d'ouvrir une boite de dialogue pour enregistrer son fichier ou choisir son image personalisable por le QR Code
    messagebox,  # Pop-up si champ non saisie
)

import qrcode
import requests
from PIL import (  # Permet de gérer les images générer via la librairie qrcode grace à PIL. Pour que Tkinter affiche le qrcode
    Image,
    ImageTk,
)
from qrcode.constants import ERROR_CORRECT_H

image_en_memoire = None  # Initialise la memoire  à vide
chemin_logo_choisi = None


def envoyer_litterbox():
    # 1. On choisit le fichier
    chemin = filedialog.askopenfilename()

    # Si l'utilisateur annule, on arrête la fonction
    if not chemin:
        return

    # On prépare l'envoi
    url = "https://litterbox.catbox.moe/resources/internals/api.php"
    parametres = {"reqtype": "fileupload", "time": "1h"}

    # ON OUVRE ET ON ENVOIE (Directement)
    # L'instruction 'with open' gère l'ouverture/fermeture du fichier proprement
    with open(chemin, "rb") as mon_fichier:
        reponse = requests.post(
            url, data=parametres, files={"fileToUpload": mon_fichier}
        )

    # On affiche le résultat
    if reponse.status_code == 200:
        lien = reponse.text

        # On met le lien dans le champ texte
        entry_lien.delete(0, "end")
        entry_lien.insert(0, lien)

        messagebox.showinfo("Réussi !", f"Voici votre lien :\n{lien}")
    else:
        messagebox.showerror(
            "Erreur", "L'envoi a échoué (Site en panne ? Ou fichier superieure à 1Go?)"
        )


def choisir_logo():
    global chemin_logo_choisi
    fichier = filedialog.askopenfilename(
        title="Choisissez votre logo",
        filetypes=[
            ("Images", "*.png *.jpg *.jpeg *.jpe *.bmp *.gif *.tiff *.tif *.webp"),
            ("Tous les fichiers", "*.*"),
        ],
    )  # Variable fichier stocke l'image. Permettant d'afficher une image sur le QR Code

    if fichier:
        chemin_logo_choisi = fichier
        label_info_logo.config(text="Logo: Chargé !", fg="green")
    else:
        # Si l'utilisateur annule
        pass


def generer_qrcode():
    global image_en_memoire

    lien = entry_lien.get()

    if not lien:
        messagebox.showwarning("Attention", "Veuillez saisir un lien ou une image !")
        return

    c_qr = var_couleur_qr.get()
    c_fond = var_couleur_fond.get()

    if c_qr == c_fond:
        messagebox.showerror(
            "Erreur", "La couleur des carrés et du fond sont identiques."
        )
        return

    # 1. Création du QR Code
    qr = qrcode.QRCode(
        version=5,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=5,
    )

    qr.add_data(lien)
    qr.make(fit=True)

    # 2. On crée l'image et on la convertit tout de suite en RGB (Couleurs)
    image_en_memoire = qr.make_image(fill_color=c_qr, back_color=c_fond).convert("RGB")

    # 3. Ajout du Logo (Méthode directe sans masque)
    if chemin_logo_choisi:
        logo = Image.open(chemin_logo_choisi)

        # Calcul taille
        largeur_qr = image_en_memoire.size[0]
        taille_logo = int(largeur_qr * 0.25)

        # Redimensionnement
        logo = logo.resize((taille_logo, taille_logo))

        # Position
        pos_x = (largeur_qr - taille_logo) // 2
        pos_y = (largeur_qr - taille_logo) // 2

        # On colle juste l'image aux coordonnées (pos_x, pos_y).
        image_en_memoire.paste(logo, (pos_x, pos_y))

    # 4. Affichage
    affichage_img = image_en_memoire.resize((250, 250))
    tk_image = ImageTk.PhotoImage(affichage_img)

    label_image_preview.config(image=tk_image)
    label_image_preview.image = tk_image

    btn_sauvegarder.config(state=tk.NORMAL, bg="#90ee90")


def sauvegarder_fichier():
    global image_en_memoire

    # Si aucune image n'a été générée, on ne fait rien
    if image_en_memoire is None:
        messagebox.showwarning("Erreur", "Générez d'abord un QR Code !")
        return

    # Ouvre la fenêtre "Enregistrer sous"
    chemin_fichier = filedialog.asksaveasfilename(
        title="Enregistrer votre QR Code",
        defaultextension=".png",  # Extension par defaut pour eviter que l'utilisateur rentre le .png
        filetypes=[
            ("Fichiers PNG", "*.png"),
            ("Tous les fichiers", "*.*"),
        ],  # Le choix entre .png ou toute les extensions
    )

    if chemin_fichier:
        image_en_memoire.save(chemin_fichier)
        messagebox.showinfo("QR Code sauvergardé à ce chemin: ", chemin_fichier)


def reinitialiser():
    global image_en_memoire, chemin_logo_choisi
    entry_lien.delete(
        0, tk.END
    )  # Vide le champ de saisie ('0' du début et 'END' à la fin)

    label_image_preview.config(
        image=""
    )  # Enlève le QR Code en utilisant une chaine de charactère vide
    image_en_memoire = None  # On vide la mémoire
    btn_sauvegarder.config(
        state=tk.DISABLED, bg="#f0f0f0"
    )  # Désactivation du bouton de sauvegarder de QR Code. Gris
    # On remet les couleurs par défaut
    var_couleur_qr.set("Black")
    var_couleur_fond.set("White")

    # On réinitialise le logo
    chemin_logo_choisi = None
    label_info_logo.config(text="Aucun logo", fg="black")


# ----------------- Application ---------------
# Création de la fenêtre de l'application
app = tk.Tk()
app.title("Générateur QR Code")
app.geometry("700x500")

# Texte (instruction)
label_instruction = tk.Label(app, text="Entrez votre lien ou insérer")
label_instruction.pack(pady=5)

# Champ de saisie
entry_lien = tk.Entry(app, width=40)
entry_lien.pack(pady=5)

# Upload image
frame_upload = tk.LabelFrame(
    app, text=" Upload le fichier sur litterbox.catbox.moe ", padx=10, pady=10
)
frame_upload.pack(pady=10, fill="x", padx=20)

tk.Label(
    frame_upload, text="Upload le fichier et générez son lien:", font=("Arial", 9)
).pack()

btn_upload = tk.Button(
    frame_upload,
    text="📤",
    command=envoyer_litterbox,
    bg="#007aff",
    fg="white",
    font=("Arial", 10, "bold"),
)
btn_upload.pack(pady=5)

label_upload_status = tk.Label(frame_upload, text="", font=("Arial", 9))
label_upload_status.pack()

# Bouton / generation
btn_generer = tk.Button(
    app, text="Générer QR Code", command=generer_qrcode, bg="#dddddd"
)
btn_generer.pack(pady=10)

# Affiche le Qr Code une fois générer dans l'application sans rechercher la photo sur le disque dur du pc
label_image_preview = tk.Label(app)
label_image_preview.pack(pady=10)

# Bouton pour sauvegarde le QR Code
btn_sauvegarder = tk.Button(
    app, text="Enregistrer le QR Code", command=sauvegarder_fichier, state=tk.DISABLED
)
btn_sauvegarder.pack(pady=10)

# Bouton / reinitialiser
btn_reinitialiser = tk.Button(
    app, text="Reinitialiser", command=reinitialiser, bg="#ff0000"
)  # Fond rouge
btn_reinitialiser.pack(pady=5)

# Zone d'apprence
frame_options = tk.LabelFrame(app, text=" Personnalisation ", padx=10, pady=10)
frame_options.pack(pady=10, fill="x", padx=20)
liste_couleurs = [
    "Black",
    "White",
    "Blue",
    "Red",
    "Green",
    "Yellow",
    "Orange",
    "Purple",
    "Grey",
]

# Couleur des carrés
tk.Label(frame_options, text="Couleur Code :").pack(side=tk.LEFT)
var_couleur_qr = tk.StringVar(app)  # Variable qui stocke le choix
var_couleur_qr.set("Black")  # Valeur par défaut
menu_qr = tk.OptionMenu(frame_options, var_couleur_qr, *liste_couleurs)
menu_qr.pack(side=tk.LEFT, padx=10)

# Couleur du Fond
tk.Label(frame_options, text="Couleur Fond :").pack(side=tk.LEFT)
var_couleur_fond = tk.StringVar(app)
var_couleur_fond.set("White")
menu_fond = tk.OptionMenu(frame_options, var_couleur_fond, *liste_couleurs)
menu_fond.pack(side=tk.LEFT, padx=10)

# Ajout du logo
tk.Frame(frame_options, height=1, bg="#ddd").pack(
    fill="x", pady=10
)  # Ligne de séparation
frame_logo = tk.Frame(frame_options)
frame_logo.pack(fill="x")

btn_logo = tk.Button(
    frame_logo, text="Ajouter un Logo (Optionnel)", command=choisir_logo
)
btn_logo.pack(side=tk.LEFT)

label_info_logo = tk.Label(frame_logo, text="Aucun logo", font=("Arial", 9, "italic"))
label_info_logo.pack(side=tk.LEFT, padx=10)

app.mainloop()
