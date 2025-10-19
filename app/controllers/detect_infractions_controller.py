from ultralytics import YOLO
import cv2
import os
import datetime
from typing import Dict, Any, List
import easyocr
import numpy as np
from sklearn.cluster import KMeans
import re 

reader = easyocr.Reader(['pt'], gpu=False) 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_dominant_color(image: np.ndarray) -> str:
    image = cv2.resize(image, (50, 50))
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    pixels = image_rgb.reshape(-1, 3)

    kmeans = KMeans(n_clusters=1, n_init=10, random_state=42)
    kmeans.fit(pixels)
    dominant_color = kmeans.cluster_centers_.astype(int)[0]

    color_map = {
        "Preto": [0, 0, 0],
        "Branco": [255, 255, 255],
        "Vermelho": [255, 0, 0],
        "Verde": [0, 128, 0],
        "Azul": [0, 0, 255],
        "Amarelo": [255, 255, 0],
        "Prata": [192, 192, 192],
        "Cinza": [128, 128, 128]
    }

    min_dist = float('inf')
    closest_color = "Desconhecida"
    for name, rgb in color_map.items():
        dist = np.linalg.norm(np.array(rgb) - dominant_color)
        if dist < min_dist:
            min_dist = dist
            closest_color = name
            
    return closest_color

def is_valid_plate(text: str) -> bool:
    text = re.sub(r'[\s-]', '', text).upper()
    
    pattern_mercosul = re.compile(r'^[A-Z]{3}\d[A-Z]\d{2}$')
    
    pattern_antigo = re.compile(r'^[A-Z]{3}\d{4}$')
    
    return bool(pattern_mercosul.match(text) or pattern_antigo.match(text))

def detect_infractions(model_path: str, image_path: str = None, video_path: str = None, use_webcam: bool = False) -> Dict[str, Any]:
    model = YOLO(model_path)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    if image_path:
        detections_list: List[Dict[str, Any]] = []
        results = model(image_path)
        
        filename = f"detection_result_{timestamp}.jpg"
        save_path = os.path.join(BASE_DIR, '..', 'images', filename) 

        for r in results:
            original_image = r.orig_img
            annotated_frame = r.plot()
            cv2.imwrite(save_path, annotated_frame)
            
            for box in r.boxes:
                confidence = float(box.conf[0])
                cls_id = int(box.cls[0])
                label = model.names[cls_id]
                
                if label.lower() == 'carro' and confidence >= 0.75:
                    coords = box.xyxy[0].tolist()
                    x1, y1, x2, y2 = map(int, coords)
                    
                    car_crop = original_image[y1:y2, x1:x2]
                    car_color = get_dominant_color(car_crop)
                    
                    plate_text = "Não identificada"
                    try:
                        plate_results = reader.readtext(car_crop)

                        valid_plates = []
                        for (bbox, text, prob) in plate_results:
                            if is_valid_plate(text):
                                valid_plates.append((text, prob))
                        
                        if valid_plates:
                            best_plate = max(valid_plates, key=lambda item: item[1])
                            plate_text = best_plate[0].strip().upper()

                    except Exception as e:
                        print(f"Erro ao processar OCR da placa: {e}")

                    detection_data = {
                        "label": label,
                        "confidence": confidence,
                        "color": car_color,
                        "license_plate": plate_text,
                        "bounding_box": {
                            "x1": coords[0], "y1": coords[1],
                            "x2": coords[2], "y2": coords[3]
                        }
                    }
                    detections_list.append(detection_data)

        print(f"Resultado da imagem salvo em: {save_path}")
        print(f"Detecções encontradas: {detections_list}")

        return {
            "file_path": save_path,
            "detections": detections_list
        }

    if use_webcam or video_path:
        pass

    raise ValueError("Você deve passar uma imagem, um vídeo ou usar a webcam.")