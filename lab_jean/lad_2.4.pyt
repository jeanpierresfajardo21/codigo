import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Valores iniciales
R0 = 1000      # ohmios
C0 = 1e-6      # faradios
V0 = 5         # voltios

# Tiempo
t = np.linspace(0, 0.01, 1000)

# Funciones
def carga(t, R, C, V):
    return V * (1 - np.exp(-t/(R*C)))

def descarga(t, R, C, V):
    return V * np.exp(-t/(R*C))

# Crear figura
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.35)

# Graficas iniciales
line1, = ax.plot(t, carga(t, R0, C0, V0), label="Carga")
line2, = ax.plot(t, descarga(t, R0, C0, V0), label="Descarga")

ax.set_title("Carga y descarga de un condensador")
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Voltaje (V)")
ax.legend()

# Sliders
ax_R = plt.axes([0.1, 0.25, 0.8, 0.03])
ax_C = plt.axes([0.1, 0.18, 0.8, 0.03])
ax_V = plt.axes([0.1, 0.11, 0.8, 0.03])

slider_R = Slider(ax_R, 'Resistencia (Ω)', 100, 10000, valinit=R0)
slider_C = Slider(ax_C, 'Capacitancia (F)', 1e-7, 1e-5, valinit=C0)
slider_V = Slider(ax_V, 'Voltaje (V)', 1, 10, valinit=V0)

# Actualización
def update(val):
    R = slider_R.val
    C = slider_C.val
    V = slider_V.val

    line1.set_ydata(carga(t, R, C, V))
    line2.set_ydata(descarga(t, R, C, V))

    fig.canvas.draw_idle()

# Conectar sliders
slider_R.on_changed(update)
slider_C.on_changed(update)
slider_V.on_changed(update)

plt.show()