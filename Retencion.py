import tkinter as tk
from tkinter import font

# Parámetros de retención según normativa en Guatemala
ISR_THRESHOLD = 2800  # Umbral para retención de ISR en quetzales
IVA_THRESHOLD = 2500  # Umbral para retención de IVA en quetzales
BASE_THRESHOLD_HIGH_ISR = 30000  # Umbral para aplicar 7% de retención en el excedente de Q30,000
ISR_RATE_LOW = 0.05  # Tasa de retención del ISR (5%)
ISR_RATE_HIGH = 0.07  # Tasa de retención del ISR en el excedente (7%)
IVA_RATE = 0.12  # Tasa de IVA (12%)

# Función para calcular retenciones
def calcular_retencion():
    try:
        # Obtener el monto ingresado y calcular la base
        monto = float(entry.get())
        base = monto / 1.12  
        
        # Inicializar variables de retención
        retencion_isr = 0
        retencion_iva = 0

        # Calcular retención de ISR
        if monto >= ISR_THRESHOLD:
            if base >= BASE_THRESHOLD_HIGH_ISR:
                # Aplicar 5% sobre los primeros 30,000 y 7% sobre el excedente
                retencion_isr = (BASE_THRESHOLD_HIGH_ISR * ISR_RATE_LOW) + ((base - BASE_THRESHOLD_HIGH_ISR) * ISR_RATE_HIGH)
                detalle_isr_label.config(
                    text=f"Retención ISR: = Q{retencion_isr:.2f}"
                )
            else:
                # Aplicar 5% si la base es menor a 30,000
                retencion_isr = base * ISR_RATE_LOW
                detalle_isr_label.config(text=f"Retención ISR: Q{retencion_isr:.2f}")
        else:
            detalle_isr_label.config(text=f"No aplica retención ISR. Aplica a partir de Q{ISR_THRESHOLD}.")

        # Verificar si aplica retención de IVA
        if monto >= IVA_THRESHOLD and iva_var.get():  # Si el checkbox de IVA está seleccionado 
            retencion_iva = (base * IVA_RATE) * 0.15 #15% Sobre el IVA de la factura. Recordar que este es el calculo para Contribuyentes Especiales 
            detalle_iva_label.config(text=f"Retención IVA: Q{retencion_iva:.2f}")
        else:
            detalle_iva_label.config(text=f"No aplica retención IVA. Aplica a partir de Q{IVA_THRESHOLD}.")

        # Monto final después de retenciones
        monto_final = monto - (retencion_isr + retencion_iva)
        
        # Mostrar el monto final con retenciones aplicadas
        resultado_label.config(text="Monto a Pagar (menos retenciones):")
        resultado_num_label.config(text=f"Q{monto_final:.2f}", fg="#98FB98") 
    except ValueError:
        resultado_label.config(text="Por favor, ingresa un monto válido.")
        resultado_num_label.config(text="")
        detalle_isr_label.config(text="")
        detalle_iva_label.config(text="")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Cálculo de Retenciones")
root.geometry("550x550")  # Tamaño de la ventana
root.configure(bg="#2e2e2e")  # Fondo en gris oscuro

font_large = font.Font(family="Arial", size=14, weight="bold")
font_result = font.Font(family="Arial", size=16, weight="bold", underline=True)

# Etiqueta y entrada para el monto
label = tk.Label(root, text="Ingresa el monto (Q):", fg="white", bg="#2e2e2e", font=font_large)
label.pack(pady=10)

entry = tk.Entry(root, font=font_large)
entry.pack(pady=5)

# Checkbox para incluir retención de IVA
iva_var = tk.BooleanVar()
iva_checkbox = tk.Checkbutton(root, text="Incluir retención de IVA", variable=iva_var, fg="white", bg="#2e2e2e", selectcolor="#2e2e2e", font=font_large)
iva_checkbox.pack(pady=5)

# Botón para calcular las retenciones
button = tk.Button(root, text="Calcular Retención", command=calcular_retencion, fg="white", bg="#4d4d4d", font=font_large)
button.pack(pady=10)

# Etiquetas para mostrar el detalle de cada retención
detalle_isr_label = tk.Label(root, text="", fg="white", bg="#2e2e2e", font=font_large)
detalle_isr_label.pack(pady=5)

detalle_iva_label = tk.Label(root, text="", fg="white", bg="#2e2e2e", font=font_large)
detalle_iva_label.pack(pady=5)

# Etiquetas para mostrar el monto final
resultado_label = tk.Label(root, text="", fg="white", bg="#2e2e2e", font=font_large)
resultado_label.pack(pady=5)

# Etiqueta para el monto resultante 
resultado_num_label = tk.Label(root, text="", fg="#98FB98", bg="#2e2e2e", font=font_result)
resultado_num_label.pack(pady=5)

# Ejecuta la aplicación
root.mainloop()
