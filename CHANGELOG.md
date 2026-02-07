# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/), y este proyecto mantiene [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-02-07

### ✨ Agregado
- Interfaz gráfica moderna con PyQt6
- Soporte para 10 idiomas (español, inglés, francés, alemán, italiano, portugués, japonés, chino, ruso, árabe)
- Generación de audio usando Google Text-to-Speech (gTTS)
- Reproducción de audio con controles (Play, Pausa, Detener)
- Función de guardar archivos de audio en formato MP3
- Tema translúcido azul con interface minimalista
- Selector de idioma en tiempo real
- Contador de palabras y caracteres
- Botones de Copiar, Pegar y Limpiar
- Indicador de progreso de reproducción
- Barra de estado con información de operación

### 🔧 Cambios técnicos
- Primera versión estable del proyecto
- Integración de sounddevice y soundfile para reproducción de audio
- Implementación de threading para no bloquear la interfaz
- Estilos CSS personalizados para toda la aplicación

### 🎨 Diseño
- Aplicación con ventana fija de 800x600 píxeles
- Diseño translúcido (50% opacidad) con fondo gradiente azul
- Texto blanco en contraste con fondo azul
- Botones con tema azul (#2196F3) y estados hover/pressed
- Campo de texto con fondo blanco y borde azul

## [0.5.0 - Alpha] - 2026-02-06

### 🧪 Estado Experimental
- Pruebas iniciales con edge-tts para múltiples voces
- Validación de arquitectura de backend
- Desarrollo de componentes de UI

### ❌ Descontinuado
- Soporte para pyttsx3 (reemplazado por gTTS)
- Soporte para edge-tts (reemplazado por gTTS)
- Sistema de selección de voces local
- Reproducción con pygame (reemplazado por sounddevice)

---

## Notas sobre versiones anteriores

### Por qué gTTS en lugar de edge-tts
- **gTTS**: Más simple, más confiable, mejor calidad de voz, sin dependencias complejas
- **edge-tts**: Validación compleja, múltiples errores de configuración, requería IDs de voz completos

### Por qué sounddevice en lugar de pygame
- **sounddevice**: Reproducción de audio de bajo nivel más eficiente
- **pygame**: Dependencias pesadas, problemas de sincronización con PyQt6

---

## Planificado para futuras versiones

### [1.1.0] - Mejoras de interfaz
- [ ] Selector de velocidad de reproducción
- [ ] Historial de textos recientes
- [ ] Tema oscuro/claro intercambiable
- [ ] Atajos de teclado personalizables

### [1.2.0] - Características avanzadas
- [ ] Soporte para múltiples voces por idioma
- [ ] Generación de audio en lotes
- [ ] Edición de etiquetas de audio (ID3)
- [ ] Conversión de texto desde archivos

### [2.0.0] - Versión mayor
- [ ] Aplicación multiplataforma empaquetada (exe, dmg, deb)
- [ ] API para integración con otros programas
- [ ] Sincronización en la nube
- [ ] Soporte para sintetización offline

---

Para reportar bugs o sugerir características, abre un issue en el repositorio.
