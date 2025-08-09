#!/usr/bin/env python3
"""
Teste das funções de detecção de movimento para letras em Libras
"""

import numpy as np
from gestures import (
    detect_j_movement, 
    detect_h_movement, 
    detect_z_movement, 
    detect_x_movement,
    get_hand_shape_for_movement,
    detect_movement_letter
)

def create_mock_landmarks(positions):
    """Cria landmarks simulados para teste"""
    landmarks = [[0.5, 0.5, 0.0] for _ in range(21)]
    
    for landmark_idx, pos in positions.items():
        landmarks[landmark_idx] = pos
    
    return landmarks

def test_j_movement():
    """Testa detecção do movimento da letra J"""
    print("Testando movimento da letra J...")

    sequence = []

    for i in range(3):
        landmarks = create_mock_landmarks({
            20: [0.6, 0.3, 0.0],  
            8: [0.5, 0.6, 0.0],   
            12: [0.5, 0.6, 0.0],  
            16: [0.5, 0.6, 0.0], 
        })
        sequence.append(landmarks)
    
    for i in range(3):
        y_pos = 0.3 + (i * 0.1)  
        landmarks = create_mock_landmarks({
            20: [0.6, y_pos, 0.0],
            8: [0.5, 0.6, 0.0],
            12: [0.5, 0.6, 0.0],
            16: [0.5, 0.6, 0.0],
        })
        sequence.append(landmarks)
    

    for i in range(3):
        x_pos = 0.6 - (i * 0.05)
        landmarks = create_mock_landmarks({
            20: [x_pos, 0.6, 0.0],
            8: [0.5, 0.6, 0.0],
            12: [0.5, 0.6, 0.0],
            16: [0.5, 0.6, 0.0],
        })
        sequence.append(landmarks)
    
    result = detect_j_movement(sequence)
    print(f"Resultado J: {'PASSOU' if result else 'FALHOU'}")
    return result

def test_h_movement():
    """Testa detecção do movimento da letra H"""
    print("Testando movimento da letra H...")
    
    sequence = []
    

    for i in range(8):
        x_pos = 0.7 - (i * 0.02)
        landmarks = create_mock_landmarks({
            8: [x_pos, 0.4, 0.0],      
            12: [x_pos, 0.5, 0.0],     
            16: [0.5, 0.7, 0.0],       
            20: [0.5, 0.7, 0.0],       
        })
        sequence.append(landmarks)
    
    result = detect_h_movement(sequence)
    print(f"Resultado H: {'✓ PASSOU' if result else '✗ FALHOU'}")
    return result

def test_z_movement():
    """Testa detecção do movimento da letra Z"""
    print("Testando movimento da letra Z...")
    
    sequence = []
    for i in range(3):
        x_pos = 0.3 + (i * 0.02)
        y_pos = 0.3 + (i * 0.02)
        landmarks = create_mock_landmarks({
            8: [x_pos, y_pos, 0.0],    
            12: [0.5, 0.7, 0.0],      
            16: [0.5, 0.7, 0.0],      
            20: [0.5, 0.7, 0.0],      
        })
        sequence.append(landmarks)
    
    for i in range(3):
        x_pos = 0.36 - (i * 0.03)
        landmarks = create_mock_landmarks({
            8: [x_pos, 0.36, 0.0],
            12: [0.5, 0.7, 0.0],
            16: [0.5, 0.7, 0.0],
            20: [0.5, 0.7, 0.0],
        })
        sequence.append(landmarks)
    
    for i in range(3):
        x_pos = 0.27 + (i * 0.02)
        y_pos = 0.36 + (i * 0.02)
        landmarks = create_mock_landmarks({
            8: [x_pos, y_pos, 0.0],
            12: [0.5, 0.7, 0.0],
            16: [0.5, 0.7, 0.0],
            20: [0.5, 0.7, 0.0],
        })
        sequence.append(landmarks)
    
    result = detect_z_movement(sequence)
    print(f"Resultado Z: {'✓ PASSOU' if result else '✗ FALHOU'}")
    return result

def test_x_movement():
    """Testa detecção do movimento da letra X"""
    print("Testando movimento da letra X...")
    
    sequence = []
    
    
    positions = [
        [0.5, 0.4, 0.0], 
        [0.5, 0.45, 0.0], 
        [0.5, 0.47, 0.0], 
        [0.5, 0.43, 0.0], 
        [0.5, 0.41, 0.0], 
    ]
    
    for pos in positions:
        landmarks = create_mock_landmarks({
            8: pos,                    
            12: [0.5, 0.7, 0.0],      
            16: [0.5, 0.7, 0.0],      
            20: [0.5, 0.7, 0.0],     
        })
        sequence.append(landmarks)
    
    result = detect_x_movement(sequence)
    print(f"Resultado X: {'✓ PASSOU' if result else '✗ FALHOU'}")
    return result

def test_hand_shapes():
    """Testa identificação das formas da mão"""
    print("\nTestando identificação de formas da mão...")
    class MockHandLandmarks:
        def __init__(self, landmarks):
            self.landmark = [MockLandmark(pos) for pos in landmarks]
    
    class MockLandmark:
        def __init__(self, pos):
            self.x, self.y, self.z = pos
    
    j_landmarks = create_mock_landmarks({
        20: [0.6, 0.2, 0.0],  
        19: [0.6, 0.3, 0.0],  
        8: [0.5, 0.6, 0.0],   
        6: [0.5, 0.5, 0.0],   
        12: [0.5, 0.6, 0.0],  
        10: [0.5, 0.5, 0.0],  
        16: [0.5, 0.6, 0.0], 
        14: [0.5, 0.5, 0.0],
    })
    
    mock_j = MockHandLandmarks(j_landmarks)
    j_shape = get_hand_shape_for_movement(mock_j)
    print(f"Forma J: {'✓ PASSOU' if j_shape == 'J' else '✗ FALHOU'} (detectado: {j_shape})")
    h_landmarks = create_mock_landmarks({
        8: [0.5, 0.2, 0.0],  
        6: [0.5, 0.3, 0.0],   
        12: [0.5, 0.2, 0.0], 
        10: [0.5, 0.3, 0.0], 
        16: [0.5, 0.6, 0.0],  
        14: [0.5, 0.5, 0.0],  
        20: [0.5, 0.6, 0.0],  
        18: [0.5, 0.5, 0.0],  
    })
    
    mock_h = MockHandLandmarks(h_landmarks)
    h_shape = get_hand_shape_for_movement(mock_h)
    print(f"Forma H: {'PASSOU' if h_shape == 'H' else 'FALHOU'} (detectado: {h_shape})")

def main():
    """Executa todos os testes"""
    print("=== TESTE DO SISTEMA DE DETECÇÃO DE MOVIMENTOS ===\n")
    
    tests_passed = 0
    total_tests = 0
    movement_tests = [
        test_j_movement,
        test_h_movement,
        test_z_movement,
        test_x_movement
    ]
    
    for test_func in movement_tests:
        total_tests += 1
        if test_func():
            tests_passed += 1
        print()
    
    test_hand_shapes()
    
    print(f"\n=== RESULTADO FINAL ===")
    print(f"Testes de movimento: {tests_passed}/{len(movement_tests)} passaram")
    print(f"Taxa de sucesso: {(tests_passed/len(movement_tests)*100):.1f}%")
    
    if tests_passed == len(movement_tests):
        print("Todos os testes de movimento passaram!")
    else:
        print("Alguns testes falharam. Verifique os parâmetros.")

if __name__ == "__main__":
    main()