# Comandos útiles en el servidor (SSH root@82.25.66.67)

---

## Ver archivos .env

```bash
# .env del backend
cat /opt/country/backend/.env

# .env de producción del frontend
cat /opt/country/frontend/.env.production
```

---

## Logs del backend en tiempo real

```bash
# Todos los logs (recomendado)
journalctl -u country-backend -f

# Solo los últimos 100 líneas + tiempo real
journalctl -u country-backend -n 100 -f

# Filtrar solo errores
journalctl -u country-backend -f | grep -i "error\|exception\|traceback"

# Filtrar logs de Telegram específicamente
journalctl -u country-backend -f | grep -i "telegram\|webhook\|bot"
```

---

## Estado del backend

```bash
# Ver si el servicio está activo
systemctl status country-backend

# Reiniciar el backend
systemctl restart country-backend

# Ver los últimos logs tras un reinicio
journalctl -u country-backend -n 50
```

---

## Verificar webhook de Telegram

```bash
# Ver qué webhook tiene registrado el bot actualmente
curl "https://api.telegram.org/botTU_BOT_TOKEN_AQUI/getWebhookInfo"

# Registrar el webhook manualmente apuntando al servidor nuevo
curl "https://api.telegram.org/botTU_BOT_TOKEN_AQUI/setWebhook?url=https://api.countryclub.doc-ia.cloud/telegram/webhook"

# Eliminar el webhook (útil para depurar)
curl "https://api.telegram.org/botTU_BOT_TOKEN_AQUI/deleteWebhook"
```

---

## Verificar conectividad

```bash
# Comprobar que el backend responde
curl https://api.countryclub.doc-ia.cloud/

# Comprobar el endpoint de Telegram desde el servidor
curl -X POST https://api.countryclub.doc-ia.cloud/telegram/webhook \
     -H "Content-Type: application/json" \
     -d '{"message":{"text":"/test","chat":{"id":0},"from":{"id":0}}}'
```

---

## Nginx

```bash
# Ver errores de Nginx
tail -f /var/log/nginx/error.log

# Ver accesos en tiempo real
tail -f /var/log/nginx/access.log

# Recargar configuración sin cortar conexiones
systemctl reload nginx
```
