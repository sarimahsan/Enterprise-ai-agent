# FlowForge AI - Docker Deployment Guide

## Overview

This guide provides complete instructions for deploying FlowForge AI using Docker and Docker Compose. All services are containerized and orchestrated together for seamless deployment.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Nginx (Reverse Proxy)              │
│                     Port: 80/443                        │
└────────────────┬──────────────────────────┬─────────────┘
                 │                          │
         ┌───────▼────────┐        ┌────────▼─────────┐
         │   Frontend     │        │    Backend       │
         │   React App    │        │    FastAPI       │
         │   Port: 3000   │        │    Port: 8000    │
         └────────────────┘        └────────┬─────────┘
                                            │
                                   ┌────────▼─────────┐
                                   │   PostgreSQL     │
                                   │   Database       │
                                   │   Port: 5432     │
                                   └──────────────────┘
```

## Prerequisites

- Docker Engine (v20.10+)
- Docker Compose (v3.8+)
- Git (for cloning the repository)
- At least 4GB RAM and 10GB disk space

### Installation

**Windows, macOS, or Linux:**
- Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop)

## Quick Start

### 1. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# nano .env  (Linux/macOS)
# Edit .env  (Windows)
```

**Essential .env variables:**
```env
DB_USER=flowforge
DB_PASSWORD=change_this_to_strong_password
DB_NAME=flowforge_db
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_secret
OPENAI_API_KEY=your_openai_api_key
DEBUG=false
```

### 2. Start Services

```bash
# Linux/macOS
./deploy.sh up

# Windows
deploy.bat up
```

**Expected output:**
```
Creating flowforge-db       ... done
Creating flowforge-backend  ... done
Creating flowforge-frontend ... done
Creating flowforge-nginx    ... done
```

### 3. Verify Running Services

```bash
./deploy.sh status    # Linux/macOS
deploy.bat status     # Windows
```

**Output:**
```
NAME                     COMMAND                  SERVICE      STATUS
flowforge-db             docker-entrypoint.s...   db           Up 2 minutes
flowforge-backend        uvicorn main:app --...   backend      Up 2 minutes
flowforge-frontend       serve -s dist -l 3...    frontend     Up 2 minutes
flowforge-nginx          nginx -g daemon off;     nginx        Up 2 minutes
```

### 4. Access Application

- **Frontend:** http://localhost
- **API:** http://localhost/api
- **Database:** `localhost:5432` (for direct connections)

---

## Deployment Commands

### Essential Commands

| Command | Purpose |
|---------|---------|
| `./deploy.sh up` | Start all services in background |
| `./deploy.sh down` | Stop all services |
| `./deploy.sh restart` | Restart all services |
| `./deploy.sh logs [service]` | View logs (optional service name) |
| `./deploy.sh status` | Show container status |

### Advanced Commands

| Command | Purpose |
|---------|---------|
| `./deploy.sh build` | Rebuild Docker images |
| `./deploy.sh rebuild` | Full clean rebuild |
| `./deploy.sh clean` | Remove containers and volumes |
| `./deploy.sh shell-backend` | SSH into backend |
| `./deploy.sh shell-db` | Connect to database |

### Examples

```bash
# View all logs
./deploy.sh logs

# View backend logs only
./deploy.sh logs backend

# View last 100 lines and follow
docker-compose logs -f --tail 100 backend

# Follow frontend logs
./deploy.sh logs frontend

# Get into backend container for debugging
./deploy.sh shell-backend

# Connect directly to database
./deploy.sh shell-db
```

---

## Service Details

### 1. PostgreSQL Database

- **Image:** postgres:15-alpine
- **Container Name:** flowforge-db
- **Port:** 5432 (internal), customizable via `DB_PORT` env
- **Default User:** `flowforge`
- **Default Password:** Set via `DB_PASSWORD` env
- **Default Database:** `flowforge_db`
- **Volume:** `db_data` (persistent)
- **Health Check:** PostgreSQL ready check every 10s

**Useful Database Commands:**

```bash
# Connect to database
psql -U flowforge -h localhost -d flowforge_db

# List tables
\dt

# View table structure
\d campaigns

# Exit
\q
```

### 2. FastAPI Backend

- **Image:** python:3.11-slim (custom built)
- **Container Name:** flowforge-backend
- **Port:** 8000
- **Framework:** FastAPI + Uvicorn
- **Health Check:** HTTP GET `/api/health` every 30s
- **Startup Time:** ~40s

**Environment Variables:**
```env
DATABASE_URL=postgresql://...
DEBUG=false
SECRET_KEY=your-key
GMAIL_CLIENT_ID=...
OPENAI_API_KEY=...
```

**Health Check:**
```bash
curl http://localhost:8000/api/health
```

### 3. React Frontend

- **Image:** node:18-alpine (multi-stage build)
- **Container Name:** flowforge-frontend
- **Port:** 3000
- **Framework:** React 18 + Vite + Tailwind CSS
- **Health Check:** HTTP GET / every 30s
- **Build:** Multi-stage (build → production)

**Frontend Endpoints:**
- `/` - Main application
- `/api/*` - Proxied to backend

### 4. Nginx Reverse Proxy

- **Image:** nginx:alpine
- **Container Name:** flowforge-nginx
- **Ports:** 80 (HTTP), 443 (HTTPS)
- **Health Check:** `/health` endpoint every 30s

**Routes:**
- `/` → Frontend (port 3000)
- `/api/*` → Backend (port 8000)

**Features:**
- Rate limiting (30 req/s general, 10 req/s API)
- Gzip compression
- Security headers
- Cache control
- SSL/TLS ready

---

## Volume Management

### Current Volumes

```bash
# List all volumes
docker volume ls

# Inspect database volume
docker volume inspect enterprise-ai-agent_db_data

# Backup database
docker run --rm -v enterprise-ai-agent_db_data:/data -v $(pwd):/backup \
  postgres:15-alpine tar czf /backup/db_backup.tar.gz /data
```

### Persistent Data

The following data persists across container restarts:
- **Database:** `db_data` volume
- **Nginx Cache:** `nginx_cache` volume

---

## Production Deployment

### Security Checklist

- [ ] Change all default passwords in `.env`
- [ ] Set `DEBUG=false` in production
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure valid SSL certificates
- [ ] Set up proper CORS origins
- [ ] Enable HTTPS in nginx.conf
- [ ] Use environment-specific .env files
- [ ] Enable Docker secrets management
- [ ] Set resource limits in docker-compose.yml

### Resource Limits

Edit `docker-compose.yml` to add limits:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### Enable HTTPS

1. Obtain SSL certificate:
```bash
# Using Let's Encrypt with Certbot
certbot certonly --standalone -d your_domain.com
```

2. Update `.env`:
```env
HTTPS_PORT=443
```

3. Mount certificates in `docker-compose.yml`:
```yaml
volumes:
  - /etc/letsencrypt/live/your_domain.com:/etc/nginx/certs:ro
```

4. Uncomment HTTPS section in `nginx/nginx.conf`

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs backend

# Rebuild image
docker-compose build --no-cache backend

# Force recreate
docker-compose up -d --force-recreate backend
```

### Database Connection Errors

```bash
# Check database health
docker-compose exec db pg_isready -U flowforge

# View database logs
docker-compose logs db

# Reset database
docker-compose down -v
docker-compose up db

# Wait for database startup (30-40s)
```

### Memory Issues

```bash
# Check Docker resource usage
docker stats

# Reduce memory usage
# Edit docker-compose.yml and set resource limits

# Clean up unused containers/images
docker system prune -a
```

### Port Already in Use

If port 80 or 3000 is already in use:

```bash
# Change in .env
HTTP_PORT=8080

# Or kill existing process
# Linux/macOS
lsof -i :80
kill -9 <PID>

# Windows
netstat -ano | findstr :80
taskkill /PID <PID> /F
```

### Slow Performance

```bash
# Check CPU/Memory usage
docker stats

# Check disk space
df -h

# Review logs for errors
docker-compose logs --tail 100

# Clear Docker cache
docker system prune
```

---

## Backup & Recovery

### Backup Database

```bash
# Full backup
docker-compose exec db pg_dump -U flowforge flowforge_db > backup.sql

# Compressed backup
docker-compose exec db pg_dump -U flowforge flowforge_db | gzip > backup.sql.gz
```

### Restore Database

```bash
# From SQL file
docker-compose exec -T db psql -U flowforge flowforge_db < backup.sql

# From compressed file
gunzip -c backup.sql.gz | docker-compose exec -T db psql -U flowforge flowforge_db
```

---

## Monitoring

### View Real-time Metrics

```bash
# CPU, Memory, Network
docker stats

# With specific service
docker stats flowforge-backend
```

### Health Check Status

```bash
# Check all health statuses
docker-compose ps

# Detailed health check info
docker inspect flowforge-backend --format='{{json .State.Health}}' | jq
```

### Application Logs

```bash
# Real-time logs from all services
docker-compose logs -f

# Logs from specific service with timestamps
docker-compose logs -f --timestamps backend

# Last N lines
docker-compose logs --tail 50 backend
```

---

## Updating Services

### Update Application Code

```bash
# 1. Pull latest changes
git pull origin main

# 2. Rebuild images
./deploy.sh build

# 3. Restart services
./deploy.sh restart
```

### Update Docker Images

```bash
# Pull latest base images
docker-compose pull

# Rebuild with latest bases
./deploy.sh rebuild
```

---

## Clean Up & Restart

### Soft Restart (keeps data)

```bash
./deploy.sh restart
```

### Full Reset (removes containers)

```bash
./deploy.sh down
./deploy.sh up
```

### Clean Rebuild (removes everything)

```bash
./deploy.sh clean
./deploy.sh rebuild
```

---

## Advanced Configuration

### Custom Environment per Stage

Create environment files:
- `.env.production`
- `.env.staging`
- `.env.development`

Use specific file:
```bash
docker-compose --env-file .env.production up -d
```

### Multiple Backend Replicas

In `docker-compose.yml`:
```yaml
services:
  backend:
    deploy:
      replicas: 3
```

Then use load balancing in nginx.

---

## Support & Documentation

- **Docker Documentation:** https://docs.docker.com/
- **Docker Compose Docs:** https://docs.docker.com/compose/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/
- **PostgreSQL Docs:** https://www.postgresql.org/docs/

---

## License

FlowForge AI © 2024. All rights reserved.
