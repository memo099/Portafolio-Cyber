import feedparser
import os
import requests
from datetime import datetime, timezone, timedelta

# ── CONFIG ───────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# ── FUENTES RSS + SUBSTACK ────────────────────────────────────────────────────
FEEDS = [
    # Medios principales
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://www.darkreading.com/rss.xml",
    "https://securityaffairs.com/feed",
    "https://www.cisa.gov/news.xml",
    "https://krebsonsecurity.com/feed/",
    "https://cyberscoop.com/feed/",
    "https://therecord.media/feed/",
    # Substack - threat intel y geopolítica
    "https://riskybiznews.substack.com/feed",       # Risky Business News - breaches diarios
    "https://cybergeopolitics.substack.com/feed",   # Geopolítica cyber
    "https://thecyberwhy.substack.com/feed",        # Análisis de incidentes
    "https://ransomware.substack.com/feed",         # Ransomware específico
    "https://allenwestbrook.substack.com/feed",     # Threat intel
    # Extra
    "https://schneier.com/feed/atom/",              # Bruce Schneier - análisis profundo
    "https://isc.sans.edu/rssfeed_full.xml",        # SANS ISC - alertas técnicas
]

# ── KEYWORDS ──────────────────────────────────────────────────────────────────
KEYWORDS_MX = [
    "mexico", "méxico", "sat", "imss", "pemex", "banxico",
    "latam", "latin america", "america latina", "cdmx",
    "gobierno mexico", "condusef", "secretaria de", "ejercito mexicano",
    "banco mexico", "bbva mexico", "telcel", "telmex"
]

KEYWORDS_GLOBAL = [
    # Grupos APT por nación
    "apt28", "apt29", "apt41", "apt40", "apt42",
    "lazarus group", "sandworm", "cozy bear", "fancy bear",
    "volt typhoon", "salt typhoon", "flax typhoon", "kimsuky",
    "charming kitten", "muddy water", "turla", "gamaredon",
    # Naciones
    "chinese hackers", "russian hackers", "iranian hackers",
    "north korean hackers", "state-sponsored", "nation-state",
    # Guerra cyber / espionaje
    "cyberwarfare", "cyber warfare", "cyberespionage", "espionage",
    "critical infrastructure attack", "sabotage", "psyop",
    # Incidentes graves
    "ransomware attack", "data breach", "database exposed",
    "millions of records", "records leaked", "records stolen",
    "hacked", "compromised", "extortion", "darkweb leak",
    "stolen credentials", "supply chain attack",
    # Infraestructura crítica
    "hospital ransomware", "government hacked", "energy sector breach",
    "water system hack", "power grid attack", "pipeline attack",
    # Grupos ransomware activos
    "lockbit", "ransomhub", "blackcat", "alphv", "cl0p",
    "scattered spider", "revil", "conti", "play ransomware",
    "akira ransomware", "black basta", "medusa ransomware",
    # Vulnerabilidades críticas
    "zero-day exploit", "actively exploited", "critical vulnerability",
    "remote code execution", "ivanti", "fortinet", "palo alto exploit"
]

# ── FUNCIONES ─────────────────────────────────────────────────────────────────
def fetch_recent_news(hours=24):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    mx_articles = []
    global_articles = []

    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    pub = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                else:
                    pub = datetime.now(timezone.utc)

                if pub < cutoff:
                    continue

                title    = entry.get("title", "Sin título")
                summary  = entry.get("summary", "")[:300]
                link     = entry.get("link", "")
                combined = (title + " " + summary).lower()

                is_mx     = any(kw in combined for kw in KEYWORDS_MX)
                is_global = any(kw in combined for kw in KEYWORDS_GLOBAL)

                if is_mx:
                    mx_articles.append(f"🇲🇽 *{title}*\n{link}")
                elif is_global:
                    global_articles.append(f"🌐 *{title}*\n{link}")

        except Exception as e:
            print(f"Error en feed {url}: {e}")

    return mx_articles, global_articles


def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
    for chunk in chunks:
        r = requests.post(url, json={
            "chat_id": int(TELEGRAM_CHAT_ID),
            "text": chunk,
            "parse_mode": "Markdown"
        })
        print(f"Telegram response: {r.status_code} - {r.text}")

# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Recopilando noticias...")
    mx, globales = fetch_recent_news(hours=24)
    print(f"  México: {len(mx)} | Global: {len(globales)}")

    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    msg = f"🔒 *CyberNews MX* — {now}\n\n"

    if mx:
        msg += "*━━━ MÉXICO ━━━*\n\n"
        msg += "\n\n".join(mx[:5])
        msg += "\n\n"

    if globales:
        msg += "*━━━ GLOBAL ━━━*\n\n"
        msg += "\n\n".join(globales[:15])

    if not mx and not globales:
        msg += "Sin incidentes relevantes en las últimas 24 horas."

    send_telegram(msg)
    print("Mensaje enviado a Telegram.")
