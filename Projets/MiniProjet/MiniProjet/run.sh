#!/bin/bash

# Script de lancement pour la détection des mains avec MediaPipe

echo "🖐️  Lancement de la détection des mains avec MediaPipe..."
echo "========================================================="
echo ""
echo "📌 Instructions :"
echo "   - Placez votre main devant la caméra"
echo "   - Le squelette de votre main sera affiché avec 21 points"
echo "   - Le nombre de doigts levés sera compté en temps réel"
echo "   - Appuyez sur 'q' pour quitter"
echo ""
echo "========================================================="
echo ""

# Lancer le programme avec l'environnement MediaPipe (Python 3.11)
venv_mediapipe/bin/python hand_detection.py
