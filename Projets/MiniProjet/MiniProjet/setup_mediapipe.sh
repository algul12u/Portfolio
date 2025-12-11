#!/bin/bash

# Script pour installer MediaPipe avec Python 3.12 ou inférieur

echo "🔧 Configuration de l'environnement pour MediaPipe..."
echo "=================================================="

# Vérifier si Python 3.12 est disponible
if command -v python3.12 &> /dev/null; then
    echo "✅ Python 3.12 détecté"
    
    # Créer un environnement virtuel avec Python 3.12
    python3.12 -m venv venv_mediapipe
    
    # Activer l'environnement
    source venv_mediapipe/bin/activate
    
    # Installer les packages
    pip install --upgrade pip
    pip install opencv-python mediapipe numpy
    
    echo ""
    echo "✅ Installation terminée!"
    echo "📌 Pour utiliser le programme avec MediaPipe:"
    echo "   source venv_mediapipe/bin/activate"
    echo "   python hand_detection.py"
    
else
    echo "⚠️  Python 3.12 non trouvé"
    echo "📌 Utilisez hand_detection_v3.py avec Python 3.13"
    echo "   .venv/bin/python hand_detection_v3.py"
fi
