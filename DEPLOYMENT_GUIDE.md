# Agent Service - Deployment Guide

## Overview

This guide covers deploying the Agent service locally, via Docker, and on cloud platforms.

## Local Development

### Prerequisites
- Python 3.9+
- pip
- OpenRouter API key

### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   # Create .env file in the root directory
   OPENROUTER_API_KEY=your_api_key_here
   ```

3. **Run the service:**
   ```bash
   python start_service.py
   ```

4. **Access the service:**
   - UI: http://localhost:8501
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Docker Deployment

### Build and Run

1. **Build the Docker image:**
   ```bash
   docker build -t agent-service:latest .
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

3. **Access the service:**
   - UI: http://localhost:8501
   - API: http://localhost:8000

### Docker Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build -d

# Run specific service
docker-compose up -d agent-api
```

## Cloud Deployment

### AWS EC2

1. **Launch EC2 Instance:**
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t3.medium or higher
   - Security groups: Allow ports 80, 443, 8000, 8501

2. **Setup on Instance:**
   ```bash
   # Update system
   sudo apt-get update && sudo apt-get upgrade -y
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   
   # Clone repository
   git clone <your-repo-url>
   cd agent-service
   
   # Create .env file
   echo "OPENROUTER_API_KEY=your_api_key" > .env
   
   # Start services
   docker-compose up -d
   ```

3. **Setup Domain with Route 53:**
   - Create hosted zone for your domain
   - Add A record pointing to EC2 instance public IP
   - Update nginx.conf with your domain

4. **Setup SSL Certificate (Let's Encrypt):**
   ```bash
   sudo apt-get install certbot python3-certbot-nginx -y
   sudo certbot certonly --standalone -d yourdomain.com
   
   # Copy certificates
   sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./ssl/cert.pem
   sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./ssl/key.pem
   sudo chown 1000:1000 ./ssl/*
   
   # Restart services
   docker-compose restart
   ```

### Google Cloud Platform (GCP)

1. **Create Cloud Run service:**
   ```bash
   gcloud run deploy agent-service \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars OPENROUTER_API_KEY=your_api_key \
     --memory 2Gi \
     --timeout 3600 \
     --max-instances 10
   ```

2. **Setup custom domain:**
   - Go to Cloud Run → agent-service → Manage custom domains
   - Add your domain
   - Update DNS records according to instructions

### Heroku

1. **Prepare for deployment:**
   ```bash
   # Create Heroku app
   heroku create your-app-name
   
   # Set environment variables
   heroku config:set OPENROUTER_API_KEY=your_api_key
   
   # Deploy
   git push heroku main
   
   # View logs
   heroku logs --tail
   ```

2. **Add custom domain:**
   ```bash
   heroku domains:add yourdomain.com
   ```

### Azure Container Instances (ACI)

1. **Create container registry:**
   ```bash
   az acr create --resource-group myResourceGroup \
     --name myRegistry --sku Basic
   ```

2. **Build and push image:**
   ```bash
   az acr build --registry myRegistry --image agent-service:latest .
   ```

3. **Deploy container:**
   ```bash
   az container create \
     --resource-group myResourceGroup \
     --name agent-service \
     --image myRegistry.azurecr.io/agent-service:latest \
     --cpu 2 --memory 4 \
     --ports 80 443 8000 8501 \
     --environment-variables OPENROUTER_API_KEY=your_api_key
   ```

## Production Configuration

### Environment Variables
```bash
# Required
OPENROUTER_API_KEY=your_api_key

# Optional
HOST=0.0.0.0           # Default: 0.0.0.0
PORT=8000              # Default: 8000
PYTHONUNBUFFERED=1     # Default: 1 (for Docker)
```

### Performance Tuning

1. **API Server (uvicorn):**
   - Update `api_server.py` with workers for production
   ```python
   uvicorn.run(
       app,
       host=host,
       port=port,
       workers=4,  # Multiple workers for production
       log_level="info"
   )
   ```

2. **Nginx Configuration:**
   - Already configured in nginx.conf with:
     - Rate limiting
     - Connection pooling
     - SSL/TLS optimization

3. **Docker Resources:**
   - Update docker-compose.yml with resource limits:
   ```yaml
   agent-api:
     deploy:
       resources:
         limits:
           cpus: '2'
           memory: 4G
         reservations:
           cpus: '1'
           memory: 2G
   ```

## Monitoring and Logging

### Health Checks
```bash
# API health
curl http://localhost:8000/health

# Full health from container
docker-compose exec agent-api curl http://localhost:8000/health
```

### View Logs
```bash
# Docker Compose logs
docker-compose logs -f agent-api

# Specific lines
docker-compose logs --tail=100 agent-api

# With timestamps
docker-compose logs -f --timestamps agent-api
```

### Monitoring Endpoints
- Health: `/health`
- Metrics: `/info`
- API Docs: `/docs`
- ReDoc: `/redoc`

## Troubleshooting

### API not responding
```bash
# Check if container is running
docker-compose ps

# Check logs
docker-compose logs agent-api

# Restart service
docker-compose restart agent-api
```

### Port already in use
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### SSL certificate issues
```bash
# Verify certificates
openssl s_client -connect localhost:443

# Renew Let's Encrypt certificate
sudo certbot renew --dry-run
```

### Memory issues
```bash
# Check memory usage
docker stats agent-api

# Increase memory in docker-compose.yml
```

## Security Best Practices

1. **API Key Management:**
   - Use environment variables (never commit to git)
   - Rotate keys regularly
   - Use separate keys for different environments

2. **Network Security:**
   - Enable HTTPS/SSL only
   - Use rate limiting (configured in nginx)
   - Set up firewall rules

3. **Container Security:**
   - Run as non-root user (configured in Dockerfile)
   - Use minimal base image (python:3.11-slim)
   - Keep dependencies updated

4. **Monitoring:**
   - Setup log aggregation (ELK stack, CloudWatch, etc.)
   - Monitor API response times
   - Alert on errors and failures

## Backup and Recovery

### Backup Configuration
```bash
# Backup environment
cp .env .env.backup

# Backup application code
git commit -am "backup: $(date)"
git push
```

### Recovery
```bash
# Restore from backup
cp .env.backup .env

# Restart services
docker-compose restart
```

## Support and Resources

- **API Documentation:** http://localhost:8000/docs
- **OpenRouter Docs:** https://openrouter.ai/docs
- **OpenAI Agents:** https://openai.github.io/openai-agents-python/
- **Docker Docs:** https://docs.docker.com/
- **Streamlit Docs:** https://docs.streamlit.io/

## License

This project is licensed under the MIT License.

