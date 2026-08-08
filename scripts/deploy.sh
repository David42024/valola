#!/bin/bash
# deploy.sh - Script para desplegar Valola en la nube

set -e

echo "🚀 Desplegando Valola..."

# 1. Subir a GitHub
echo "📤 Subiendo a GitHub..."
git add .
git commit -m "Deploy: $(date +'%Y-%m-%d %H:%M')" || echo "No hay cambios para commitear"
git push -u origin main

# 2. Render (blueprint)
echo "🏗️ Notificando a Render..."
# Si tienes RENDER_SERVICE_ID y RENDER_API_KEY configurados en .env, descomenta:
# source .env
# curl -X POST \
#   -H "Authorization: Bearer $RENDER_API_KEY" \
#   -H "Content-Type: application/json" \
#   "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys"

echo "✅ Código subido. GitHub Actions/blueprint de Render se encargará del resto."
echo "   Revisa: https://render.com"