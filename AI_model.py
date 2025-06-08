# AI_model.py
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Verificar si la API Key está configurada
if not GEMINI_API_KEY:
    raise ValueError("No se encontró la API Key de Gemini. Asegúrate de agregar GEMINI_API_KEY en las variables de entorno.")

def analizar_documento_solo_texto(prompt):
    """
    Genera texto usando el modelo Gemini 1.5 Flash.
    """
    try:
        # Configurar la API de Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Crear instrucciones del sistema para respuestas más detalladas
        system_message = """Eres GuíaShipping, un asistente conversacional especializado exclusivamente en dropshipping y comercio electrónico.
        Tienes una personalidad amigable y hablas de forma natural, como lo haría un mentor experto en negocios digitales.
        
        CAPACIDADES:
        1. ANÁLISIS DE NICHOS: Puedes sugerir nichos de mercado rentables para dropshipping basados en tendencias actuales,
           considerando factores como competencia, margenes, demanda estacional y potencial de crecimiento.
        
        2. BÚSQUEDA DE PRODUCTOS: Puedes recomendar tipos de productos específicos dentro de un nicho,
           con detalles sobre por qué podrían funcionar bien, rangos de precios estimados y posibles proveedores.
        
        3. ESTRATEGIAS DE MARKETING: Ofreces consejos sobre métodos efectivos de promoción para tiendas de dropshipping,
           incluyendo marketing en redes sociales, SEO, email marketing y publicidad pagada.
        
        4. LOGÍSTICA Y OPERACIONES: Explicas aspectos operativos como gestión de proveedores, tiempos de envío,
           servicio al cliente, manejo de devoluciones y aspectos legales del dropshipping.
        
        5. ANÁLISIS DE PLATAFORMAS: Comparas diferentes plataformas para crear tiendas (Shopify, WooCommerce, etc.)
           y marketplaces (Amazon, eBay, etc.) para dropshipping, con sus ventajas y desventajas.
        
        RESTRICCIONES:
        - LIMITA TUS RESPUESTAS EXCLUSIVAMENTE AL ÁMBITO DEL DROPSHIPPING Y COMERCIO ELECTRÓNICO.
        - NO proporciones información sobre temas no relacionados con el dropshipping.
        - NO des consejos sobre inversiones financieras, criptomonedas, o temas ajenos al e-commerce.
        - NO menciones que estás analizando un documento o datos específicos.
        - NUNCA des opiniones políticas, religiosas o sobre temas controvertidos.
        
        ESTILO DE RESPUESTA:
        1. Sé directo y conversacional, como un mentor experimentado hablando con un amigo.
        2. Proporciona ejemplos concretos y accionables cuando sea posible.
        3. Estructura tus respuestas de manera clara pero informal.
        4. Puedes usar emojis ocasionalmente para dar un toque más humano.
        5. Adapta el nivel de detalle técnico según el tipo de pregunta.
        6. Si la pregunta es ambigua, interpreta lo que sea más útil en el contexto del dropshipping.
        7. Si no tienes información sobre algo específico del dropshipping, reconócelo honestamente.
        
        Al recomendar nichos o productos:
        - Menciona el potencial de mercado y tendencias actuales
        - Explica por qué podría ser rentable o problemático
        - Sugiere formas de evaluar la competencia
        - Ofrece consejos prácticos para comenzar en ese nicho
        - Da ejemplos de productos específicos dentro del nicho
        
        Recuerda que tu objetivo principal es ayudar a emprendedores a tener éxito en sus negocios de dropshipping, 
        proporcionando información útil, actualizada y práctica para cada etapa del proceso."""
        
        # Crear el prompt completo con el mensaje del sistema
        prompt_completo = f"{system_message}\n\n{prompt}"
        
        # Generar respuesta con el modelo Gemini
        model = genai.GenerativeModel("gemini-1.5-flash-8b")
        response = model.generate_content(prompt_completo)
        
        # Extraer el texto de la respuesta
        content = response.text
        
        print(content)
        return content

    except Exception as e:
        return f"❌ Error al analizar el documento: {e}"

def get_amazon_real_data(search_term, rapidapi_key):
    """Obtiene datos reales de Amazon usando RapidAPI"""
    try:
        import requests
        
        url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/search"
        
        headers = {
            "X-RapidAPI-Key": rapidapi_key,
            "X-RapidAPI-Host": "amazon-product-reviews-keywords.p.rapidapi.com"
        }
        
        params = {
            "keyword": search_term,
            "country": "US",
            "category": "aps"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            productos = []
            
            for item in data.get("products", [])[:5]:  # Limitar a 5 productos
                productos.append({
                    "titulo": item.get("title", "N/A"),
                    "precio": item.get("price", "N/A"),
                    "rating": item.get("rating", "N/A"),
                    "reviews": item.get("reviews_count", "N/A"),
                    "url": item.get("url", "N/A")
                })
            
            return {"productos": productos, "source": "Amazon API Real"}
        else:
            print(f"⚠️ Error Amazon API: {response.status_code}")
            return get_amazon_mock_data(search_term)
            
    except Exception as e:
        print(f"⚠️ Error conectando Amazon API: {e}")
        return get_amazon_mock_data(search_term)

def get_aliexpress_real_data(search_term, rapidapi_key):
    """Obtiene datos reales de AliExpress usando RapidAPI"""
    try:
        import requests
        
        url = "https://aliexpress-datahub.p.rapidapi.com/item_search"
        
        headers = {
            "X-RapidAPI-Key": rapidapi_key,
            "X-RapidAPI-Host": "aliexpress-datahub.p.rapidapi.com"
        }
        
        params = {
            "q": search_term,
            "page": 1
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            productos = []
            
            for item in data.get("result", {}).get("resultList", [])[:5]:
                productos.append({
                    "titulo": item.get("subject", "N/A"),
                    "precio": f"${item.get('priceInfo', {}).get('discountPrice', 'N/A')}",
                    "precio_original": f"${item.get('priceInfo', {}).get('originalPrice', 'N/A')}",
                    "pedidos": item.get("tradeInfo", {}).get("sellerOrderCount", "N/A"),
                    "rating": item.get("evalInfo", {}).get("starRating", "N/A"),
                    "envio_gratis": item.get("logisticsInfo", {}).get("freeshipping", False)
                })
            
            return {"productos": productos, "source": "AliExpress API Real"}
        else:
            print(f"⚠️ Error AliExpress API: {response.status_code}")
            return get_aliexpress_mock_data(search_term)
            
    except Exception as e:
        print(f"⚠️ Error conectando AliExpress API: {e}")
        return get_aliexpress_mock_data(search_term)

def get_amazon_mock_data(search_term):
    """Datos simulados de Amazon como fallback"""
    return {
        "productos": [
            {"titulo": f"{search_term} - Best Seller", "precio": "$29.99", "rating": 4.5, "reviews": 1250},
            {"titulo": f"{search_term} Premium", "precio": "$45.99", "rating": 4.7, "reviews": 890}
        ],
        "source": "Amazon Mock Data"
    }

def get_aliexpress_mock_data(search_term):
    """Datos simulados de AliExpress como fallback"""
    return {
        "productos": [
            {"titulo": f"{search_term} Wholesale", "precio": "$8.99", "precio_original": "$15.99", "pedidos": 2500},
            {"titulo": f"{search_term} Bulk", "precio": "$12.50", "precio_original": "$20.00", "pedidos": 1800}
        ],
        "source": "AliExpress Mock Data"
    }

def analizar_con_datos_productos(nicho_query):
    """
    Analiza un nicho usando datos reales de productos para dropshipping
    """
    try:
        # Configurar la API de Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        
        # API Keys
        rapidapi_key = os.getenv("RAPIDAPI_KEY")
        
        # Obtener datos reales de productos
        amazon_data = get_amazon_real_data(nicho_query, rapidapi_key) if rapidapi_key else get_amazon_mock_data(nicho_query)
        aliexpress_data = get_aliexpress_real_data(nicho_query, rapidapi_key) if rapidapi_key else get_aliexpress_mock_data(nicho_query)
        
        # Crear contexto con datos de productos
        context = f"""
        ANÁLISIS DE PRODUCTOS PARA DROPSHIPPING: {nicho_query}
        
        DATOS DE AMAZON:
        {amazon_data}
        
        DATOS DE ALIEXPRESS: 
        {aliexpress_data}
        """
        
        # Prompt especializado para análisis con datos de productos
        system_message = """Eres GuíaShipping, un experto en análisis de productos para dropshipping.
        Analiza los datos reales de productos proporcionados y genera un análisis completo que incluya:
        
        📊 RESUMEN DEL NICHO (viabilidad, competencia, oportunidades)
        💰 ANÁLISIS DE PRECIOS (márgenes, comparación plataformas)  
        🎯 PRODUCTOS DESTACADOS (mejores oportunidades)
        📈 MÉTRICAS CLAVE (ratings, demanda, reviews)
        🚀 RECOMENDACIONES (estrategias, próximos pasos)
        
        Sé conversacional y da consejos prácticos como un mentor experto."""
        
        prompt_completo = f"{system_message}\n\n{context}\n\nAnaliza este nicho para dropshipping."
        
        # Generar respuesta
        model = genai.GenerativeModel("gemini-1.5-flash-8b")
        response = model.generate_content(prompt_completo)
        
        content = response.text
        print(content)
        return content
        
    except Exception as e:
        return f"❌ Error en análisis con datos de productos: {e}"
