import tkinter as tk
import time
import threading
import random  # para simular valores

# Función para simular sensor
def leer_sensor():
    # Simula un valor de sensor (por ejemplo temperatura)
    return round(random.uniform(20, 30), 2)

# Función que ejecuta la lectura durante cierto tiempo
def iniciar_lectura():
    try:
        duracion = int(entry_tiempo.get())
    except:
        label_resultado.config(text="Tiempo inválido")
        return

    def proceso():
        inicio = time.time()
        while time.time() - inicio < duracion:
            valor = leer_sensor()

            # Actualización segura de Tkinter
            ventana.after(0, lambda v=valor: label_resultado.config(text=f"Lectura: {v}"))

            time.sleep(1)

        ventana.after(0, lambda: label_resultado.config(text="Finalizado"))

    threading.Thread(target=proceso, daemon=True).start()

# Crear ventana
ventana = tk.Tk()
ventana.title("Lectura Simulada")

# Label
label_resultado = tk.Label(ventana, text="Lectura: ---", font=("Arial", 14))
label_resultado.pack(pady=10)

# Entry
entry_tiempo = tk.Entry(ventana)
entry_tiempo.pack(pady=5)
entry_tiempo.insert(0, "5")

# Botón
boton = tk.Button(ventana, text="Iniciar lectura", command=iniciar_lectura)
boton.pack(pady=10)

ventana.mainloop()