import tkinter as tk
from tkinter import filedialog, messagebox
import pywhatkit as kit
import datetime
import time

numeros = []

def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, "r") as f:
            global numeros
            numeros = f.read().splitlines()
            texto_numeros.delete("1.0", tk.END)
            texto_numeros.insert(tk.END, "\n".join(numeros))
            messagebox.showinfo("Éxito", "Números cargados correctamente.")

def enviar_mensajes():
    mensaje = caja_mensaje.get("1.0", tk.END).strip()
    if not mensaje or not numeros:
        messagebox.showwarning("Error", "Debes escribir un mensaje y cargar números.")
        return

    # Calcular la hora inicial (2 minutos en el futuro para dar tiempo de cargar WhatsApp Web)
    hora_envio = datetime.datetime.now() + datetime.timedelta(minutes=2)

    for numero in numeros:
        hora = hora_envio.hour
        minuto = hora_envio.minute

        try:
            kit.sendwhatmsg(
                numero,
                mensaje,
                hora,
                minuto,
                wait_time=20,
                tab_close=True,
                close_time=3
            )
            print(f"Mensaje programado para {numero} a las {hora}:{minuto:02d}")
            time.sleep(25)  # Espera entre cada envío para no colapsar el navegador
        except Exception as e:
            print(f"Error enviando a {numero}: {e}")

        # Programar el siguiente mensaje 2 minutos después del anterior
        hora_envio += datetime.timedelta(minutes=2)

    messagebox.showinfo("Listo", "Mensajes programados.")

# Crear ventana
ventana = tk.Tk()
ventana.title("Enviar WhatsApp en lote")
ventana.geometry("500x500")

# Etiqueta y caja para el mensaje
tk.Label(ventana, text="Mensaje a enviar:").pack(pady=5)
caja_mensaje = tk.Text(ventana, height=10, width=60)
caja_mensaje.pack()

# Botón para cargar archivo
tk.Button(ventana, text="Cargar archivo de números", command=cargar_archivo).pack(pady=10)

# Mostrar números cargados
tk.Label(ventana, text="Números cargados:").pack()
texto_numeros = tk.Text(ventana, height=10, width=60)
texto_numeros.pack()

# Botón para enviar
tk.Button(ventana, text="Enviar mensajes", bg="green", fg="white", command=enviar_mensajes).pack(pady=10)

# Mostrar la ventana
ventana.mainloop()
