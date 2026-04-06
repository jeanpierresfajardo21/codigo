import cv2 # para procesamiento de imágenes
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# --- CONFIGURACIÓN PARA MOSTRAR TODO EN CONSOLA ---
pd.set_option('display.max_rows', None)  # Muestra todas las filas
pd.set_option('display.max_columns', None) # Muestra todas las columnas
pd.set_option('display.width', 1000)      # Evita saltos de línea en la tabla

def extraer_datos(ruta_archivo, nombre_logo):
    """Procesa la imagen y retorna el DataFrame de puntos y los arreglos X, Y."""
    img = cv2.imread(ruta_archivo, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: No se pudo leer {ruta_archivo}")
        return None, None, None

    # 1. Preprocesamiento para precisión
    blur = cv2.GaussianBlur(img, (3, 3), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # 2. Cerrar contornos (Mejora el logo de Chevrolet)
    kernel = np.ones((3,3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # 3. Extracción de contornos (CHAIN_APPROX_NONE para tener todos los puntos)
    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contornos:
        return None, None, None
    
    cnt = max(contornos, key=cv2.contourArea)
    puntos = cnt.reshape(-1, 2)
    x = puntos[:, 0]
    y = puntos[:, 1]

    # Crear DataFrame para la tabla
    df = pd.DataFrame(puntos, columns=[f'{nombre_logo}_X', f'{nombre_logo}_Y'])
    
    return df, x, y

# --- INICIO DEL PROGRAMA ---

img1 = "chevrolet.png"
img2 = "ferrari.png"
# Detectar ruta del script para evitar errores de carpeta
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_chev = os.path.join(directorio_actual, img1)
ruta_mazda = os.path.join(directorio_actual, img2)

try:
    print("Iniciando procesamiento de logos...")
    
    # Extraer información
    df_c, x_c, y_c = extraer_datos(ruta_chev, "CHEVROLET")
    df_m, x_m, y_m = extraer_datos(ruta_mazda, "FERRARI")

    if df_c is not None and df_m is not None:
        
        # --- PARTE 1: TABLA EN CONSOLA ---
        # Concatenamos horizontalmente
        tabla_comparativa = pd.concat([df_c, df_m], axis=1)
        
        print("\n" + "="*50)
        print("   TABLA COMPLETA DE COORDENADAS (LADO A LADO)")
        print("="*50)
        print(tabla_comparativa.to_string(index=True, na_rep="-"))
        print("="*50)
        print(f"Puntos {img1}: {len(x_c)} | Puntos {img2}: {len(x_m)}")

        # --- PARTE 2: GRÁFICA ---
        plt.figure(figsize=(12, 5))
        
        # Gráfica Chevrolet
        plt.subplot(1, 2, 1)
        plt.plot(x_c, -y_c, color='#C49C48', linewidth=2.5, label='Contorno Chevrolet')
        plt.title(f"Extracción: Logo {img1}", fontsize=12, fontweight='bold')
        plt.axis('equal') # Mantiene la proporción real
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()

        # Gráfica Mazda
        plt.subplot(1, 2, 2)
        plt.plot(x_m, -y_m, color='black', linewidth=2.5, label='Contorno Ferrari')
        plt.title(f"Extracción: Logo {img2}", fontsize=12, fontweight='bold')
        plt.axis('equal') # Evita que el círculo se vea como óvalo
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()

        plt.tight_layout() 
        plt.show()

    else:
        print("Verifica que las imágenes estén en la misma carpeta que el script.")

except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")