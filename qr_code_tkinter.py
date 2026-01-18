import tkinter as tk  # Définit "tk"
from tkinter import (
    filedialog,  # Bibliotheque permettant d'ouvrir une boite de dialogue pour enregistrer son fichier ou choisir son image personalisable por le QR Code
    messagebox,  # Pop-up si champ non saisie
)

import qrcode
from PIL import (  # Permet de gérer les images générer via la librairie qrcode grace à PIL. Pour que Tkinter affiche le qrcode
    Image,
    ImageTk,
)
from qrcode.constants import ERROR_CORRECT_H

image_en_memoire = None  # Initialise la memoire  à vide
chemin_logo_choisi = None


def choisir_logo():
    global chemin_logo_choisi
    fichier = filedialog.askopenfilename(
        title="Choisissez votre logo",
        filetypes=[
            (
                "Images",
                "*.png;*.jpg;*.jpeg;*.jpe;*.bmp;*.gif;*.tiff;*.tif;*.webp;*.ico;*.heic;*.heif",
            )
        ],
    )  # Variable fichier stocke l'image. Permettant d'afficher une image sur le QR Code

    if fichier:
        chemin_logo_choisi = fichier
        label_info_logo.config(text="Logo: Chargé !", fg="green")
    else:
        # Si l'utilisateur annule
        pass


def generer_qrcode():
    global image_en_memoire  # Utiliser la variable  en tant que globale

    lien = entry_lien.get()

    if not lien:
        messagebox.showwarning("Attention", "Veuillez saisir un lien ou une image !")
        return
    c_qr = var_couleur_qr.get()
    c_fond = var_couleur_fond.get()

    # Si les couleurs sont identiques, on avertit
    if c_qr == c_fond:
        messagebox.showerror(
            "Erreur", "La couleur des carrés et du fond sont identiques."
        )
        return

    qr = qrcode.QRCode(
        version=5,  # Contrôle la taille du QR Code (1 = petit jusqu'à 40)
        error_correction=ERROR_CORRECT_H,  # Haute correction (Ideal pour l'ajout d'un logo)
        box_size=10,  # Taille de chaque "pixel" du QR code
        border=5,  # Épaisseur de la bordure blanche
    )

    qr.add_data(lien)
    qr.make(fit=True)

    image_en_memoire = qr.make_image(
        fill_color=c_qr, back_color=c_fond
    )  # Image de type PIL et gardé en memoire + parametre pour l'apparence du QR Code

    image_en_memoire = image_en_memoire.convert(
        "RGBA"
    )  # Converti en mode RGBA pour la transparence

    if chemin_logo_choisi:
        logo = Image.open(chemin_logo_choisi)

        logo = logo.convert(
            "RGBA"
        )  # Force le logo à avoir une couche de transparence (Alpha soit le A à la fin de "RGBA")

        # Calcul de la taille du logo
        largeur_qr = image_en_memoire.size[0]
        taille_logo = int(largeur_qr * 0.25)  # 25% max pour le logo

        logo = logo.resize((taille_logo, taille_logo))

        # Calcul du centre
        pos_x = (largeur_qr - taille_logo) // 2
        pos_y = (largeur_qr - taille_logo) // 2

        if len(logo.split()) == 4:
            r, g, b, a = logo.split()
            masque = a
        else:
            masque = logo

        image_en_memoire.paste(
            logo, (pos_x, pos_y), mask=masque
        )  # Collage du logo sur le QR Code. Le 3ème argument 'logo' sert de masque (pour gérer la transparence du logo s'il y en a). Si le logo n'a pas de transparence, on peut l'enlever

    affichage_img = image_en_memoire.resize(
        (250, 250)
    )  # Copie de l'image de type PIL pour l'affichage de l'image à 250x250 Px

    tk_image = ImageTk.PhotoImage(
        affichage_img
    )  # Convertit de PIL en image compréhensible pour Tkinter

    label_image_preview.config(image=tk_image)  # Met l'image dans le label creer pour

    label_image_preview.image = tk_image  # Garde l'image en référence sinon, python la supprime et donc ne s'affiche pas

    btn_sauvegarder.config(
        state=tk.NORMAL, bg="#90ee90"
    )  # Bouton pour sauvegarder le fichier activé. Vert clair


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
label_instruction = tk.Label(app, text="Entrez votre lien ou image")
label_instruction.pack(pady=5)

# Champ de saisie
entry_lien = tk.Entry(app, width=40)
entry_lien.pack(pady=5)

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
