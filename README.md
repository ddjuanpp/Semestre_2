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

Si quieres implementar este proyecto desde cero, sigue estos pasos:

### Requisitos previos
- Python 3.8 o superior
- Pip (gestor de paquetes de Python)
- Una API key de Google Gemini o Mistral AI

### Instalación

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/tuusuario/guiashipping.git
   cd guiashipping
   ```

2. **Crea un entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno**
   
   Crea un archivo `.env` en la raíz del proyecto con:
   ```
   GEMINI_API_KEY=tu_api_key_aqui
   MISTRAL_API_KEY=tu_api_key_aqui_si_usas_mistral
   ```

### Estructura del proyecto

```
guiashipping/
├── app.py               # Aplicación principal (Streamlit)
├── AI_model.py          # Configuración del modelo de IA
├── documentos.py        # Gestión de documentos
├── faiss_manager.py     # Índice vectorial para búsqueda semántica
├── DROPSHIPPING.pdf     # Documento de referencia
├── requirements.txt     # Dependencias
└── README.md            # Documentación
```

### Componentes principales

#### 1. AI_model.py
Este archivo configura la conexión con el modelo de lenguaje (Google Gemini 1.5 Flash).
```python
# Configuración básica del modelo
def analizar_documento_solo_texto(prompt):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash-8b")
    response = model.generate_content(prompt)
    return response.text
```

#### 2. faiss_manager.py
Implementa un índice vectorial FAISS para búsqueda semántica.
```python
# Creación de índice FAISS
def create_faiss_index(self, documents):
    self.documents = documents
    self.texts = [doc.page_content for doc in documents]
    self.embedding_model = MistralAIEmbeddings(api_key=self.api_key)
    self.embeddings = self.embedding_model.embed_documents(self.texts)
    self.index = faiss.IndexFlatL2(len(self.embeddings[0]))
    faiss.normalize_L2(np.array(self.embeddings, dtype=np.float32))
    self.index.add(np.array(self.embeddings, dtype=np.float32))
```

#### 3. documentos.py
Maneja la carga y procesamiento de documentos.
```python
# Carga de documentos PDF
def add_document(self, file_obj):
    pdf_reader = PyPDF2.PdfReader(file_obj)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    self.documents.append(Document(page_content=text))
```

#### 4. app.py
Aplicación principal con Streamlit, implementa la interfaz de usuario y la lógica de la aplicación.

### Ejecución

Para ejecutar la aplicación:
```bash
streamlit run app.py
```

### Personalización

- **Documento de referencia**: Reemplaza DROPSHIPPING.pdf con tu propio documento
- **Modelo de IA**: Puedes cambiar el modelo en AI_model.py (ej. OpenAI, Claude)
- **Diseño**: Modifica el CSS en app.py para cambiar la apariencia

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes, abre primero un issue para discutir lo que te gustaría cambiar.

---

## 📞 Contacto

Si tienes preguntas o sugerencias, contáctame en [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com). 