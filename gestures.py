import json
import math
import numpy as np
import os

def load_landmarks(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def load_all_landmarks(filename="landmarks/all_landmarks.json"):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return {}
    with open(filename, 'r') as f:
        return json.load(f)

def extract_landmarks(hand_landmarks):
    return [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]

def compare_landmarks(landmarks1, landmarks2):
    return sum(
        math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
        for a, b in zip(landmarks1, landmarks2)
    )

def normalize_landmarks(landmarks):
    arr = np.array([[x, y] for x, y, z in landmarks])
    center = arr.mean(axis=0)
    arr -= center
    scale = np.linalg.norm(arr, axis=1).max()
    if scale > 0:
        arr /= scale
    return arr.tolist()

def detect_letra(hand_landmarks, filename="landmarks/all_landmarks.json"):
    current = normalize_landmarks(extract_landmarks(hand_landmarks))
    all_landmarks = load_all_landmarks(filename)
    min_dist = float('inf')
    letra_detectada = '?'
    limiar = 1.2

    for letra, amostras in all_landmarks.items():
        for ref in amostras:
            ref_norm = normalize_landmarks(ref)
            dist = compare_landmarks(current, ref_norm)
            if dist < min_dist and dist < limiar:
                min_dist = dist
                letra_detectada = letra
    return letra_detectada

def detect_j_movement(sequence):
    """Detecta movimento da letra J - movimento em gancho para baixo e esquerda"""
    if len(sequence) < 5:
        return False

    start = sequence[0][20]
    end = sequence[-1][20]

    moved_down = end[1] > start[1] + 0.05 
    moved_left = end[0] < start[0] - 0.02
    
    return moved_down and moved_left

def detect_h_movement(sequence):
    """Detecta movimento da letra H - movimento horizontal da direita para esquerda"""
    if len(sequence) < 5:
        return False
    start_index = sequence[0][8]
    end_index = sequence[-1][8]
    start_middle = sequence[0][12]
    end_middle = sequence[-1][12]
    index_moved_left = end_index[0] < start_index[0] - 0.08
    middle_moved_left = end_middle[0] < start_middle[0] - 0.08
    index_stable_y = abs(end_index[1] - start_index[1]) < 0.05
    middle_stable_y = abs(end_middle[1] - start_middle[1]) < 0.05
    
    return index_moved_left and middle_moved_left and index_stable_y and middle_stable_y

def detect_z_movement(sequence):
    """Detecta movimento da letra Z - movimento em zigue-zague"""
    if len(sequence) < 8:
        return False
    points = [frame[8] for frame in sequence]
    third = len(points) // 3
    
    if third < 2:
        return False

    start1 = points[0]
    end1 = points[third]
    diagonal_down_right = (end1[0] > start1[0] + 0.03) and (end1[1] > start1[1] + 0.03)
    start2 = points[third]
    end2 = points[2 * third]
    horizontal_left = (end2[0] < start2[0] - 0.05) and (abs(end2[1] - start2[1]) < 0.03)
    start3 = points[2 * third]
    end3 = points[-1]
    diagonal_down_right2 = (end3[0] > start3[0] + 0.03) and (end3[1] > start3[1] + 0.03)
    
    return diagonal_down_right and horizontal_left and diagonal_down_right2

def detect_x_movement(sequence):
    """Detecta movimento da letra X - movimento de gancho pequeno"""
    if len(sequence) < 4:
        return False
    start = sequence[0][8]
    end = sequence[-1][8]
    middle_idx = len(sequence) // 2
    middle = sequence[middle_idx][8]
    moved_down = middle[1] > start[1] + 0.02
    moved_up = end[1] < middle[1] - 0.01
    horizontal_stable = abs(end[0] - start[0]) < 0.03
    
    return moved_down and moved_up and horizontal_stable

def detect_movement_letter(sequence, letter_type):
    """Função principal para detectar letras que requerem movimento"""
    if letter_type == 'J':
        return detect_j_movement(sequence)
    elif letter_type == 'H':
        return detect_h_movement(sequence)
    elif letter_type == 'Z':
        return detect_z_movement(sequence)
    elif letter_type == 'X':
        return detect_x_movement(sequence)
    else:
        return False

def get_hand_shape_for_movement(hand_landmarks):
    """Identifica a forma da mão para determinar qual movimento detectar"""
    landmarks = extract_landmarks(hand_landmarks)
    
    pinky_extended = landmarks[20][1] < landmarks[19][1]
    other_fingers_closed = all([
        landmarks[8][1] > landmarks[6][1],  
        landmarks[12][1] > landmarks[10][1],
        landmarks[16][1] > landmarks[14][1],
    ])
    
    if pinky_extended and other_fingers_closed:
        return 'J'
    index_extended = landmarks[8][1] < landmarks[6][1]
    middle_extended = landmarks[12][1] < landmarks[10][1]
    ring_closed = landmarks[16][1] > landmarks[14][1]
    pinky_closed = landmarks[20][1] > landmarks[18][1]
    
    if index_extended and middle_extended and ring_closed and pinky_closed:
        return 'H'
    index_extended = landmarks[8][1] < landmarks[6][1]
    other_fingers_closed = all([
        landmarks[12][1] > landmarks[10][1], 
        landmarks[16][1] > landmarks[14][1],
        landmarks[20][1] > landmarks[18][1],
    ])
    
    if index_extended and other_fingers_closed:
        return 'Z'
    
    return None
