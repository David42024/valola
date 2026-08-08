# Valola - Sistema Multi-Agente para WhatsApp

## 🚀 Descripción
Valola es un sistema inteligente de gestión empresarial vía WhatsApp que utiliza múltiples agentes especializados para responder consultas de inventario, finanzas, proveedores, marketing y más.

## 🏗️ Arquitectura
- **Frontend**: WhatsApp Business API
- **Orquestador**: n8n Cloud
- **API**: FastAPI (Render)
- **Base de Datos**: PostgreSQL (Render)
- **Memoria/Caché**: Redis (Upstash)
- **Vector DB**: Pinecone
- **IA**: OpenAI GPT-4

## 📦 Servicios Gratuitos Utilizados
| Servicio | Propósito | Límite Gratuito |
|----------|-----------|-----------------|
| n8n Cloud | Orquestador | 2 flujos activos |
| Render | API + BD | 750 horas/mes |
| Upstash | Redis | 10k req/día |
| Pinecone | Vector DB | 1GB |

## 🛠️ Instalación Local (opcional)

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/valola.git
cd valola

# Crear .env
cp .env.example .env

# Ejecutar con Docker
docker-compose up -d

# Acceder a servicios
# n8n: http://localhost:5678
# FastAPI: http://localhost:8000
# pgAdmin: http://localhost:5050
```

## 🌐 Despliegue en Producción

### 1. Render (API + BD)
```bash
# Conectar repositorio a Render
# Usar render.yaml para configuración automática
```

### 2. Upstash (Redis)
```bash
# Crear cuenta en upstash.com
# Obtener REDIS_URL y REDIS_TOKEN
```

### 3. Pinecone (Vector DB)
```bash
# Crear cuenta en pinecone.io
# Obtener API Key y Environment
```

### 4. n8n Cloud
```bash
# Importar flujo desde n8n/flows/valola-flow.json
# Configurar webhook con URL de Render
```

## 📊 Endpoints API

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Información de la API |
| `/health` | GET | Estado de servicios |
| `/api/whatsapp/webhook` | POST | Webhook WhatsApp |
| `/api/agents/inventory` | POST | Agente de inventario |
| `/api/agents/finance` | POST | Agente de finanzas |

## 🔧 Variables de Entorno

Ver `.env.example` para la lista completa.

## 📝 Flujo de Trabajo

1. Usuario envía mensaje a WhatsApp
2. Meta envía webhook a n8n
3. n8n procesa y llama a FastAPI
4. FastAPI clasifica y ejecuta agentes
5. Resultado se envía de vuelta al usuario

## 🤝 Contribución

1. Fork el repositorio
2. Crea tu rama de feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia
MIT

## 📞 Contacto
Email: soporte@valola.com  
WhatsApp: +51 9XX XXX XXX