#!/bin/bash
# Script para verificar status dos serviços Docker

echo "🔍 Verificando status dos containers Docker..."
echo ""

cd /opt/aumivet

echo "📦 Containers em execução:"
docker compose ps

echo ""
echo "🔗 Testando conectividade:"
echo -n "Frontend (porta 3000): "
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:3000 && echo " ✅" || echo " ❌"

echo -n "Strapi (porta 1337): "
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:1337 && echo " ✅" || echo " ❌"

echo ""
echo "📋 Últimas linhas dos logs do Frontend:"
docker compose logs --tail=5 frontend

echo ""
echo "📋 Últimas linhas dos logs do Strapi:"
docker compose logs --tail=5 strapi

echo ""
echo "💾 Status dos containers:"
docker ps --filter "name=aumivet" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

