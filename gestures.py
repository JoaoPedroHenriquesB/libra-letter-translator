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

