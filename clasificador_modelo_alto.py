import cv2
import numpy as np
import tensorflow as tf

# Cargar el modelo desde el sistema de archivos
model_dir = 'models/ssd_mobilenet_v1_coco_2018_01_28/saved_model'
model = tf.saved_model.load(model_dir)

# Obtener la firma de detección del modelo
infer = model.signatures['serving_default']

# Categorías de los objetos de COCO
category_index = {1: {'id': 1, 'name': 'person'}}

# Inicializar la cámara
cap = cv2.VideoCapture(0)

def load_image_into_numpy_array(image):
    return np.array(image).astype(np.uint8)

def detect_objects(frame):
    input_tensor = tf.convert_to_tensor(load_image_into_numpy_array(frame))
    input_tensor = input_tensor[tf.newaxis, ...]

    detections = infer(input_tensor)

    return detections

def draw_boxes(frame, detections):
    height, width, _ = frame.shape
    boxes = detections['detection_boxes'][0].numpy()
    scores = detections['detection_scores'][0].numpy()
    classes = detections['detection_classes'][0].numpy().astype(np.int64)

    for i in range(len(scores)):
        if scores[i] > 0.5 and classes[i] in category_index:
            box = boxes[i]
            class_name = category_index[classes[i]]['name']
            
            if class_name == 'person':  # Detectar personas
                y_min, x_min, y_max, x_max = box
                (left, right, top, bottom) = (x_min * width, x_max * width, y_min * height, y_max * height)
                cv2.rectangle(frame, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), 2)
                cv2.putText(frame, f'{class_name}: {scores[i]:.2f}', (int(left), int(top) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return frame

while True:
    # Capturar frame a frame
    ret, frame = cap.read()
    
    if not ret:
        break

    # Detectar objetos en la imagen
    detections = detect_objects(frame)
    
    # Dibujar recuadros alrededor de las personas detectadas
    frame = draw_boxes(frame, detections)
    
    # Mostrar el resultado
    cv2.imshow('Object Detection', frame)
    
    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
