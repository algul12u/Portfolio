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
        
        # Debug : stocker les derniers ratios calculés
        self.last_finger_ratio = 0
        self.last_aspect_ratio = 0
        self.last_all_fingers_ratio = 0
        self.last_thumb_angle = 0
        self.last_spread_ratio = 0
        
    def is_valid_hand(self, hand_landmarks, debug=False):
        """
        Vérifie si la main détectée a des proportions géométriques valides
        VALIDATION ULTRA-STRICTE pour éliminer TOUS les pieds
        """
        # Points de repère principaux
        wrist = hand_landmarks.landmark[0]
        thumb_tip = hand_landmarks.landmark[4]
        thumb_mcp = hand_landmarks.landmark[2]   # Base du pouce
        index_mcp = hand_landmarks.landmark[5]   # Base de l'index
        index_tip = hand_landmarks.landmark[8]   # Bout de l'index
        middle_mcp = hand_landmarks.landmark[9]  # Base du majeur
        middle_tip = hand_landmarks.landmark[12] # Bout du majeur
        ring_mcp = hand_landmarks.landmark[13]   # Base de l'annulaire
        ring_tip = hand_landmarks.landmark[16]   # Bout de l'annulaire
        pinky_mcp = hand_landmarks.landmark[17]  # Base de l'auriculaire
        pinky_tip = hand_landmarks.landmark[20]  # Bout de l'auriculaire
        
        # 1. Longueur de la paume (Poignet -> Base du majeur)
        palm_length = math.hypot(middle_mcp.x - wrist.x, middle_mcp.y - wrist.y)
        
        # 2. Largeur de la paume (Base Index -> Base Auriculaire)
        palm_width = math.hypot(pinky_mcp.x - index_mcp.x, pinky_mcp.y - index_mcp.y)
        
        # 3. Longueur de TOUS les doigts
        index_length = math.hypot(index_tip.x - index_mcp.x, index_tip.y - index_mcp.y)
        middle_length = math.hypot(middle_tip.x - middle_mcp.x, middle_tip.y - middle_mcp.y)
        ring_length = math.hypot(ring_tip.x - ring_mcp.x, ring_tip.y - ring_mcp.y)
        pinky_length = math.hypot(pinky_tip.x - pinky_mcp.x, pinky_tip.y - pinky_mcp.y)
        
        # 4. Angle du pouce
        v1_x = thumb_tip.x - wrist.x
        v1_y = thumb_tip.y - wrist.y
        v2_x = index_mcp.x - wrist.x
        v2_y = index_mcp.y - wrist.y
        
        dot_product = v1_x * v2_x + v1_y * v2_y
        mag1 = math.sqrt(v1_x**2 + v1_y**2)
        mag2 = math.sqrt(v2_x**2 + v2_y**2)
        
        if mag1 == 0 or mag2 == 0 or palm_length == 0:
            return False
            
        cos_angle = max(-1.0, min(1.0, dot_product / (mag1 * mag2)))
        thumb_angle_deg = math.degrees(math.acos(cos_angle))
        
        # 5. NOUVEAU: Écartement des doigts (spread)
        # Les mains peuvent écarter les doigts, les pieds ont des orteils serrés
        finger_spread = math.hypot(index_tip.x - pinky_tip.x, index_tip.y - pinky_tip.y)
        spread_ratio = finger_spread / palm_length
        
        # --- VALIDATION ULTRA-STRICTE ---
        
        finger_ratio = middle_length / palm_length
        aspect_ratio = palm_width / palm_length
        avg_finger_length = (index_length + middle_length + ring_length + pinky_length) / 4
        all_fingers_ratio = avg_finger_length / palm_length
        
        # Stockage debug
        self.last_finger_ratio = finger_ratio
        self.last_aspect_ratio = aspect_ratio
        self.last_all_fingers_ratio = all_fingers_ratio
        self.last_thumb_angle = thumb_angle_deg
        self.last_spread_ratio = spread_ratio
        
        # SEUILS MAXIMUM - Si un pied passe ça, c'est impossible
        is_long_fingers = finger_ratio > 0.8        # TRÈS long (était 0.7)
        is_square_palm = aspect_ratio > 0.75        # TRÈS carré (était 0.7)
        is_all_fingers_long = all_fingers_ratio > 0.65  # TOUS très longs (était 0.55)
        is_thumb_perpendicular = 50 < thumb_angle_deg < 130  # Plus strict (était 40-140)
        is_fingers_spread = spread_ratio > 1.2      # Doigts écartés
        
        # TOUS les critères doivent être vrais
        return (is_long_fingers and is_square_palm and is_all_fingers_long 
                and is_thumb_perpendicular and is_fingers_spread)

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
        
        # Stocker uniquement les mains valides
        self.valid_hands = []
        
        # Dessiner les landmarks si des mains sont détectées
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if self.is_valid_hand(hand_landmarks):
                    self.valid_hands.append(hand_landmarks)
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
        
        if self.valid_hands:
            if hand_number < len(self.valid_hands):
                my_hand = self.valid_hands[hand_number]
                
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
    detector = HandDetector(max_hands=2, detection_confidence=0.8, tracking_confidence=0.8)
    
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
            
            # Affichage DEBUG des ratios géométriques
            debug_y = 300
            cv2.putText(img, f'DEBUG - Validation ULTRA-STRICTE:', (30, debug_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
            cv2.putText(img, f'Majeur/Paume: {detector.last_finger_ratio:.2f} (min: 0.80)', (30, debug_y + 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
            cv2.putText(img, f'Largeur/Long: {detector.last_aspect_ratio:.2f} (min: 0.75)', (30, debug_y + 45),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
            cv2.putText(img, f'Moy.Doigts: {detector.last_all_fingers_ratio:.2f} (min: 0.65)', (30, debug_y + 65),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
            cv2.putText(img, f'Angle Pouce: {detector.last_thumb_angle:.1f}deg (50-130)', (30, debug_y + 85),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
            cv2.putText(img, f'Ecartement: {detector.last_spread_ratio:.2f} (min: 1.20)', (30, debug_y + 105),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
        
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
