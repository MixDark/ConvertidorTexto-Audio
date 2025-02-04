import pygame
from gtts import gTTS
from PyQt6.QtCore import QObject, pyqtSignal
import time

class AudioLogic(QObject):
    # Señales para comunicar el progreso
    progress_updated = pyqtSignal(int)
    conversion_finished = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.audio_file = None

    def save_audio(self, text, file_path, language='es'):
        try:
            if not text:
                raise ValueError("El texto no puede estar vacío.")
            
            if language not in ['es', 'en']:
                raise ValueError("Idioma no soportado, usa español o inglés.")
            
            # Dividir el texto en segmentos para simular el progreso
            total_length = len(text)
            segment_size = total_length // 10  # 10 actualizaciones de progreso
            
            # Emitir progreso inicial
            self.progress_updated.emit(10)
            
            # Crear el objeto gTTS
            tts = gTTS(text, lang=language)
            
            # Emitir progreso medio
            self.progress_updated.emit(50)
            
            # Guardar el archivo
            tts.save(file_path)
            self.audio_file = file_path
            
            # Emitir progreso final
            self.progress_updated.emit(100)
            self.conversion_finished.emit()
            
            return file_path

        except Exception as e:
            self.error_occurred.emit(str(e))
            raise

    def play_audio(self):
        try:
            if self.audio_file:
                pygame.mixer.music.load(self.audio_file)
                pygame.mixer.music.play()
        except Exception as e:
            self.error_occurred.emit(f"Error al reproducir el audio: {str(e)}")

    def stop_audio(self):
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            self.error_occurred.emit(f"Error al detener el audio: {str(e)}")

    def is_playing(self):
        return pygame.mixer.music.get_busy()

    def set_volume(self, volume):
        """
        Establece el volumen de reproducción (0.0 a 1.0)
        """
        try:
            pygame.mixer.music.set_volume(volume)
        except Exception as e:
            self.error_occurred.emit(f"Error al ajustar el volumen: {str(e)}")
