import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                            QFileDialog, QMessageBox, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QClipboard, QIcon
from convertidor import AudioLogic

class ConversionThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, audio_logic, text, file_path):
        super().__init__()
        self.audio_logic = audio_logic
        self.text = text
        self.file_path = file_path

    def run(self):
        try:
            # Conectar las señales del AudioLogic
            self.audio_logic.progress_updated.connect(self.progress.emit)
            self.audio_logic.conversion_finished.connect(self.finished.emit)
            self.audio_logic.error_occurred.connect(self.error.emit)
            
            # Realizar la conversión
            self.audio_logic.save_audio(self.text, self.file_path)
        except Exception as e:
            self.error.emit(str(e))

class AudioApp(QMainWindow):
    def __init__(self):
                super().__init__()
                self.audio_logic = AudioLogic()
                self.initUI()
                self.setWindowIcon(QIcon('icono.png'))  
                self.setStyleSheet("""
                    QMainWindow {
                        background-color: #f0f0f0;
                    }
                    QLabel {
                        color: #333333;
                        font-size: 14px;
                        margin-bottom: 5px;
                    }
                    QTextEdit {
                        background-color: white;
                        color: black;
                        border: 1px solid #cccccc;
                        border-radius: 4px;
                        padding: 5px;
                        font-size: 14px;
                    }
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 8px 16px;
                        font-size: 12px;
                        margin: 0px 10px;
                    }
                    QPushButton:hover {
                        background-color: #1976D2;
                    }
                    QPushButton:disabled {
                        background-color: #BDBDBD;
                    }
                    QProgressBar {
                        border: 1px solid #cccccc;
                        border-radius: 4px;
                        text-align: center;
                        height: 20px;
                        margin: 10px 0px;
                    }
                    QProgressBar::chunk {
                        background-color: #2196F3;
                    }
                    QMessageBox {
                        background-color: #f0f0f0;
                    }
                    QMessageBox QLabel {
                        color: #333333;
                    }
                    QMessageBox QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 6px 12px;
                        margin: 0px 5px;
                        min-width: 60px;
                    }
                    QMessageBox QPushButton:hover {
                        background-color: #1976D2;
                    }
                """)

    def initUI(self):
            self.setWindowTitle('Convertidor de texto a audio')
            self.setFixedSize(600, 400)  # Aumentado el tamaño de la ventana

            # Widget central y layout principal
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)
            layout.setContentsMargins(20, 20, 20, 20)  # Márgenes generales

            # Label
            label = QLabel('Ingrese el texto o haga clic en pegar para agregarlo desde el portapeles:')
            layout.addWidget(label)

            # TextEdit
            self.text_edit = QTextEdit()
            layout.addWidget(self.text_edit)

            # Progress Bar
            self.progress_bar = QProgressBar()
            self.progress_bar.setVisible(False)
            layout.addWidget(self.progress_bar)

            # Contenedor para los botones
            button_container = QWidget()
            button_layout = QHBoxLayout(button_container)
            button_layout.setSpacing(20)  # Espacio entre botones
            button_layout.setContentsMargins(0, 10, 0, 10)  # Márgenes del contenedor de botones
            
            # Crear botones con tamaño fijo
            self.paste_button = QPushButton('Pegar')
            self.generate_button = QPushButton('Generar')
            self.play_button = QPushButton('Reproducir')
            self.stop_button = QPushButton('Detener')

            # Establecer un tamaño fijo para todos los botones
            button_width = 120
            button_height = 35
            for button in [self.paste_button, self.generate_button, 
                        self.play_button, self.stop_button]:
                button.setFixedSize(button_width, button_height)

            self.play_button.setEnabled(False)
            self.stop_button.setEnabled(False)

            # Añadir botones al layout con espaciadores
            button_layout.addStretch(1)
            button_layout.addWidget(self.paste_button)
            button_layout.addWidget(self.generate_button)
            button_layout.addWidget(self.play_button)
            button_layout.addWidget(self.stop_button)
            button_layout.addStretch(1)

            layout.addWidget(button_container)

            # Conectar señales
            self.paste_button.clicked.connect(self.paste_text)
            self.generate_button.clicked.connect(self.save_audio)
            self.play_button.clicked.connect(self.play_audio)
            self.stop_button.clicked.connect(self.stop_audio)

    def paste_text(self):
        try:
            clipboard = QApplication.clipboard()
            mime_data = clipboard.mimeData()

            if mime_data.hasText():
                text = clipboard.text()
                current_text = self.text_edit.toPlainText()
                
                # Si hay texto seleccionado, reemplazarlo
                cursor = self.text_edit.textCursor()
                if cursor.hasSelection():
                    cursor.insertText(text)
                # Si no hay selección, agregar al final o en la posición actual
                else:
                    if current_text:
                        self.text_edit.insertPlainText(text)
                    else:
                        self.text_edit.setPlainText(text)
            else:
                QMessageBox.warning(self, 'Advertencia', 
                                'No hay texto disponible para pegar.')
                
        except Exception as e:
            QMessageBox.critical(self, 'Error', 
                            f'Error al pegar texto: {str(e)}')

    def save_audio(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, 'Advertencia', 'Por favor, ingrese algún texto.')
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Guardar audio', '', 'MP3 files (*.mp3)'
        )

        if file_path:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            self.conversion_thread = ConversionThread(self.audio_logic, text, file_path)
            self.conversion_thread.progress.connect(self.update_progress)
            self.conversion_thread.finished.connect(self.conversion_finished)
            self.conversion_thread.error.connect(self.show_error)
            self.conversion_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def conversion_finished(self):
        self.progress_bar.setValue(100)
        self.play_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        QMessageBox.information(self, 'Éxito', 'Audio guardado exitosamente')
        self.progress_bar.setVisible(False)

    def show_error(self, error_message):
        QMessageBox.critical(self, 'Error', error_message)
        self.progress_bar.setVisible(False)

    def play_audio(self):
        self.audio_logic.play_audio()

    def stop_audio(self):
        self.audio_logic.stop_audio()

def main():
    app = QApplication(sys.argv)
    window = AudioApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
