# 🖐️ Mini-Projet : Détection des mains et squelette, comptage des doigts

## 📋 Description

Système de détection des mains en temps réel utilisant l'IA de Google (MediaPipe) :

✅ **Détection précise des mains** avec squelette (21 points de repère)  
✅ **Comptage automatique des doigts** levés (0-5)  
✅ **Affichage en temps réel** via webcam  
✅ **Support multi-mains** (jusqu'à 2 mains simultanément)  

## 🛠️ Technologies

- **Python 3.11** 
- **OpenCV** - Traitement d'image et vidéo
- **MediaPipe** - IA de Google pour la détection des mains
- **NumPy** - Calculs mathématiques

## 📦 Installation

**✅ Déjà fait !** Tout est installé dans `venv_mediapipe/`

### Pour réinstaller si nécessaire :

```bash
/usr/local/bin/python3.11 -m venv venv_mediapipe
venv_mediapipe/bin/pip install opencv-python mediapipe numpy
```

## 🚀 Lancement

**Méthode simple :**
```bash
./run.sh
```

**Ou manuellement :**
```bash
venv_mediapipe/bin/python hand_detection.py
```

## 🎮 Utilisation

1. **Lancez** le programme
2. **Autorisez** l'accès à la webcam si demandé
3. **Placez votre main** devant la caméra (distance ~50cm)
4. **Levez vos doigts** pour voir le comptage en direct
5. **Appuyez sur 'q'** pour quitter

## 📊 Affichage

- **Zone verte** : Nombre total de doigts levés
- **Squelette** : 21 points rouges connectés suivant votre main
- **Liste détaillée** : État de chaque doigt (vert=levé, rouge=baissé)
  - Pouce, Index, Majeur, Annulaire, Auriculaire


## 🧠 Algorithme

### Détection des doigts levés

Le système utilise les 21 points de repère MediaPipe :
- **Point 0** : Poignet
- **Points 1-4** : Pouce
- **Points 5-8** : Index  
- **Points 9-12** : Majeur
- **Points 13-16** : Annulaire
- **Points 17-20** : Auriculaire

**Logique de détection :**
- **Pouce** : Comparaison horizontale (gauche/droite)
- **Autres doigts** : Le bout doit être au-dessus de l'articulation

## 💡 Conseils

✓ **Bon éclairage** (lumière naturelle ou LED)  
✓ **Fond simple** (mur uni, bureau)  
✓ **Main bien visible** (doigts écartés)  
✓ **Distance optimale** (~50cm de la caméra)  

## ⚠️ Dépannage

**Webcam ne fonctionne pas :**
- Vérifiez les autorisations : Préférences Système → Sécurité → Caméra

**Détection imprécise :**
- Améliorez l'éclairage
- Utilisez un fond neutre
- Ajustez votre distance

## 📁 Structure du projet

```
MiniProjet/
├── hand_detection.py       # Programme principal
├── run.sh                  # Script de lancement
├── README.md               # Documentation
├── RAPPORT.md              # Rapport technique
├── requirements.txt        # Dépendances
├── venv_mediapipe/        # Environnement Python 3.11
└── AppGraph_MiniProjet.pdf # Sujet
```

## 📝 Auteurs

Mini-Projet - Application Graphique

## 📄 Licence

Projet éducatif
