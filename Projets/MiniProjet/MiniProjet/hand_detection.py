"""
Mini-Projet : Détection des mains et squelette, comptage des doigts
Utilise MediaPipe et OpenCV pour détecter les mains en temps réel
"""

import cv2
import mediapipe as mp
import math

class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        """
        Initialise le détecteur de mains avec MediaPipe
        
        Args:
            mode: Mode statique ou vidéo
            max_hands: Nombre maximum de mains à détecter
            detection_confidence: Confiance minimum pour la détection
            tracking_confidence: Confiance minimum pour le suivi
        """
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        
        # Initialisation de MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # IDs des doigts (pouce, index, majeur, annulaire, auriculaire)
        self.tip_ids = [4, 8, 12, 16, 20]
        
    def find_hands(self, img, draw=True):
        """
        Détecte les mains dans une image
        
        Args:
            img: Image d'entrée
            draw: Si True, dessine le squelette de la main
            
        Returns:
            Image avec annotations si draw=True
        """
        # Conversion BGR vers RGB pour MediaPipe
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        # Dessiner les landmarks si des mains sont détectées
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    # Dessiner les connexions du squelette
                    self.mp_draw.draw_landmarks(
                        img,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )
        
        return img
    
    def find_position(self, img, hand_number=0, draw=True):
        """
        Trouve la position de tous les landmarks d'une main
        
        Args:
            img: Image d'entrée
            hand_number: Numéro de la main à analyser
            draw: Si True, dessine des cercles sur les landmarks
            
        Returns:
            Liste des positions [id, x, y] pour chaque landmark
        """
        self.landmark_list = []
        
        if self.results.multi_hand_landmarks:
            if hand_number < len(self.results.multi_hand_landmarks):
                my_hand = self.results.multi_hand_landmarks[hand_number]
                
                for id, landmark in enumerate(my_hand.landmark):
                    # Obtenir les coordonnées en pixels
                    h, w, c = img.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    self.landmark_list.append([id, cx, cy])
                    
                    if draw:
                        cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
        
        return self.landmark_list
    
    def fingers_up(self):
        """
        Détermine quels doigts sont levés
        
        Returns:
            Liste de 5 éléments (1 si doigt levé, 0 sinon)
        """
        fingers = []
        
        if len(self.landmark_list) != 0:
            # Pouce (logique différente car il se déplace horizontalement)
            if self.landmark_list[self.tip_ids[0]][1] > self.landmark_list[self.tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            
            # 4 autres doigts (index, majeur, annulaire, auriculaire)
            for id in range(1, 5):
                # Si le bout du doigt est au-dessus de l'articulation
                if self.landmark_list[self.tip_ids[id]][2] < self.landmark_list[self.tip_ids[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        
        return fingers
    
    def find_distance(self, p1, p2, img, draw=True, endpoint_color=(255, 0, 255), midpoint_color=(255, 0, 255)):
        """
        Calcule la distance entre deux points
        
        Args:
            p1: ID du premier point
            p2: ID du deuxième point
            img: Image pour dessiner
            draw: Si True, dessine une ligne entre les points
            
        Returns:
            Tuple (longueur, img, [x1, y1, x2, y2, cx, cy])
        """
        if len(self.landmark_list) != 0:
            x1, y1 = self.landmark_list[p1][1], self.landmark_list[p1][2]
            x2, y2 = self.landmark_list[p2][1], self.landmark_list[p2][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            # Calculer la longueur avant d'utiliser 'length' pour les rayons
            length = math.hypot(x2 - x1, y2 - y1)

            if draw:
                # Calculer un rayon dynamique basé sur la distance entre les points
                # Ainsi les cercles s'adaptent à différentes tailles de mains
                # On prend une fraction de la distance et on la borne entre min/max
                dynamic_radius = max(12, min(int(length * 0.20), 120))
                midpoint_radius = max(8, min(int(length * 0.12), 80))

                # Dessiner les deux cercles aux extrémités (pouce et index) et la droite
                cv2.circle(img, (x1, y1), dynamic_radius, endpoint_color, cv2.FILLED)
                cv2.circle(img, (x2, y2), dynamic_radius, endpoint_color, cv2.FILLED)

                # Ligne de connexion (épaisseur relative)
                line_thickness = max(2, int(dynamic_radius / 6))
                cv2.line(img, (x1, y1), (x2, y2), endpoint_color, line_thickness)

                # Cercle au milieu avec une couleur différente et rayon adapté
                cv2.circle(img, (cx, cy), midpoint_radius, midpoint_color, cv2.FILLED)
            return length, img, [x1, y1, x2, y2, cx, cy]
        
        return None, img, None


def main():
    """
    Fonction principale pour exécuter la détection en temps réel
    """
    # Initialisation de la webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # Largeur
    cap.set(4, 720)   # Hauteur
    
    # Initialisation du détecteur
    detector = HandDetector(max_hands=2)
    
    # Noms des doigts
    finger_names = ["Pouce", "Index", "Majeur", "Annulaire", "Auriculaire"]
    
    print("🖐️  Détection des mains activée!")
    print("Appuyez sur 'q' pour quitter")
    
    while True:
        success, img = cap.read()
        
        if not success:
            print("Erreur: Impossible de lire la webcam")
            break
        
        # Détecter les mains
        img = detector.find_hands(img)
        landmark_list = detector.find_position(img, draw=False)
        
        # Comptage des doigts
        if len(landmark_list) != 0:
            fingers = detector.fingers_up()
            total_fingers = fingers.count(1)
            
            # Afficher le nombre de doigts levés
            cv2.rectangle(img, (20, 20), (270, 120), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'Doigts leves: {total_fingers}', (30, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
            
            # Afficher le détail des doigts
            y_position = 150
            for i, finger in enumerate(fingers):
                status = "LEVE" if finger == 1 else "BAISSE"
                color = (0, 255, 0) if finger == 1 else (0, 0, 255)
                cv2.putText(img, f'{finger_names[i]}: {status}', (30, y_position),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                y_position += 35
            # Dessiner un cercle sur le pouce et l'index, une droite entre eux,
            # et un cercle d'une autre couleur au milieu de la droite
            detector.find_distance(4, 8, img, draw=True, endpoint_color=(0, 255, 0), midpoint_color=(0, 0, 255))
        
        # Afficher les instructions
        cv2.putText(img, "Appuyez sur 'q' pour quitter", (img.shape[1] - 400, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Afficher l'image
        cv2.imshow("Detection des mains - Comptage des doigts", img)
        
        # Quitter avec 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Libérer les ressources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
