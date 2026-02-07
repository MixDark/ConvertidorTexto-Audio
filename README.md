# 🎙️ Convertidor texto a audio

Una aplicación PyQt6 moderna y minimalista que convierte texto en audio usando Google Text-to-Speech (gTTS). Soporta 10 idiomas diferentes con una interfaz translúcida y elegante.

## ✨ Características

- 🌍 **10 Idiomas soportados**: Español, Inglés, Francés, Alemán, Italiano, Portugués, Japonés, Chino, Ruso, Árabe
- 🎵 **Reproducción de audio**: Con controles de Play, Pausa y Detener
- 💾 **Guardar audio**: Guarda los archivos en formato MP3
- 🎨 **Interfaz moderna**: Diseño translúcido en azul con tema profesional
- 📊 **Estadísticas**: Contador de palabras y caracteres en tiempo real
- 🔤 **Copiar/pegar**: Botones para facilitar el manejo de texto
- ⚙️ **Ventana fija**: Tamaño optimizado (800x600) sin opción de redimensionar

## 🚀 Requisitos

- Python 3.14+
- PyQt6 6.10.2
- gTTS 2.5.4
- sounddevice 0.5.1
- soundfile 0.13.0

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/ConvertidorTexto-Audio.git
cd ConvertidorTexto-Audio
```

### 2. Crear un entorno virtual (opcional pero recomendado)
```bash
python -m venv venv
```

### 3. Activar el entorno virtual
- **Windows**:
```bash
venv\Scripts\activate
```
- **macOS/Linux**:
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 🎯 Uso

### Ejecutar la aplicación
```bash
python interfaz.py
```

### Pasos básicos
1. Selecciona el idioma en el dropdown (esquina superior derecha)
2. Ingresa el texto en el área de texto principal
3. Haz clic en "Generar" para crear el audio
4. Haz clic en "Reproducir" para escuchar el audio
5. (Opcional) Haz clic en "Guardar" para guardar el archivo MP3

## 📁 Estructura del proyecto

```
ConvertidorTexto-Audio/
├── interfaz.py              # Interfaz gráfica PyQt6
├── convertidor.py           # Lógica de generación de audio
├── styles.css               # Estilos de la interfaz
├── requirements.txt         # Dependencias del proyecto
├── README.md               # Este archivo
├── CHANGELOG.md            # Historial de cambios
├── .gitignore              # Archivos ignorados por Git
└── favicon.ico             # Icono de la aplicación
```

## 🎨 Idiomas soportados

| Código | Idioma |
|--------|--------|
| es | Español |
| en | Inglés |
| fr | Francés |
| de | Alemán |
| it | Italiano |
| pt | Portugués |
| ja | Japonés |
| zh | Chino |
| ru | Ruso |
| ar | Árabe |

## 🛠️ Tecnologías utilizadas

- **PyQt6**: Framework GUI multiplataforma
- **gTTS (Google Text-to-Speech)**: Motor de síntesis de voz
- **sounddevice**: Reproducción de audio de bajo nivel
- **soundfile**: Lectura de archivos de audio

## ⚙️ Configuración

### Tasa de reproducción
La tasa de reproducción por defecto es estándar (120 caracteres/minuto). Puedes modificarla en `convertidor.py`.

### Formato de salida
Por defecto, los archivos se guardan como MP3. El formato se puede cambiar en la interfaz.

## 🐛 Solución de problemas

### "El audio no se escucha"
- Asegúrate de que los altavoces estén encendidos
- Verifica que el archivo se generó correctamente (debe tener más de 10KB)
- Intenta regenerar el audio

### "Error al instalar sounddevice"
- En Windows, puede necesitar librerias del sistema no instaladas. Intenta instalar:
```bash
pip install --upgrade sounddevice
```

### "GeForce o error de codificación de caracteres"
- Asegúrate de que tu archivo esté en UTF-8:
```bash
# Convertir a UTF-8 si es necesario
dos2unix interfaz.py convertidor.py
```

## 📝 Licencia

Este proyecto está bajo licencia MIT. Consulta [LICENSE](LICENSE) para más información.

## 👤 Autor

Creado con ❤️ para automatizar la conversión de texto a audio.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Si encuentras algún problema, por favor abre un issue en el repositorio.

---

**Versión**: 1.0.0  
**Última actualización**: 7 de febrero de 2026
