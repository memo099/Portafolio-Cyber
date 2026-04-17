#!/usr/bin/env python3
"""
News Bot: Daily aggregator for Mexico and World news
Executes once daily at 4 PM Mexico time
Filters only verified news sources
Sends curated summaries to Telegram
"""

import feedparser
import requests
from datetime import datetime
from collections import defaultdict
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

# Fuentes verificadas con sus feeds RSS
VERIFIED_SOURCES = {
    # México
    'méxico': {
        'El Universal': 'https://www.eluniversal.com.mx/feed/noticias/',
        'Latinus': 'https://www.latinus.mx/feed/',
        'Reforma': 'https://www.reforma.com/rss/portada.xml',
    },
    # Mundo
    'mundo': {
        'Reuters': 'https://feeds.reuters.com/reuters/newsOne',
        'BBC News': 'https://feeds.bbc.co.uk/news/rss.xml',
        'CNN': 'https://feeds.cnn.com/cnn/cnn-world-rss.xml',
        'The New York Times': 'https://feeds.nytimes.com/services/xml/rss/nyt/World.xml',
    }
}

# ===================== FUNCIONES =====================

def fetch_feed(feed_url, source_name):
    """Obtiene y parsea un feed RSS"""
    try:
        feed = feedparser.parse(feed_url)
        
        articles = []
        for entry in feed.entries[:5]:  # Top 5 por fuente
            article = {
                'title': entry.get('title', 'Sin título'),
                'link': entry.get('link', ''),
                'source': source_name,
            }
            articles.append(article)
        
        logger.info(f"✓ {source_name}: {len(articles)} artículos obtenidos")
        return articles
    except Exception as e:
        logger.error(f"✗ Error en {source_name}: {e}")
        return []


def build_telegram_message(mexico_news, world_news):
    """Construye el mensaje para Telegram"""
    message = "📰 *Resumen de Noticias del Día*\n\n"
    message += f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    
    # Noticias de México
    message += "🇲🇽 *MÉXICO*\n"
    message += "─" * 40 + "\n"
    if mexico_news:
        for i, article in enumerate(mexico_news[:5], 1):
            title = article['title'][:70] + "..." if len(article['title']) > 70 else article['title']
            message += f"{i}. {title}\n"
            message += f"   📌 {article['source']}\n"
            if article['link']:
                message += f"   🔗 {article['link']}\n"
            message += "\n"
    else:
        message += "Sin noticias disponibles\n\n"
    
    # Noticias del Mundo
    message += "🌍 *MUNDO*\n"
    message += "─" * 40 + "\n"
    if world_news:
        for i, article in enumerate(world_news[:5], 1):
            title = article['title'][:70] + "..." if len(article['title']) > 70 else article['title']
            message += f"{i}. {title}\n"
            message += f"   📌 {article['source']}\n"
            if article['link']:
                message += f"   🔗 {article['link']}\n"
            message += "\n"
    else:
        message += "Sin noticias disponibles\n\n"
    
    message += "─" * 40 + "\n"
    message += "_Fuentes: El Universal, Latinus, Reforma, Reuters, BBC, CNN, NYT_"
    
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
    
    all_articles = defaultdict(list)
    
    # Obtener noticias de México
    logger.info("📥 Obteniendo noticias de México...")
    for source_name, feed_url in VERIFIED_SOURCES['méxico'].items():
        articles = fetch_feed(feed_url, source_name)
        all_articles['méxico'].extend(articles)
    
    # Obtener noticias del Mundo
    logger.info("📥 Obteniendo noticias del Mundo...")
    for source_name, feed_url in VERIFIED_SOURCES['mundo'].items():
        articles = fetch_feed(feed_url, source_name)
        all_articles['mundo'].extend(articles)
    
    # Rankear por fecha (más recientes primero)
    mexico_news = sorted(all_articles['méxico'], key=lambda x: x['title'])[:10]
    world_news = sorted(all_articles['mundo'], key=lambda x: x['title'])[:10]
    
    logger.info(f"📊 Total: {len(mexico_news)} noticias de México, {len(world_news)} del mundo")
    
    # Construir y enviar mensaje
    message = build_telegram_message(mexico_news, world_news)
    send_telegram_message(message)
    
    logger.info("✅ Completado")


if __name__ == '__main__':
    main()
