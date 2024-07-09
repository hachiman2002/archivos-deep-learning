#https://www.kaggle.com/datasets/jessicali9530/lfw-dataset
import os
import matplotlib.pyplot as plt

def contar_imagenes(directorio):
    total_imagenes = 0
    for ruta_directorio, _, archivos in os.walk(directorio):
        for archivo in archivos:
            if archivo.endswith(".jpg") or archivo.endswith(".png") or archivo.endswith(".jpeg"):
                total_imagenes += 1
    
    return total_imagenes

# Directorios que quieres contar
directorios = [
    r'C:\Users\Graciany\Desktop\5to semestre\Calculo\proyecto final\AppV1\person\lfw-deepfunneled\lfw-deepfunneled',
    r'C:\Users\Graciany\Desktop\5to semestre\Calculo\proyecto final\AppV1\apple'
]

# Contar imágenes en cada directorio y evaluar el nivel de entrenamiento
resultados = []
nombres_carpetas = []
for directorio in directorios:
    total = contar_imagenes(directorio)
    resultados.append(total)
    nombres_carpetas.append(os.path.basename(directorio))
    
    # Evaluar nivel de entrenamiento
    if total < 100:
        nivel_entrenamiento = "bajo"
    elif total < 2350:
        nivel_entrenamiento = "medio"
    else:
        nivel_entrenamiento = "alto"
    
    print(f"Total de imágenes en {directorio}: {total}. Nivel de entrenamiento: {nivel_entrenamiento}")

# Graficar los resultados
plt.figure(figsize=(8, 6))
bars = plt.bar(nombres_carpetas, resultados, color='skyblue')
plt.xlabel('Directorios')
plt.ylabel('Número de Imágenes')
plt.title('Número de Imágenes por Carpeta')

# Añadir las cifras encima de las barras
for bar, resultado in zip(bars, resultados):
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, f'{resultado}', ha='center', va='bottom', fontsize=10)

plt.xticks(rotation=15)
plt.tight_layout()

# Mostrar mensaje sobre el nivel de entrenamiento
for nombre, resultado in zip(nombres_carpetas, resultados):
    if resultado < 100:
        plt.text(nombres_carpetas.index(nombre), resultado - 50, "Entrenamiento bajo", color='red', fontsize=10, ha='center')
    elif resultado < 500:
        plt.text(nombres_carpetas.index(nombre), resultado - 50, "Entrenamiento medio", color='orange', fontsize=10, ha='center')
    else:
        plt.text(nombres_carpetas.index(nombre), resultado - 50, "Entrenamiento alto", color='green', fontsize=10, ha='center')

plt.show()
