# import cv2
# import easyocr
# import numpy as np
# from detector.PlateDetector import PlateDetector # Importando o DETECTOR do seu projeto
# import argparse

# # --- CONFIGURAÇÃO INICIAL ---
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="caminho para a imagem de entrada")
# args = vars(ap.parse_args())

# # --- PASSO 1: INICIALIZAÇÃO DO DETECTOR (JÁ CORRIGIDO) ---

# print("[INFO] Carregando o detector de placas do projeto AccessALPR...")
# PATH_CONFIG = "detector/config/yolov3-plates.cfg"
# PATH_WEIGHTS = "detector/weights/detector-w.pth"
# plate_detector = PlateDetector(cfg=PATH_CONFIG, weights_path=PATH_WEIGHTS, conf_thresh=0.5)

# # Carrega a imagem de entrada usando OpenCV
# original_image = cv2.imread(args["image"])
# if original_image is None:
#     print(f"[ERRO] Não foi possível carregar a imagem em: {args['image']}")
#     exit()

# # --- PASSO 2: DETECÇÃO DAS COORDENADAS (MÉTODO CORRETO) ---

# print("[INFO] Procurando pela placa na imagem...")
# # Usa o método .predict() para obter as coordenadas da caixa delimitadora (bounding box)
# # A função retorna uma lista de coordenadas [[x1, y1, x2, y2, conf]]
# bounding_boxes = plate_detector.predict(original_image)

# # --- PASSO 3: RECORTE MANUAL E RECONHECIMENTO COM EASYOCR ---

# if len(bounding_boxes) > 0:
#     print(f"[INFO] {len(bounding_boxes)} placa(s) encontrada(s). Realizando OCR com EasyOCR...")

#     reader = easyocr.Reader(['pt', 'en'], gpu=False)

#     # Itera sobre cada caixa de coordenadas encontrada
#     for i, bbox in enumerate(bounding_boxes):
#         # Extrai as coordenadas
#         x1, y1, x2, y2, conf = bbox
        
#         # Converte as coordenadas para inteiros
#         x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

#         # **AQUI ESTÁ A MÁGICA: Recorta a placa da imagem original usando as coordenadas**

#         plate_image = original_image[y1:y2, x1:x2]
#         # Verifica se o recorte não está vazio
#         if plate_image.size > 0:
#             # Converte para tons de cinza para melhorar o OCR
#             plate_image_large = cv2.resize(plate_image, (0, 0), fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
#             # --------------------------------------------------------------------

#             # Converte a imagem GRANDE para tons de cinza para melhorar o OCR
#             gray_plate = cv2.cvtColor(plate_image_large, cv2.COLOR_BGR2GRAY)
            
#             # Usa EasyOCR para ler o texto
#             result = reader.readtext(gray_plate, detail=1, paragraph=False)

#             if len(result) > 0:
#                 plate_text = result[0][1]
#                 confidence = result[0][2]

#                 print(f"\n--- Placa {i+1} ---")
#                 print(f"Texto Reconhecido: {plate_text.upper()}")
#                 print(f"Confiança do OCR: {confidence:.4f}")

#                 # Mostra a imagem da placa que foi lida
#                 cv2.imshow(f"Placa Recortada {i+1}", plate_image)
#             else:
#                 print(f"[AVISO] OCR não conseguiu ler texto na placa {i+1}.")
#         else:
#             print(f"[AVISO] Recorte da placa {i+1} resultou em uma imagem vazia.")

#     print("\n[INFO] Pressione qualquer tecla nas janelas de imagem para fechar.")
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# else:
#     print("[INFO] Nenhuma placa foi detectada na imagem.")