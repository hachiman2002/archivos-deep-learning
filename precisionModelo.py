import tkinter as tk
from tkinter import messagebox
import math

def precision(N, k=0.0003):
    """Calcula la precisión del modelo basada en el número de imágenes."""
    return 1 - math.exp(-k * N)

def clasificar_modelo(precision):
    """Clasifica la calidad del modelo en bueno, medio o bajo."""
    if precision >= 0.8:
        return "bueno"
    elif 0.5 <= precision < 0.8:
        return "medio"
    else:
        return "bajo"

def evaluar_modelo():
    """Evalúa el modelo basado en el número de imágenes ingresado por el usuario."""
    try:
        N = int(entry.get())
        if N <= 0:
            raise ValueError
        prec = precision(N)
        clasificacion = clasificar_modelo(prec)
        result_text.set(f"Con {N} imágenes, la precisión del modelo es {prec:.2f}, lo cual es considerado {clasificacion}.")
    except ValueError:
        messagebox.showerror("Entrada inválida", "Por favor, ingrese un número entero positivo.")

# Crear la ventana principal
root = tk.Tk()
root.title("Evaluador de Modelo de IA")

# Crear y colocar los widgets
tk.Label(root, text="Ingrese el número de imágenes:").pack(pady=10)
entry = tk.Entry(root)
entry.pack(pady=10)
entry.focus()

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, wraplength=300)
result_label.pack(pady=10)

tk.Button(root, text="Evaluar Modelo", command=evaluar_modelo).pack(pady=10)

# Ejecutar la aplicación
root.mainloop()
