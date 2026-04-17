#!/usr/bin/env python3
"""
News Bot: Daily aggregator for important Mexico and World news using NewsAPI
Executes once daily at 4 PM Mexico time
Sends curated summaries to Telegram
"""

import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

# ===================== CONFIGURACIÓN =====================
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')

# NewsAPI endpoint
NEWSAPI_URL = "https://newsapi.org/v2/everything"

# Palabras clave para noticias IMPORTANTES
IMPORTANT_KEYWORDS_MX = [
    'México president',
    'México política',
    'México economía',
    'México crimen',
    'México seguridad',
    'CDMX',
    'México desastre',
    'México reforma',
    'México impuestos'
]

IMPORTANT_KEYWORDS_WORLD = [
    'world breaking news',
    'world conflict',
    'world economy',
    'international crisis',
    'major incident',
    'USA politics',
    'China',
    'Russia',
    'Europe crisis'
]

# ===================== FUNCIONES =====================

def get_important_mexico_news():
    """Obtiene noticias IMPORTANTES de México de HOY"""
    from datetime import date
    today = date.today().isoformat()
    
    all_articles = []
    
    for keyword in IMPORTANT_KEYWORDS_MX:
        try:
            params = {
                'q': keyword,
                'sortBy': 'relevancy',
                'language': 'es',
                'from': today,  # Solo noticias de hoy
                'to': today,
                'pageSize': 5,
                'apiKey': NEWSAPI_KEY
            }
            response = requests.get(NEWSAPI_URL, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for article in data.get('articles', []):
                    all_articles.append({
                        'title': article.get('title', 'Sin título'),
                        'link': article.get('url', ''),
                        'source': article.get('source', {}).get('name', 'Desconocida'),
                        'publishedAt': article.get('publishedAt', ''),
                    })
        except Exception as e:
            logger.warning(f"⚠️ Error obteniendo {keyword}: {e}")
    
    # Eliminar duplicados y ordenar por fecha
    seen = set()
    unique_articles = []
    for article in sorted(all_articles, key=lambda x: x['publishedAt'], reverse=True):
        title_lower = article['title'].lower()
        if title_lower not in seen:
            seen.add(title_lower)
            unique_articles.append(article)
    
    logger.info(f"✓ México: {len(unique_articles[:10])} noticias importantes de HOY obtenidas")
    return unique_articles[:10]


def get_important_world_news():
    """Obtiene noticias IMPORTANTES del mundo de HOY"""
    from datetime import date
    today = date.today().isoformat()
    
    all_articles = []
    
    for keyword in IMPORTANT_KEYWORDS_WORLD:
        try:
            params = {
                'q': keyword,
                'sortBy': 'relevancy',
                'language': 'en',
                'from': today,  # Solo noticias de hoy
                'to': today,
                'pageSize': 5,
                'apiKey': NEWSAPI_KEY
            }
            response = requests.get(NEWSAPI_URL, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for article in data.get('articles', []):
                    all_articles.append({
                        'title': article.get('title', 'Sin título'),
                        'link': article.get('url', ''),
                        'source': article.get('source', {}).get('name', 'Desconocida'),
                        'publishedAt': article.get('publishedAt', ''),
                    })
        except Exception as e:
            logger.warning(f"⚠️ Error obteniendo {keyword}: {e}")
    
    # Eliminar duplicados y ordenar por fecha
    seen = set()
    unique_articles = []
    for article in sorted(all_articles, key=lambda x: x['publishedAt'], reverse=True):
        title_lower = article['title'].lower()
        if title_lower not in seen:
            seen.add(title_lower)
            unique_articles.append(article)
    
    logger.info(f"✓ Mundo: {len(unique_articles[:10])} noticias importantes de HOY obtenidas")
    return unique_articles[:10]


def build_telegram_message(mexico_news, world_news):
    """Construye el mensaje para Telegram - Solo titulares"""
    message = "📰 *TOP NOTICIAS DEL DÍA*\n\n"
    
    # Noticias de México
    message += "🇲🇽 *MÉXICO*\n"
    if mexico_news:
        for i, article in enumerate(mexico_news[:10], 1):
            message += f"{i}. {article['title']}\n"
    else:
        message += "Sin noticias disponibles\n"
    
    # Noticias del Mundo
    message += "\n🌍 *MUNDO*\n"
    if world_news:
        for i, article in enumerate(world_news[:10], 1):
            message += f"{i}. {article['title']}\n"
    else:
        message += "Sin noticias disponibles\n"
    
    message += "\n_NewsAPI - Noticias de hoy_"
    
    return message


def send_telegram_message(message):
    """Envía el mensaje a Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            logger.info("✓ Mensaje enviado a Telegram")
            return True
        else:
            logger.error(f"✗ Error Telegram: {response.text}")
            return False
    except Exception as e:
        logger.error(f"✗ Excepción Telegram: {e}")
        return False


def main():
    """Función principal"""
    logger.info("🚀 Iniciando News Bot...")
    logger.info("📥 Buscando noticias importantes...")
    
    # Obtener noticias importantes
    mexico_news = get_important_mexico_news()
    world_news = get_important_world_news()
    
    logger.info(f"📊 Total: {len(mexico_news)} de México, {len(world_news)} del mundo")
    
    # Construir y enviar mensaje
    message = build_telegram_message(mexico_news, world_news)
    send_telegram_message(message)
    
    logger.info("✅ Completado")


if __name__ == '__main__':
    main()
