import pygame
from gtts import gTTS

class AudioLogic:
    def __init__(self):
        pygame.mixer.init()
        self.audio_file = None

    def save_audio(self, text, file_path, language='es'):
        if not text:
            raise ValueError("El texto no puede estar vacío.")
        
        # Guarda el audio dependiendo del idioma
        if language not in ['es', 'en']:
            raise ValueError("Idioma no soportado, usa español o inglés.")
        
        tts = gTTS(text, lang=language)
        tts.save(file_path)
        self.audio_file = file_path
        return file_path

    # Reproduce el audio
    def play_audio(self):
        if self.audio_file:
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play()

    # Detiene la reproducción
    def stop_audio(self):
        pygame.mixer.music.stop()