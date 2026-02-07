from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QComboBox, QFileDialog,
    QMessageBox, QProgressBar, QStatusBar, QGroupBox, QSpinBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject, QThread
from PyQt6.QtGui import QFont, QIcon, QColor, QTextCursor
from convertidor import AudioLogic
import os


class AudioWorker(QObject):
    """Worker para generar audio sin bloquear la interfaz"""
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, text, file_path, language, audio_logic):
        super().__init__()
        self.text = text
        self.file_path = file_path
        self.language = language
        # USAR la instancia de AudioLogic pasada desde AudioApp
        self.audio_logic = audio_logic

    def run(self):
        try:
            self.audio_logic.save_audio(self.text, self.file_path, self.language)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class AudioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audio_logic = AudioLogic()
        self.current_audio_file = None
        self.playback_timer = QTimer()
        self.playback_timer.timeout.connect(self.update_playback_status)
        
        # Establecer Sabina como voz por defecto
        voices = self.audio_logic.get_available_voices()
        if voices:
            self.audio_logic.set_voice(voices[0]['id'], voices[0].get('source', 'system'))
            print(f"Voz por defecto establecida: {voices[0]['name']}")
        
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle("Convertidor texto a audio - Voz: Sabina")
        
        # Establecer favicon
        favicon_path = os.path.join(os.path.dirname(__file__), 'favicon.ico')
        if os.path.exists(favicon_path):
            self.setWindowIcon(QIcon(favicon_path))
        
        # Establecer tamaño fijo y deshabilitar redimensionado, maximizar y minimizar
        self.setFixedSize(800, 600)
        # Solo mostrar botón cerrar (sin maximizar ni minimizar)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)
        
        # Centrar la ventana en la pantalla
        screen = self.screen().geometry()
        window_geometry = self.frameGeometry()
        x = (screen.width() - window_geometry.width()) // 2
        y = (screen.height() - window_geometry.height()) // 2
        self.move(x, y)
        
        # Cargar CSS desde archivo
        try:
            css_file = os.path.join(os.path.dirname(__file__), 'styles.css')
            if os.path.exists(css_file):
                with open(css_file, 'r', encoding='utf-8') as f:
                    self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error al cargar estilos: {e}")

        # Widget principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # ===== SECCIÓN SUPERIOR: TÍTULO E IDIOMA =====
        top_layout = QHBoxLayout()
        title_label = QLabel("🎙️ Convertidor texto a audio")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        top_layout.addWidget(title_label)

        top_layout.addStretch()

        # Selector de idioma
        language_label = QLabel("Idioma:")
        self.language_combo = QComboBox()
        self.language_combo.addItems([f"{lang} ({code})" for code, lang in self.audio_logic.get_supported_languages().items()])
        top_layout.addWidget(language_label)
        top_layout.addWidget(self.language_combo)

        main_layout.addLayout(top_layout)

        # ===== SECCIÓN DE ESTADÍSTICAS =====
        stats_layout = QHBoxLayout()
        
        self.word_label = QLabel("Palabras: 0")
        self.char_label = QLabel("Caracteres: 0")
        
        stats_layout.addWidget(self.word_label)
        stats_layout.addStretch()
        stats_layout.addWidget(self.char_label)
        
        main_layout.addLayout(stats_layout)

        # ===== SECCIÓN DE ENTRADA DE TEXTO =====
        text_group = QGroupBox("Texto a convertir")
        text_layout = QVBoxLayout()
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Ingrese el texto aquí o use el botón pegar...")
        self.text_edit.setMinimumHeight(200)
        self.text_edit.textChanged.connect(self.update_stats)
        text_layout.addWidget(self.text_edit)
        
        text_group.setLayout(text_layout)
        main_layout.addWidget(text_group)

        # ===== SECCIÓN DE BOTONES DE CONTROL =====
        button_layout = QHBoxLayout()

        self.paste_btn = QPushButton("📋 Pegar")
        self.paste_btn.clicked.connect(self.paste_text)
        button_layout.addWidget(self.paste_btn)

        self.clear_btn = QPushButton("🗑️ Limpiar")
        self.clear_btn.clicked.connect(self.clear_text)
        button_layout.addWidget(self.clear_btn)

        button_layout.addStretch()

        self.generate_btn = QPushButton("⚙️ Generar")
        self.generate_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 8px;")
        self.generate_btn.clicked.connect(self.generate_audio)
        button_layout.addWidget(self.generate_btn)

        main_layout.addLayout(button_layout)

        # ===== SECCIÓN DE REPRODUCCIÓN =====
        playback_group = QGroupBox("Reproducción")
        playback_layout = QVBoxLayout()

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setEnabled(False)
        playback_layout.addWidget(self.progress_bar)

        # Botones de reproducción
        control_layout = QHBoxLayout()

        self.play_btn = QPushButton("▶️ Reproducir")
        self.play_btn.clicked.connect(self.play_audio)
        self.play_btn.setEnabled(False)
        control_layout.addWidget(self.play_btn)

        self.pause_btn = QPushButton("⏸️ Pausar")
        self.pause_btn.clicked.connect(self.pause_audio)
        self.pause_btn.setEnabled(False)
        control_layout.addWidget(self.pause_btn)

        self.stop_btn = QPushButton("⏹️ Detener")
        self.stop_btn.clicked.connect(self.stop_audio)
        self.stop_btn.setEnabled(False)
        control_layout.addWidget(self.stop_btn)

        control_layout.addStretch()

        self.save_btn = QPushButton("💾 Guardar")
        self.save_btn.clicked.connect(self.save_audio_file)
        self.save_btn.setEnabled(False)
        control_layout.addWidget(self.save_btn)

        playback_layout.addLayout(control_layout)
        playback_group.setLayout(playback_layout)
        main_layout.addWidget(playback_group)

        # ===== BARRA DE ESTADO =====
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Listo")

        central_widget.setLayout(main_layout)

    def update_stats(self):
        """Actualiza las estadísticas de texto"""
        text = self.text_edit.toPlainText()
        words = len(text.split()) if text.strip() else 0
        chars = len(text.replace(" ", ""))
        
        self.word_label.setText(f"Palabras: {words}")
        self.char_label.setText(f"Caracteres: {chars}")

    def paste_text(self):
        """Pega texto desde el portapapeles"""
        try:
            clipboard = QApplication.clipboard()
            text = clipboard.text()
            if text:
                self.text_edit.insertPlainText(text)
            else:
                QMessageBox.warning(self, "Advertencia", "El portapapeles está vacío.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo obtener el texto del portapapeles: {e}")

    def clear_text(self):
        """Limpia el área de texto"""
        self.text_edit.clear()
        self.update_stats()

    def get_selected_language(self):
        """Retorna el código de idioma seleccionado"""
        languages = self.audio_logic.get_supported_languages()
        selected_text = self.language_combo.currentText()
        # Extrae el código de idioma (entre paréntesis)
        lang_code = selected_text.split('(')[-1].rstrip(')')
        return lang_code

    def generate_audio(self):
        """Genera el archivo de audio"""
        text = self.text_edit.toPlainText().strip()
        
        if not text:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingrese algún texto.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar archivo de audio",
            "",
            "MP3 Files (*.mp3);;WAV Files (*.wav)"
        )

        if not file_path:
            return

        # Si no especifica extensión, usar .wav por defecto (pyttsx3)
        if not file_path.endswith('.wav') and not file_path.endswith('.mp3'):
            file_path = file_path + '.wav'

        self.generate_btn.setEnabled(False)
        self.status_bar.showMessage("Generando audio...")

        try:
            language = self.get_selected_language()
            print(f"DEBUG generate_audio: selected_voice={self.audio_logic.selected_voice}, voice_source={self.audio_logic.voice_source}")
            # USAR la misma instancia de audio_logic que tiene la voz seleccionada
            generated_file = self.audio_logic.save_audio(text, file_path, language)
            
            # Usar la ruta retornada por save_audio (puede ser diferente si se convierte)
            self.current_audio_file = generated_file if generated_file else file_path
            
            # Validar que el archivo existe
            if os.path.exists(self.current_audio_file):
                file_size = os.path.getsize(self.current_audio_file)
                print(f"DEBUG: Archivo verificado - {self.current_audio_file}")
                print(f"DEBUG: Tamaño del archivo: {file_size} bytes")
            else:
                print(f"DEBUG ERROR: El archivo no existe - {self.current_audio_file}")
            
            # Habilitar botones de reproducción
            self.play_btn.setEnabled(True)
            self.play_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
            self.stop_btn.setEnabled(True)
            self.pause_btn.setEnabled(True)
            self.save_btn.setEnabled(True)
            
            self.status_bar.showMessage(f"Audio generado exitosamente: {os.path.basename(self.current_audio_file)}")
            QMessageBox.information(self, "Éxito", f"Audio guardado en:\n{self.current_audio_file}")
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            self.status_bar.showMessage("Error al generar audio")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {e}")
            self.status_bar.showMessage("Error al generar audio")
        finally:
            self.generate_btn.setEnabled(True)

    def play_audio(self):
        """Reproduce el audio"""
        if self.current_audio_file and os.path.exists(self.current_audio_file):
            try:
                print(f"DEBUG interfaz play_audio: Reproduciendo {self.current_audio_file}")
                print(f"DEBUG interfaz: audio_logic.audio_file={self.audio_logic.audio_file}")
                # Pasar explícitamente el archivo a reproducir para garantizar sincronización
                self.audio_logic.play_audio(self.current_audio_file)
                self.status_bar.showMessage("Reproduciendo...")
                self.play_btn.setEnabled(False)
                self.pause_btn.setEnabled(True)
                self.playback_timer.start(100)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo reproducir el audio: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, genera el audio primero.")

    def pause_audio(self):
        """Pausa la reproducción"""
        try:
            self.audio_logic.pause_audio()
            self.status_bar.showMessage("En pausa")
            self.pause_btn.setEnabled(False)
            self.play_btn.setEnabled(True)
            self.playback_timer.stop()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo pausar: {e}")

    def stop_audio(self):
        """Detiene la reproducción"""
        try:
            self.audio_logic.stop_audio()
            self.status_bar.showMessage("Detenido")
            self.play_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.playback_timer.stop()
            self.progress_bar.setValue(0)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo detener: {e}")

    def save_audio_file(self):
        """Abre el dialogo para guardar el archivo de audio"""
        if self.current_audio_file and os.path.exists(self.current_audio_file):
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar copia del audio",
                "",
                "WAV Files (*.wav);;MP3 Files (*.mp3)"
            )
            if save_path:
                try:
                    import shutil
                    shutil.copy(self.current_audio_file, save_path)
                    self.status_bar.showMessage(f"Archivo guardado: {os.path.basename(save_path)}")
                    QMessageBox.information(self, "Éxito", f"Audio guardado en:\n{save_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al guardar: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "No hay audio generado para guardar.")

    def update_playback_status(self):
        """Actualiza el estado de reproducción"""
        if not self.audio_logic.is_music_playing():
            self.status_bar.showMessage("Reproducción finalizada")
            self.play_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.playback_timer.stop()
            self.progress_bar.setValue(100)
        else:
            self.progress_bar.setValue(50)  # Simulación de progreso

    def closeEvent(self, event):
        """Detiene la reproducción al cerrar la aplicación"""
        self.audio_logic.stop_audio()
        self.playback_timer.stop()
        event.accept()


def main():
    app = QApplication([])
    window = AudioApp()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
