import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pywhatkit as kit
import datetime
import time
import threading  # ✅ Para evitar que se congele la interfaz

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

def enviar_mensajes_thread():
    mensaje = caja_mensaje.get("1.0", tk.END).strip()
    if not mensaje or not numeros:
        messagebox.showwarning("Error", "Debes escribir un mensaje y cargar números.")
        return

    estado_var.set("📤 Enviando mensajes...")
    ventana.update()

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
            estado_var.set(f"📨 Mensaje programado para {numero} a las {hora}:{minuto:02d}")
            ventana.update()
            time.sleep(25)
        except Exception as e:
            print(f"Error enviando a {numero}: {e}")

        hora_envio += datetime.timedelta(minutes=2)

    estado_var.set("✅ Mensajes programados correctamente.")
    messagebox.showinfo("Listo", "Todos los mensajes fueron programados.")

def enviar_mensajes():
    hilo = threading.Thread(target=enviar_mensajes_thread)
    hilo.start()

# Crear ventana principal
ventana = tk.Tk()
ventana.title("📲 Enviar WhatsApp en lote")
ventana.geometry("600x600")
ventana.resizable(False, False)
ventana.config(padx=15, pady=15)

# --- Frame para el mensaje ---
frame_msg = tk.Frame(ventana)
frame_msg.grid(row=0, column=0, sticky="ew", pady=5)

tk.Label(frame_msg, text="Mensaje a enviar:", font=("Arial", 12, "bold")).pack(anchor="w")
caja_mensaje = scrolledtext.ScrolledText(frame_msg, height=6, width=70, wrap=tk.WORD)
caja_mensaje.pack()

# --- Frame para archivo y lista de números ---
frame_archivo = tk.Frame(ventana)
frame_archivo.grid(row=1, column=0, sticky="ew", pady=10)

btn_cargar = tk.Button(frame_archivo, text="📂 Cargar archivo de números", font=("Arial", 11), command=cargar_archivo)
btn_cargar.pack(pady=5)

tk.Label(frame_archivo, text="Números cargados:", font=("Arial", 12, "bold")).pack(anchor="w")
texto_numeros = scrolledtext.ScrolledText(frame_archivo, height=8, width=70, wrap=tk.WORD)
texto_numeros.pack()

# --- Frame final: botón y estado ---
frame_final = tk.Frame(ventana)
frame_final.grid(row=2, column=0, pady=15)

btn_enviar = tk.Button(
    frame_final,
    text="🚀 Enviar mensajes",
    bg="#28a745",
    fg="white",
    font=("Arial", 11, "bold"),
    width=20,
    command=enviar_mensajes
)
btn_enviar.pack(pady=5)

estado_var = tk.StringVar()
estado_var.set("⏳ Esperando acción...")
estado_label = tk.Label(frame_final, textvariable=estado_var, font=("Arial", 10), fg="blue")
estado_label.pack()

# Iniciar la aplicación
ventana.mainloop()
