import streamlit as st
import os
from documentos import DocumentUploader
from AI_model import analizar_documento_solo_texto, analizar_con_datos_productos
from faiss_manager import FAISSManager
from dotenv import load_dotenv
import re

# ===== CARGA DE VARIABLES DE ENTORNO =====
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError("⚠️ No se encontró la API Key de Mistral.")

# ===== INSTANCIAR FAISS MANAGER =====
faiss_manager = FAISSManager(api_key=MISTRAL_API_KEY)

# ===== CONFIGURACIÓN DE PÁGINA EN STREAMLIT =====
st.set_page_config(
    page_title="GuíaShipping - Asistente de Dropshipping",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== INICIALIZACIÓN DE ESTADO DE SESIÓN =====
if "messages" not in st.session_state:
    st.session_state.messages = []
if "use_web_search" not in st.session_state:
    st.session_state.use_web_search = "auto"  # auto, si, no

# Función para limpiar el historial de chat
def limpiar_chat():
    st.session_state.messages = []
    # No usar st.rerun() aquí porque no funciona en callbacks

# Función para detectar si una consulta necesita búsqueda web
def necesita_analisis_productos(mensaje):
    """Detecta automáticamente si una consulta se beneficiaría de análisis de productos"""
    palabras_clave_productos = [
        'nicho', 'nichos', 'producto', 'productos', 'precio', 'precios',
        'margen', 'ganancia', 'rentable', 'vender', 'dropshipping',
        'aliexpress', 'amazon', 'competencia', 'proveedor', 'proveedores',
        'qué vender', 'mejores productos', 'análisis de mercado',
        'oportunidad', 'saturado', 'demanda', 'tendencia'
    ]
    
    mensaje_lower = mensaje.lower()
    for palabra in palabras_clave_productos:
        if palabra in mensaje_lower:
            return True
    return False

# Función para obtener respuesta inteligente
def obtener_respuesta_inteligente(user_message, context=""):
    """Obtiene respuesta usando la mejor estrategia según el tipo de consulta"""
    try:
        # Determinar qué tipo de análisis usar
        if st.session_state.use_web_search == "productos":
            # Análisis de productos forzado
            return analizar_con_datos_productos(user_message), "📊 Análisis con datos de productos"
                
        elif st.session_state.use_web_search == "basico":
            # Sin análisis de productos
            if context:
                prompt = f"""Usa el siguiente contexto para responder a la consulta del usuario sobre dropshipping.

Contexto:
{context}

Consulta:
{user_message}

Recuerda ser conversacional y amigable, como un mentor experto en e-commerce."""
            else:
                prompt = f"""Analiza la siguiente consulta de dropshipping y proporciona información detallada.

Consulta:
{user_message}

Recuerda ser conversacional y amigable, enfocándote exclusivamente en temas de dropshipping."""
            
            return analizar_documento_solo_texto(prompt), "📝 Respuesta básica"
            
        else:  # auto
            # Detección automática
            if necesita_analisis_productos(user_message):
                return analizar_con_datos_productos(user_message), "📊 Análisis con datos de productos (detectado automáticamente)"
            else:
                # Usar contexto si está disponible
                if context:
                    prompt = f"""Usa el siguiente contexto para responder a la consulta del usuario sobre dropshipping.

Contexto:
{context}

Consulta:
{user_message}

Recuerda ser conversacional y amigable, como un mentor experto en e-commerce."""
                else:
                    prompt = f"""Analiza la siguiente consulta de dropshipping y proporciona información detallada.

Consulta:
{user_message}

Recuerda ser conversacional y amigable, enfocándote exclusivamente en temas de dropshipping."""
                
                return analizar_documento_solo_texto(prompt), "📝 Respuesta del conocimiento base"
                
    except Exception as e:
        return f"❌ Ocurrió un error al procesar tu consulta: {str(e)}", "⚠️ Error"

# ===== DISEÑO EN STREAMLIT (CSS) =====
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background-color: #f9f9fd;
    }
    
    .main-header {
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        color: white;
        padding: 2rem 3rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0;
        padding: 0;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        font-weight: 300;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    .info-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border-left: 5px solid #4b6cb7;
        transition: transform 0.2s;
    }
    
    .info-card:hover {
        transform: translateY(-3px);
    }
    
    .info-title {
        color: #182848;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 1px solid #f0f0f0;
        padding-bottom: 0.7rem;
    }
    
    .info-content {
        color: #333;
        font-size: 1rem;
        line-height: 1.7;
    }
    
    .steps-container {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-top: 1rem;
    }
    
    .step-item {
        background: #f0f4ff;
        border-radius: 8px;
        padding: 1rem;
        flex: 1;
        min-width: 200px;
        border: 1px solid #e0e7ff;
    }
    
    .step-number {
        background: #4b6cb7;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 10px;
    }
    
    .chat-container {
        background-color: white;
        border-radius: 12px;
        padding: 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    
    .chat-header {
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        color: white;
        padding: 1.2rem 1.8rem;
        font-size: 1.3rem;
        font-weight: 600;
        border-radius: 12px 12px 0 0;
        margin-bottom: 0;
    }
    
    .chat-messages {
        padding: 0;
        display: none;
        height: 0;
        max-height: 0;
        overflow: hidden;
    }
    
    .chat-input-area {
        background-color: #f5f7ff;
        border-radius: 0 0 12px 12px;
        padding: 1.2rem 1.8rem;
        display: flex;
        gap: 10px;
        align-items: flex-end;
        border-top: none;
    }
    
    .user-message {
        align-self: flex-end;
        background-color: #e1f0ff;
        color: #094067;
        padding: 12px 16px;
        border-radius: 18px 18px 0 18px;
        max-width: 80%;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .assistant-message {
        align-self: flex-start;
        background-color: #f5f7ff;
        color: #333;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 0;
        border-left: 3px solid #4b6cb7;
        max-width: 80%;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        color: white;
        font-weight: 500;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 50px;
        height: 42px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #5d7ec9 0%, #1e325b 100%);
    }
    
    /* Estilo para el botón de limpiar */
    [data-testid="baseButton-secondary"]:nth-of-type(2) {
        background: linear-gradient(135deg, #e05252 0%, #9e2b2b 100%) !important;
    }
    
    [data-testid="baseButton-secondary"]:nth-of-type(2):hover {
        background: linear-gradient(135deg, #f56767 0%, #b33636 100%) !important;
    }
    
    .stTextArea>div>div>textarea {
        border-radius: 20px;
        border: 1px solid #e0e7ff;
        padding: 10px 15px;
        min-height: 42px !important;
        font-size: 1rem;
        resize: none;
    }
    
    .stTextArea>div {
        flex-grow: 1;
    }
    
    .footer {
        text-align: center;
        padding: 1rem;
        font-size: 0.9rem;
        color: #777;
        margin-top: 2rem;
    }
    
    .sidebar .sidebar-content {
        background-color: #f1f3f9;
    }
    
    .about-app {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        color: #333;
        margin-top: 1rem;
        border-left: 3px solid #4b6cb7;
    }
    
    .benefits-list {
        list-style-type: none;
        padding-left: 0;
    }
    
    .benefits-list li {
        margin-bottom: 8px;
        display: flex;
        align-items: flex-start;
    }
    
    .benefits-list li::before {
        content: "✓";
        color: #4b6cb7;
        font-weight: bold;
        margin-right: 8px;
    }
    
    /* Estilos para tiempo y nombre del remitente */
    .message-header {
        font-size: 0.8rem;
        margin-bottom: 4px;
        display: flex;
        justify-content: space-between;
    }
    
    .message-sender {
        font-weight: bold;
    }
    
    .message-time {
        opacity: 0.7;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem;
        }
        
        .header-title {
            font-size: 2rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ===== CARGA DEL PDF =====
doc_uploader = DocumentUploader()
pdf_path = "DROPSHIPPING.pdf"
documento_cargado = False

with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem; background: #f0f4ff; border-radius: 8px;">
        <h3 style="margin-top: 0; color: #182848;">💡 Sobre esta aplicación</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Configuración de búsqueda web
    st.markdown("""
    <div style="padding: 1rem; background: #fff3cd; border-radius: 8px; margin-top: 1rem;">
        <h4 style="margin-top: 0; color: #856404;">🔍 Configuración de Búsqueda</h4>
    </div>
    """, unsafe_allow_html=True)
    
    search_option = st.selectbox(
        "Modo de análisis:",
        options=["auto", "productos", "basico"],
        format_func=lambda x: {
            "auto": "🤖 Automático (recomendado)",
            "productos": "📊 Con datos de productos",
            "basico": "📝 Solo conocimiento base"
        }[x],
        index=0,
        help="Automático: Usa datos de productos cuando detecta consultas sobre nichos/productos"
    )
    
    st.session_state.use_web_search = search_option
    
    # Indicador visual del modo actual
    if search_option == "auto":
        st.info("🤖 **Modo Automático:** Detectará automáticamente cuándo analizar productos")
    elif search_option == "productos":
        st.warning("📊 **Análisis de Productos:** Todas las respuestas incluirán datos de productos")
    else:
        st.success("📝 **Modo Básico:** Solo usará el conocimiento base (más rápido)")
    
    # Ejemplos de consultas que activan análisis de productos
    with st.expander("💡 ¿Qué consultas usan análisis de productos?"):
        st.markdown("""
        **En modo automático, estas consultas usarán datos de productos:**
        - "¿Qué nicho es más rentable?"
        - "Análisis de productos para mascotas"
        - "Mejores productos para dropshipping"
        - "¿Qué precios manejan en Amazon vs AliExpress?"
        - "Análisis de competencia en..."
        - "Margen de ganancia en..."
        
        **Estas usarán conocimiento base:**
        - "¿Cómo funciona el dropshipping?"
        - "Pasos para crear una tienda"
        - "Consejos de marketing general"
        - "Gestión de proveedores"
        """)
    
    st.markdown("---")
    
    # Cargar el documento en segundo plano sin mostrar mensajes
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            doc_uploader.add_document(f)
        
        # Crear el índice FAISS a partir del PDF
        documentos = doc_uploader.get_documents()
        if documentos:
            try:
                faiss_manager.create_faiss_index(documentos)
                documento_cargado = True
            except Exception:
                pass
    
    st.markdown("""
    <div class="about-app">
        <p style="font-size: 0.9rem; color: #333;">Esta aplicación utiliza inteligencia artificial para responder preguntas sobre dropshipping basándose en conocimiento especializado.</p>
        <p style="font-size: 0.9rem; color: #333;">Características principales:</p>
        <ul class="benefits-list">
            <li>Respuestas detalladas y precisas</li>
            <li>Análisis de nichos con datos de productos</li>
            <li>Comparación automática Amazon vs AliExpress</li>
            <li>Ejemplos prácticos y consejos</li>
            <li>Interfaz amigable e intuitiva</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ===== ESTRUCTURA PRINCIPAL =====
# Encabezado principal
st.markdown("""
<div class="main-header">
    <h1 class="header-title">GuíaShipping 🚚</h1>
    <p class="header-subtitle">Tu asistente inteligente para empezar tu negocio de dropshipping</p>
</div>
""", unsafe_allow_html=True)

# Tarjetas informativas
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <h3 class="info-title">¿Qué es el dropshipping?</h3>
        <div class="info-content">
            <p>El dropshipping es un modelo de negocio donde no necesitas mantener inventario propio. 
            Cuando un cliente compra en tu tienda, tú adquieres el producto de un proveedor que lo envía 
            directamente al cliente.</p>
            
            Este modelo te permite:
            
                Iniciar con baja inversión
                Evitar costos de almacenamiento
                Ofrecer gran variedad de productos
                Escalar fácilmente el negocio
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h3 class="info-title">Pasos para iniciar tu negocio</h3>
        <div class="info-content">
            <div class="steps-container">
                <div class="step-item">
                    <span class="step-number">1</span>
                    <span>Escoger nicho de mercado</span>
                </div>
                <div class="step-item">
                    <span class="step-number">2</span>
                    <span>Encontrar proveedores</span>
                </div>
                <div class="step-item">
                    <span class="step-number">3</span>
                    <span>Crear tienda online</span>
                </div>
                <div class="step-item">
                    <span class="step-number">4</span>
                    <span>Estrategia de marketing</span>
                </div>
                <div class="step-item">
                    <span class="step-number">5</span>
                    <span>Gestionar pedidos y atención</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== CHAT CON IA =====
st.markdown("""
<div class="chat-container">
    <div class="chat-header">
        <i class="fas fa-robot"></i> Consulta a nuestro asistente IA
    </div>
    <div class="chat-messages" id="chat-messages">
""", unsafe_allow_html=True)

# Mostrar historial de mensajes
for message in st.session_state.messages:
    sender_class = "user-message" if message["role"] == "user" else "assistant-message"
    sender_name = "Tú" if message["role"] == "user" else "Asistente IA"
    
    # Limpiar contenido de todas las etiquetas HTML que puedan aparecer en la respuesta
    content = message["content"]
    content = content.replace("</div>", "").replace("<div>", "")
    content = content.replace("</div", "").replace("<div", "")
    content = content.replace("</", "").replace("<", "")
    content = content.replace("`</div>`", "").replace("`<div>`", "")
    
    # Mostrar indicador de tipo de respuesta si está disponible
    analysis_type = message.get("analysis_type", "")
    type_indicator = f"<small style='color: #666; font-style: italic;'>{analysis_type}</small><br>" if analysis_type else ""
    
    st.markdown(f"""
    <div class="{sender_class}">
        <div class="message-header">
            <span class="message-sender">{sender_name}</span>
            <span class="message-time">{message["time"]}</span>
        </div>
        {type_indicator}{content}
    """, unsafe_allow_html=True)

st.markdown("""
    </div>
    <div class="chat-input-area">
""", unsafe_allow_html=True)

# Área de entrada del chat
col1, col2, col3 = st.columns([5, 0.8, 0.8])
with col1:
    user_message = st.text_area("Mensaje", placeholder="Escribe tu mensaje aquí...", label_visibility="collapsed", key="user_input")

with col2:
    send_clicked = st.button("Enviar")

with col3:
    clear_clicked = st.button("Limpiar", on_click=limpiar_chat)

# Procesar envío (ya sea por botón o Enter)
if send_clicked and user_message.strip():
    # Obtener tiempo actual
    from datetime import datetime
    current_time = datetime.now().strftime("%H:%M")
    
    # Guardar mensaje del usuario
    st.session_state.messages.append({
        "role": "user",
        "content": user_message,
        "time": current_time
    })
    
    # Generar respuesta usando la función inteligente
    spinner_text = "📊 Analizando productos..." if (st.session_state.use_web_search == "productos" or 
                   (st.session_state.use_web_search == "auto" and necesita_analisis_productos(user_message))) else "El asistente está pensando..."
    
    with st.spinner(spinner_text):
        context = ""
        if documento_cargado:
            try:
                # Buscar fragmentos relevantes en el documento
                top_chunks = faiss_manager.search_similar_chunks(user_message, k=2)
                context = "\n\n".join(top_chunks)
            except Exception:
                context = ""
        
        # Obtener respuesta usando la función inteligente
        response, analysis_type = obtener_respuesta_inteligente(user_message, context)
    
    # Guardar respuesta del asistente con el tipo de análisis
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "time": datetime.now().strftime("%H:%M"),
        "analysis_type": analysis_type
    })
    
    # No intentar modificar st.session_state.user_input directamente
    # Recargar para mostrar la nueva conversación
    st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <p>© 2024 GuíaShipping - Asistente de Dropshipping | Desarrollado con ❤️ y tecnología IA</p>
</div>
""", unsafe_allow_html=True)

# Script JavaScript para controlar el desplazamiento y el envío con Enter
st.markdown("""
<script>
    // Este script se ejecutará cuando se cargue la página
    document.addEventListener('DOMContentLoaded', function() {
        // Scroll automático al final del chat
        var chatMessages = document.getElementById('chat-messages');
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        // Enviar mensaje con Enter
        var textarea = document.querySelector('textarea');
        if (textarea) {
            textarea.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    document.querySelector('button[data-testid="baseButton-secondary"]').click();
                }
            });
        }
    });
</script>
""", unsafe_allow_html=True)
