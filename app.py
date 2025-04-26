import streamlit as st
import os
from documentos import DocumentUploader
from AI_model import analizar_documento_solo_texto
from faiss_manager import FAISSManager
from dotenv import load_dotenv

# ===== CARGA DE VARIABLES DE ENTORNO =====
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("⚠️ No se encontró la API Key de Cohere.")

# ===== INSTANCIAR FAISS MANAGER =====
faiss_manager = FAISSManager(api_key=COHERE_API_KEY)

# ===== CONFIGURACIÓN DE PÁGINA EN STREAMLIT =====
st.set_page_config(
    page_title="Dropshipping",
    page_icon="🛒",
    layout="wide"
)

# ===== CARGA DEL PDF =====
doc_uploader = DocumentUploader()
pdf_path = "DROPSHIPPING.pdf"
if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as f:
        doc_uploader.add_document(f)
    st.success(f"Documento {pdf_path} cargado exitosamente!")
    # Crear el índice FAISS a partir del PDF
    faiss_manager.create_faiss_index(doc_uploader.get_documents())
else:
    st.error(f"El archivo {pdf_path} no se encontró.")

# ===== DISEÑO EN STREAMLIT (CSS) =====
st.markdown("""
    <style>
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }
    .content-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .title {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subtitle {
        color: #34495e;
        font-weight: bold;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .answer {
        text-align: justify;
        color: #34495e;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    .input-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ===== ESTRUCTURA PRINCIPAL =====
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.markdown("<h1 class='title'>Bienvenido a la Guía de Dropshipping</h1>", unsafe_allow_html=True)

# ----- Bloque con preguntas fijas -----
st.markdown("""
<div class='content-card'>
    <h3 class='subtitle'>¿Qué es el dropshipping?</h3>
    <p class='answer'>
        El dropshipping es un modelo de negocio en el que no necesitas mantener un inventario propio. 
        Cuando alguien compra un producto en tu tienda en línea, tú realizas el pedido a un proveedor 
        que se encarga de enviar el producto directamente al cliente. De esta manera, reduces costos 
        y riesgos relacionados con el almacenamiento y la logística.
    </p>
    <h3 class='subtitle'>¿Cuáles son los pasos necesarios para iniciar un negocio de dropshipping?</h3>
    <p class='answer'>
        1. Escoger un nicho o producto con demanda.<br>
        2. Encontrar proveedores confiables (Aliexpress, etc.).<br>
        3. Crear tu tienda (Shopify, WooCommerce, etc.).<br>
        4. Definir tu estrategia de marketing (TikTok, Instagram, Ads...).<br>
        5. Gestionar ventas, envíos y servicio al cliente.
    </p>
</div>
""", unsafe_allow_html=True)

# ----- Bloque para solicitar más información -----
st.markdown("""
<div class='content-card'>
    <h3 class='subtitle'>¿Tienes más preguntas?</h3>
    <div class='input-card'>
""", unsafe_allow_html=True)

question = st.text_area("Escribe aquí tu duda o comentario:")

# Botón para enviar y obtener respuesta de la IA con contexto del PDF
if st.button("Enviar"):
    user_query = question.strip()
    if user_query:
        # 1) Buscamos los fragmentos más relevantes en el PDF
        top_chunks = faiss_manager.search_similar_chunks(user_query, k=2)
        # 2) Construimos el prompt con el contexto del PDF
        context = "\n\n".join(top_chunks)
        prompt = f"""Responde la siguiente pregunta basándote únicamente en el contexto de abajo.
Si no encuentras la respuesta en el contexto, di que no está disponible.

Contexto:
{context}

Pregunta:
{user_query}

Respuesta:"""

        # 3) Llamamos a la función que usa Cohere
        response = analizar_documento_solo_texto(prompt)
        # 4) Mostramos la respuesta
        st.markdown("**Respuesta basada en el PDF:**")
        st.write(response)
    else:
        st.error("Por favor, ingresa alguna pregunta o comentario.")

st.markdown("</div></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
