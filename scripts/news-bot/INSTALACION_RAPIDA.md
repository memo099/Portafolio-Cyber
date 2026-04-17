# 🚀 Instalación Rápida - News Bot

## Tus Credenciales (Ya Configuradas)
```
Token: 8766476117:AAELU2l0NUwlKSR-C8UWmxgYxdaQXgKZ7KU
Chat ID: 5793890955
```

---

## ⚡ 5 Pasos Rápidos

### Paso 1: Crear carpeta
```bash
mkdir -p ~/Portafolio-Cyber/scripts/news-bot
cd ~/Portafolio-Cyber/scripts/news-bot
```

### Paso 2: Copiar archivos a esta carpeta
Descarga estos 3 archivos y ponlos en `scripts/news-bot/`:
- `news_bot.py`
- `requirements.txt`
- `.env`

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Probar localmente
```bash
python news_bot.py
```

Si ves esto = **¡Funcionó!** ✅
```
🚀 Iniciando News Bot...
📥 Obteniendo noticias de México...
✓ El Universal: 5 artículos obtenidos
✓ Latinus: 5 artículos obtenidos
✓ Reforma: 5 artículos obtenidos
📥 Obteniendo noticias del Mundo...
...
✓ Mensaje enviado a Telegram
✅ Completado
```

Y deberías recibir un mensaje en Telegram.

---

### Paso 5: Configurar GitHub Actions

**5a. Crear carpeta del workflow**
```bash
mkdir -p ~/.github/workflows
```

**5b. Copiar el archivo workflow**
Descarga `daily-news.yml` y ponlo en `.github/workflows/`

**5c. Configurar secretos en GitHub**
1. Ve a tu repo en GitHub.com
2. Click en **Settings**
3. Click en **Secrets and variables** → **Actions**
4. Click en **New repository secret**

Agrega estos 2 secretos:

| Name | Value |
|------|-------|
| `TELEGRAM_BOT_TOKEN` | `8766476117:AAELU2l0NUwlKSR-C8UWmxgYxdaQXgKZ7KU` |
| `TELEGRAM_CHAT_ID` | `5793890955` |

**5d. Hacer push**
```bash
git add .
git commit -m "add news bot"
git push
```

**5e. Probar en GitHub Actions**
1. Ve a tu repo en GitHub
2. Click en **Actions**
3. Click en **Daily News Bot** (o el nombre del workflow)
4. Click en **Run workflow** → **Run workflow**
5. Espera 30 segundos y revisa Telegram

---

## ⏰ Horario

El bot se ejecutará **automáticamente cada día a las 4 PM (16:00) México**.

Puedes ejecutarlo manualmente en GitHub Actions cuando quieras.

---

## ✅ Checklist

- [ ] Creé `scripts/news-bot/`
- [ ] Copié los 3 archivos (news_bot.py, requirements.txt, .env)
- [ ] Ejecuté `pip install -r requirements.txt`
- [ ] Probé con `python news_bot.py`
- [ ] Recibí un mensaje en Telegram ✨
- [ ] Creé `.github/workflows/daily-news.yml`
- [ ] Agregué los 2 secretos en GitHub
- [ ] Hice push a GitHub
- [ ] Ejecuté el workflow desde GitHub Actions

---

## 🐛 Si No Funciona

### No recibo el mensaje en Telegram
- Verifica que escribiste algo en el bot primero (para activar el chat)
- Revisa los logs en GitHub Actions
- Comprueba que el token y chat ID sean exactos

### Error: `ModuleNotFoundError`
```bash
# Asegúrate que instalaste:
pip install -r requirements.txt
```

### El horario no es exacto
- GitHub Actions puede tardar 5-10 minutos
- El cron es aproximado, no exacto al segundo

---

¿Preguntas? Avísame en qué paso te atascas 💪
