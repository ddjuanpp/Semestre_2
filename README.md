# GuíaShipping - Asistente de Dropshipping con IA

Esta aplicación utiliza **inteligencia artificial** para proporcionar respuestas detalladas, consejos prácticos y recomendaciones sobre **dropshipping y comercio electrónico**.

## 📋 Características

- **Interfaz conversacional intuitiva**: Interactúa con el asistente IA como si fuera un experto en dropshipping
- **Conocimiento especializado**: Respuestas detalladas sobre nichos de mercado, proveedores, estrategias y más
- **Enfoque práctico**: Consejos accionables y ejemplos reales de negocios de dropshipping
- **Diseño responsivo**: Funciona en dispositivos móviles y de escritorio

---

## 🚀 Uso de la aplicación

### Cómo hacer preguntas
1. Escribe tu pregunta en el campo de texto en la parte inferior
2. Presiona "Enviar" o utiliza la tecla Enter
3. Espera a que el asistente procese y responda tu consulta

### Tipos de consultas recomendadas
- **Nichos de mercado**: "¿Qué nichos son rentables para dropshipping en 2024?"
- **Proveedores**: "¿Cómo encontrar proveedores confiables para productos electrónicos?"
- **Marketing**: "¿Qué estrategias de marketing funcionan mejor para una tienda nueva?"
- **Logística**: "¿Cómo gestionar devoluciones en dropshipping?"
- **Plataformas**: "¿Shopify o WooCommerce para mi tienda de dropshipping?"

### Funciones adicionales
- Utiliza el botón "Limpiar" para borrar el historial de conversación
- La aplicación recuerda el contexto de la conversación, puedes hacer preguntas de seguimiento

---

## 🛠️ Implementación del proyecto

Esta aplicación fue desarrollada como parte de un proyecto personal para explorar las capacidades de la IA en el ámbito del comercio electrónico.

### Requisitos previos
- Python 3.8 o superior
- Las bibliotecas listadas en `requirements.txt`
- Acceso a la API de Google Gemini y Mistral AI

### Configuración del entorno

1. **Instalación de dependencias**
   ```
   pip install -r requirements.txt
   ```

2. **Configuración de las API Keys**
   
   Debes crear un archivo `.env` en la carpeta del proyecto:
   ```
   GEMINI_API_KEY=tu_api_key_de_gemini
   MISTRAL_API_KEY=tu_api_key_de_mistral
   ```

### Estructura del proyecto

```
proyecto/
├── app.py               # Aplicación principal (Streamlit)
├── AI_model.py          # Configuración del modelo de IA
├── documentos.py        # Gestión de documentos
├── faiss_manager.py     # Índice vectorial para búsqueda semántica
├── DROPSHIPPING.pdf     # Documento de referencia
├── requirements.txt     # Dependencias
└── README.md            # Documentación
```

### Componentes principales

#### 1. Modelo de IA (AI_model.py)
Este componente gestiona la conexión con el modelo de lenguaje (Google Gemini) y procesa las consultas del usuario para generar respuestas naturales y útiles sobre dropshipping.

#### 2. Búsqueda Semántica (faiss_manager.py)
Implementa un índice vectorial FAISS para encontrar información relevante en el documento de referencia, permitiendo respuestas precisas basadas en el contexto.

#### 3. Procesamiento de Documentos (documentos.py)
Se encarga de cargar y extraer texto de documentos PDF, que luego son utilizados como fuente de conocimiento por el asistente.

#### 4. Interfaz de Usuario (app.py)
Construida con Streamlit, proporciona una experiencia amigable y responsive para que los usuarios interactúen con el asistente de IA.

### Ejecución

Para ejecutar la aplicación:
```
streamlit run app.py
```

### Personalización

Se puede adaptar fácilmente para otros dominios modificando:
- El documento de referencia
- Las instrucciones del sistema en AI_model.py
- El diseño CSS en app.py
