from gtts import gTTS
import os
import threading
import sounddevice as sd
import soundfile as sf
import time

class AudioLogic:
    # Diccionario de idiomas soportados
    LANGUAGES = {
        'es': 'Español',
        'en': 'Inglés',
        'fr': 'Francés',
        'de': 'Alemán',
        'it': 'Italiano',
        'pt': 'Portugués',
        'ja': 'Japonés',
        'zh': 'Chino',
        'ru': 'Ruso'
    }

    def __init__(self):
        self.audio_file = None
        self.is_playing = False
        self.playback_thread = None
        self.stop_playback = False
        self.selected_voice = None
        self.voice_source = None


    def get_supported_languages(self):
        """Retorna el diccionario de idiomas soportados"""
        return self.LANGUAGES
    
    def get_available_voices(self):
        """Retorna 'Sabina' como voz por defecto (ahora usa gTTS)"""
        return [
            {'id': 'sabina', 'name': '🖥️ Sabina (Multidioma - gTTS)', 'source': 'system'}
        ]
    
    def set_voice(self, voice_id, source=None):
        """Establece la voz seleccionada (compatible para interfaz, pero no hace nada ahora)"""
        print(f"DEBUG: set_voice llamado - usando gTTS automáticamente")

    def save_audio(self, text, file_path, language='es'):
        """Genera y guarda el archivo de audio usando Google Text-to-Speech"""
        if not text:
            raise ValueError("El texto no puede estar vacío.")
        
        if language not in self.LANGUAGES:
            raise ValueError(f"Idioma no soportado. Usa uno de: {', '.join(self.LANGUAGES.keys())}")
        
        # Validar caracteres no soportados
        if len(text.strip()) == 0:
            raise ValueError("El texto no puede estar vacío.")
        
        print(f"DEBUG save_audio: Idioma solicitado={language}, file_path={file_path}")
        
        try:
            # Convertir a .mp3 para gTTS (genera mejor sonido)
            if not file_path.endswith('.mp3'):
                if file_path.endswith('.wav'):
                    file_path = file_path.replace('.wav', '.mp3')
                else:
                    file_path = file_path + '.mp3'
            
            print(f"DEBUG save_audio: Usando gTTS para generar audio en {language}")
            # Usar Google Text-to-Speech
            tts = gTTS(text, lang=language, slow=False)
            
            print(f"DEBUG save_audio: Guardando audio a: {file_path}")
            tts.save(file_path)
            print(f"DEBUG save_audio: Audio guardado exitosamente")
            
            self.audio_file = file_path
            print(f"DEBUG save_audio: self.audio_file asignado a {self.audio_file}")
            
        except Exception as e:
            raise ValueError(f"Error al generar audio: {e}")
        
        print(f"DEBUG save_audio: Retornando self.audio_file={self.audio_file}")
        # Retornar el archivo de audio generado
        return self.audio_file
    
    def get_word_count(self, text):
        """Retorna el número de palabras en el texto"""
        return len(text.split())

    def get_character_count(self, text):
        """Retorna el número de caracteres (sin espacios)"""
        return len(text.replace(" ", ""))

    def _play_audio_thread(self, audio_file):
        """Thread para reproducir audio sin bloquear la interfaz"""
        try:
            if audio_file and os.path.exists(audio_file):
                # Leer el archivo de audio
                data, samplerate = sf.read(audio_file)
                
                # Reproducir el audio
                print(f"DEBUG: Reproduciendo {audio_file} con samplerate={samplerate}")
                sd.play(data, samplerate)
                
                # Calcular duracion y esperar
                duration = len(data) / samplerate
                print(f"DEBUG: Duración del audio: {duration:.2f}s")
                
                start_time = time.time()
                while (time.time() - start_time) < duration and not self.stop_playback:
                    time.sleep(0.1)
                
                sd.stop()
                print(f"DEBUG: Reproducción finalizada")
                self.is_playing = False
        except Exception as e:
            print(f"Error al reproducir: {e}")
            self.is_playing = False

    def play_audio(self, file_path=None):
        """Reproduce el audio en un thread separado"""
        # Si se proporciona file_path, usar ese; si no, usar self.audio_file
        audio_to_play = file_path if file_path else self.audio_file
        print(f"DEBUG play_audio: self.audio_file={self.audio_file}")
        print(f"DEBUG play_audio: file_path parameter={file_path}")
        print(f"DEBUG play_audio: audio_to_play={audio_to_play}")
        
        if audio_to_play and os.path.exists(audio_to_play):
            self.stop_playback = False
            self.playback_thread = threading.Thread(target=self._play_audio_thread, args=(audio_to_play,), daemon=True)
            self.playback_thread.start()
            self.is_playing = True
            print(f"DEBUG play_audio: Iniciando reproducción - {audio_to_play}")
            return True
        else:
            print(f"DEBUG play_audio: ERROR - archivo no existe: {audio_to_play}")
        return False

    def stop_audio(self):
        """Detiene la reproducción"""
        self.stop_playback = True
        self.is_playing = False

    def pause_audio(self):
        """Pausa el audio (limitado con playsound)"""
        self.is_playing = False

    def unpause_audio(self):
        """Reanuda el audio"""
        self.is_playing = True

    def is_music_playing(self):
        """Verifica si hay audio reproduciéndose"""
        return self.is_playing