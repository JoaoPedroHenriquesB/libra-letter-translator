#!/usr/bin/env python3
"""
Configurações avançadas para o sistema de detecção de movimentos em Libras
Este arquivo contém parâmetros ajustáveis e funções de otimização
"""

# =============================================================================
# PARÂMETROS DE CONFIGURAÇÃO
# =============================================================================

# Parâmetros de movimento para letra J
J_MOVEMENT_CONFIG = {
    'min_sequence_length': 5,
    'down_threshold': 0.05,      # Movimento mínimo para baixo
    'left_threshold': 0.02,      # Movimento mínimo para esquerda
    'landmark_index': 20         # Dedo mindinho
}

# Parâmetros de movimento para letra H
H_MOVEMENT_CONFIG = {
    'min_sequence_length': 5,
    'horizontal_threshold': 0.08,  # Movimento horizontal mínimo
    'vertical_stability': 0.05,    # Tolerância para estabilidade vertical
    'landmark_indices': [8, 12]    # Indicador e médio
}

# Parâmetros de movimento para letra Z
Z_MOVEMENT_CONFIG = {
    'min_sequence_length': 8,
    'diagonal_threshold': 0.03,    # Movimento diagonal mínimo
    'horizontal_threshold': 0.05,  # Movimento horizontal mínimo
    'vertical_tolerance': 0.03,    # Tolerância para movimento horizontal
    'landmark_index': 8            # Indicador
}

# Parâmetros de movimento para letra X
X_MOVEMENT_CONFIG = {
    'min_sequence_length': 4,
    'down_threshold': 0.02,        # Movimento para baixo
    'up_threshold': 0.01,          # Movimento para cima
    'horizontal_tolerance': 0.03,  # Tolerância horizontal
    'landmark_index': 8            # Indicador
}

# Parâmetros gerais do sistema
SYSTEM_CONFIG = {
    'sequence_length': 15,                    # Frames para análise
    'movement_confirmation_frames': 5,        # Frames para confirmar
    'detection_confidence': 0.7,              # Confiança do MediaPipe
    'tracking_confidence': 0.5,               # Rastreamento do MediaPipe
    'static_detection_threshold': 1.2         # Limiar para detecção estática
}

# =============================================================================
# FUNÇÕES DE CONFIGURAÇÃO AVANÇADA
# =============================================================================

def configure_mediapipe_hands(
    detection_confidence=0.7,
    tracking_confidence=0.5,
    max_num_hands=1,
    static_image_mode=False
):
    """
    Configura o MediaPipe Hands com parâmetros personalizados
    
    Args:
        detection_confidence: Confiança mínima para detecção (0.0-1.0)
        tracking_confidence: Confiança mínima para rastreamento (0.0-1.0)
        max_num_hands: Número máximo de mãos a detectar
        static_image_mode: True para imagens estáticas, False para vídeo
    
    Returns:
        Objeto MediaPipe Hands configurado
    """
    import mediapipe as mp
    
    mp_hands = mp.solutions.hands
    return mp_hands.Hands(
        static_image_mode=static_image_mode,
        max_num_hands=max_num_hands,
        min_detection_confidence=detection_confidence,
        min_tracking_confidence=tracking_confidence
    )

def optimize_for_performance():
    """
    Retorna configurações otimizadas para performance
    """
    return {
        'sequence_length': 10,                # Reduzido para menos processamento
        'movement_confirmation_frames': 3,    # Resposta mais rápida
        'detection_confidence': 0.6,          # Menos rigoroso
        'tracking_confidence': 0.4,           # Menos rigoroso
    }

def optimize_for_accuracy():
    """
    Retorna configurações otimizadas para precisão
    """
    return {
        'sequence_length': 20,                # Mais frames para análise
        'movement_confirmation_frames': 8,    # Mais confirmação
        'detection_confidence': 0.8,          # Mais rigoroso
        'tracking_confidence': 0.7,           # Mais rigoroso
    }

def optimize_for_lighting_conditions(lighting='normal'):
    """
    Ajusta configurações baseado nas condições de iluminação
    
    Args:
        lighting: 'low', 'normal', 'bright'
    """
    if lighting == 'low':
        return {
            'detection_confidence': 0.5,      # Menos rigoroso para pouca luz
            'tracking_confidence': 0.3,
            'movement_confirmation_frames': 7  # Mais confirmação
        }
    elif lighting == 'bright':
        return {
            'detection_confidence': 0.8,      # Mais rigoroso para boa luz
            'tracking_confidence': 0.7,
            'movement_confirmation_frames': 4  # Menos confirmação necessária
        }
    else:  # normal
        return SYSTEM_CONFIG

# =============================================================================
# FUNÇÕES DE CALIBRAÇÃO
# =============================================================================

def calibrate_movement_thresholds(hand_size='medium'):
    """
    Calibra os thresholds baseado no tamanho da mão
    
    Args:
        hand_size: 'small', 'medium', 'large'
    """
    multiplier = {
        'small': 0.7,
        'medium': 1.0,
        'large': 1.3
    }.get(hand_size, 1.0)
    
    calibrated_config = {}
    
    for letter_config in [J_MOVEMENT_CONFIG, H_MOVEMENT_CONFIG, 
                         Z_MOVEMENT_CONFIG, X_MOVEMENT_CONFIG]:
        calibrated = letter_config.copy()
        for key, value in calibrated.items():
            if 'threshold' in key and isinstance(value, (int, float)):
                calibrated[key] = value * multiplier
        calibrated_config.update(calibrated)
    
    return calibrated_config

def auto_calibrate_from_landmarks(landmarks_history):
    """
    Calibração automática baseada no histórico de landmarks
    
    Args:
        landmarks_history: Lista de sequências de landmarks
    """
    import numpy as np
    
    if not landmarks_history:
        return SYSTEM_CONFIG
    
    variations = []
    for sequence in landmarks_history:
        if len(sequence) > 1:
            for i in range(1, len(sequence)):
                prev_frame = np.array(sequence[i-1])
                curr_frame = np.array(sequence[i])
                variation = np.mean(np.abs(curr_frame - prev_frame))
                variations.append(variation)
    
    if variations:
        avg_variation = np.mean(variations)
        adjustment_factor = max(0.5, min(2.0, avg_variation * 10))
        
        return {
            'j_down_threshold': J_MOVEMENT_CONFIG['down_threshold'] * adjustment_factor,
            'j_left_threshold': J_MOVEMENT_CONFIG['left_threshold'] * adjustment_factor,
            'h_horizontal_threshold': H_MOVEMENT_CONFIG['horizontal_threshold'] * adjustment_factor,
            'z_diagonal_threshold': Z_MOVEMENT_CONFIG['diagonal_threshold'] * adjustment_factor,
            'x_down_threshold': X_MOVEMENT_CONFIG['down_threshold'] * adjustment_factor,
        }
    
    return {}

# =============================================================================
# FUNÇÕES DE MONITORAMENTO
# =============================================================================

class PerformanceMonitor:
    """Monitora performance do sistema de detecção"""
    
    def __init__(self):
        self.detection_times = []
        self.false_positives = 0
        self.true_positives = 0
        self.frame_count = 0
    
    def record_detection_time(self, time_ms):
        """Registra tempo de detecção"""
        self.detection_times.append(time_ms)
        if len(self.detection_times) > 100:
            self.detection_times.pop(0)
    
    def record_detection_result(self, is_correct):
        """Registra resultado da detecção"""
        if is_correct:
            self.true_positives += 1
        else:
            self.false_positives += 1
    
    def get_stats(self):
        """Retorna estatísticas de performance"""
        if not self.detection_times:
            return {}
        
        import numpy as np
        
        avg_time = np.mean(self.detection_times)
        max_time = np.max(self.detection_times)
        min_time = np.min(self.detection_times)
        
        total_detections = self.true_positives + self.false_positives
        accuracy = (self.true_positives / total_detections * 100) if total_detections > 0 else 0
        
        return {
            'avg_detection_time_ms': avg_time,
            'max_detection_time_ms': max_time,
            'min_detection_time_ms': min_time,
            'accuracy_percent': accuracy,
            'total_detections': total_detections,
            'fps_estimate': 1000 / avg_time if avg_time > 0 else 0
        }

# =============================================================================
# FUNÇÕES DE DEBUG
# =============================================================================

def debug_landmarks_sequence(sequence, letter_type):
    """
    Função de debug para visualizar sequência de landmarks
    
    Args:
        sequence: Sequência de landmarks
        letter_type: Tipo de letra sendo analisada
    """
    if not sequence:
        print(f"DEBUG {letter_type}: Sequência vazia")
        return
    
    print(f"\nDEBUG {letter_type}:")
    print(f"  Tamanho da sequência: {len(sequence)}")
    
    if letter_type == 'J':
        landmark_idx = 20
        start_pos = sequence[0][landmark_idx]
        end_pos = sequence[-1][landmark_idx]
        
        print(f"  Posição inicial (mindinho): {start_pos}")
        print(f"  Posição final (mindinho): {end_pos}")
        print(f"  Movimento Y: {end_pos[1] - start_pos[1]:.3f}")
        print(f"  Movimento X: {end_pos[0] - start_pos[0]:.3f}")
        
    elif letter_type == 'H':
        for i, landmark_idx in enumerate([8, 12]):
            start_pos = sequence[0][landmark_idx]
            end_pos = sequence[-1][landmark_idx]
            finger_name = "Indicador" if i == 0 else "Médio"
            
            print(f"  {finger_name} - Início: {start_pos}")
            print(f"  {finger_name} - Fim: {end_pos}")
            print(f"  {finger_name} - Movimento X: {end_pos[0] - start_pos[0]:.3f}")

def create_debug_config():
    """Cria configuração com debug habilitado"""
    config = SYSTEM_CONFIG.copy()
    config.update({
        'debug_mode': True,
        'show_landmarks': True,
        'print_detection_info': True,
        'save_debug_frames': False
    })
    return config

# =============================================================================
# EXEMPLO DE USO DAS CONFIGURAÇÕES
# =============================================================================

def exemplo_configuracao_personalizada():
    config_pouca_luz = optimize_for_lighting_conditions('low')
    config_mao_pequena = calibrate_movement_thresholds('small')
    config_precisao = optimize_for_accuracy()
    config_final = {**SYSTEM_CONFIG, **config_pouca_luz, **config_precisao}
    
    print("Configuração personalizada criada:")
    for key, value in config_final.items():
        print(f"  {key}: {value}")
    
    return config_final

if __name__ == "__main__":
    exemplo_configuracao_personalizada()