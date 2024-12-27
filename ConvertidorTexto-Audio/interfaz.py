from tkinter import Tk, Label, Button, Text, filedialog, messagebox, Frame, Scrollbar, RIGHT, Y
from convertidor import AudioLogic

class AudioApp:
    def __init__(self, master):
        self.master = master
        master.title("Convertidor de texto a audio")

        # Fijar tamaño de la ventana y centrarla
        window_width = 440
        window_height = 260
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        master.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        master.resizable(False, False)  # Evitar que la ventana se redimensione

        self.label = Label(master, text="Ingrese el texto o haga clic en pegar para agregarlo:")
        self.label.pack(pady=10)

        # Frame para la caja de texto con scroll
        text_frame = Frame(master)
        text_frame.pack()

        self.scrollbar = Scrollbar(text_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.text_box = Text(text_frame, height=10, width=50, yscrollcommand=self.scrollbar.set)
        self.text_box.pack()
        self.scrollbar.config(command=self.text_box.yview)

        # Frame para botones en una sola fila
        button_frame = Frame(master)
        button_frame.pack(pady=15)

        # Botón para pegar texto desde el portapapeles
        self.paste_button = Button(button_frame, text="Pegar", command=self.paste_text)
        self.paste_button.pack(side="left", padx=5)

        self.save_button = Button(button_frame, text="Generar", command=self.save_audio)
        self.save_button.pack(side="left", padx=5)

        self.play_button = Button(button_frame, text="Reproducir", command=self.play_audio, state='disabled')
        self.play_button.pack(side="left", padx=5)

        self.stop_button = Button(button_frame, text="Detener", command=self.stop_audio, state='disabled')
        self.stop_button.pack(side="left", padx=5)

        self.audio_logic = AudioLogic()

    def paste_text(self):
        try:
            clipboard_text = self.master.clipboard_get()
            self.text_box.insert("end", clipboard_text)
        except Exception as e:
            messagebox.showerror("Error", "No se pudo obtener el texto del portapapeles.")

    def save_audio(self):
        text = self.text_box.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Advertencia", "Por favor, ingrese algún texto.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                 filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            try:
                self.audio_logic.save_audio(text, file_path)
                self.play_button.config(state='normal')
                self.stop_button.config(state='normal')
                messagebox.showinfo("Éxito", f"Audio guardado exitosamente en {file_path}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def play_audio(self):
        self.audio_logic.play_audio()

    def stop_audio(self):
        self.audio_logic.stop_audio()

def main():
    root = Tk()
    app = AudioApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()