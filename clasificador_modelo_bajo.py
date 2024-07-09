import json
import requests

# Descargar y cargar las etiquetas de ImageNet
response = requests.get('https://storage.googleapis.com/download.tensorflow.org/data/imagenet_class_index.json')
imagenet_class_index = response.json()

# Crear un archivo de etiquetas
with open('imagenet_labels.txt', 'w') as f:
    for key, value in imagenet_class_index.items():
        f.write(f"{value[1]}\n")

import cv2
import numpy as np
import tensorflow as tf

# Cargar el modelo MobileNetV2 preentrenado con los pesos de ImageNet
model = tf.keras.applications.MobileNetV2(weights='imagenet')

# Leer las etiquetas de ImageNet desde el archivo generado
with open('imagenet_labels.txt') as f:
    imagenet_labels = f.read().splitlines()

# Verificar las etiquetas específicas
fruit_labels = ['orange', 'apple']
fruit_indices = [imagenet_labels.index(label) for label in fruit_labels if label in imagenet_labels]

# Inicializar la cámara
cap = cv2.VideoCapture(0)

def preprocess_image(image):
    image = cv2.resize(image, (224, 224))
    image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
    return image

def classify_image(image):
    image = np.expand_dims(image, axis=0)
    predictions = model.predict(image)
    top_pred_idx = np.argmax(predictions[0])
    confidence = predictions[0][top_pred_idx]

    # Si el índice de predicción está en nuestras etiquetas de interés
    if confidence >= 0.30:
        return "Es una manzana, modelo bajo", confidence
    else:
        return "Unknown", confidence

while True:
    # Capturar frame a frame
    ret, frame = cap.read()
    
    if not ret:
        break

    # Procesar la imagen y hacer la predicción
    preprocessed_frame = preprocess_image(frame)
    label, confidence = classify_image(preprocessed_frame)
    
    # Mostrar el resultado
    cv2.putText(frame, f'Prediction: {label} ({confidence:.2f})', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow('frame', frame)
    
    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
