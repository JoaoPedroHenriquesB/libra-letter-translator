import cv2
import mediapipe as mp
import json
import os
from gestures import detect_letra

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,      
    max_num_hands=1,              
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5 
)

cap = cv2.VideoCapture(0)

def save_landmarks(landmarks, filename):
    data = [[lm.x, lm.y, lm.z] for lm in landmarks.landmark]
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(f"Landmarks salvos em {filename}")

def save_landmarks_to_single_file(landmarks, letra, filename="landmarks/all_landmarks.json"):
    data = [[lm.x, lm.y, lm.z] for lm in landmarks.landmark]
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            all_data = json.load(f)
    else:
        all_data = {}
    if letra not in all_data:
        all_data[letra] = []
    all_data[letra].append(data)
    with open(filename, 'w') as f:
        json.dump(all_data, f, indent=2)
    print(f"Amostra salva para a letra {letra} em {filename}")

def load_all_landmarks(filename="landmarks/all_landmarks.json"):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return {}
    with open(filename, 'r') as f:
        return json.load(f)

if not os.path.exists("landmarks"):
    os.makedirs("landmarks")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                mp.solutions.drawing_styles.get_default_hand_connections_style()
            )
            letra = detect_letra(hand_landmarks)
            cv2.putText(frame, letra, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            
            if cv2.waitKey(1) & 0xFF == ord('s'):
                letra = input("Digite a letra para salvar: ").upper()
                save_landmarks_to_single_file(hand_landmarks, letra)

    cv2.imshow('Detecção', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

hands.close()
cap.release()
cv2.destroyAllWindows()