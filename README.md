# 📱 Générateur de QR Code Personnalisable & Hébergeur de Fichiers

## 🎓 Contexte du projet
Ce programme a été développé dans le cadre d'un **projet étudiant en première année de Licence (L1)**. 
L'objectif de ce projet est de mettre en pratique les concepts fondamentaux de la programmation en Python, notamment la création d'une Interface Homme-Machine (IHM), l'utilisation d'API web et le traitement d'images.

## 🚀 Fonctionnalités
L'application propose une interface graphique complète permettant de :
- **Générer des QR Codes** à partir de n'importe quel lien web ou texte.
- **Héberger des fichiers en ligne** : Intégration de l'API *Litterbox (catbox.moe)* pour uploader un fichier local et récupérer automatiquement son lien web (valide 1 heure).
- **Personnaliser le QR Code** : 
  - Choix de la couleur des motifs (carrés).
  - Choix de la couleur de fond.
  - Possibilité d'incruster un **logo personnalisé** au centre du QR Code.
- **Sauvegarder** le résultat final au format `.png` sur l'ordinateur.
- **Réinitialiser** l'interface pour créer un nouveau QR Code rapidement.

## 🛠️ Prérequis et Installation

Pour exécuter ce projet, vous devez avoir **Python 3.x** installé sur votre machine. 
Le programme s'appuie sur plusieurs bibliothèques externes qu'il est nécessaire d'installer.

1. Ouvrez votre terminal ou invite de commande.
2. Installez les dépendances requises en utilisant la commande correspondant à votre système d'exploitation :

### 🪟 Pour Windows (PowerShell ou Invite de commandes) :
```powershell
python -m pip install "qrcode[pil]" Pillow requests
```

###🐧 Pour Linux et 🍏 macOS (Terminal) :
```bash
python3 -m pip install "qrcode[pil]" Pillow requests
```
