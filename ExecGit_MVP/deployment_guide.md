# ExecGit Deployment Guide

## Prerequisites
- A DigitalOcean Droplet ($5/mo) or AWS EC2 Instance (t2.micro).
- Docker and Docker Compose installed.
- Domain name pointed to the server IP.

## Step-by-Step Deployment

### 1. Server Setup
SSH into your server:
```bash
ssh root@your_server_ip
```

Install Docker & Compose:
```bash
apt update
apt install docker.io docker-compose -y
```

### 2. Clone Repository
```bash
git clone https://github.com/your-repo/ExecGit.git
cd ExecGit/ExecGit_MVP
```

### 3. Environment Variables
Create a `.env` file:
```bash
touch .env
nano .env
```
Add the following:
```env
SECRET_KEY=your_super_secret_key
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
DATABASE_URL=postgresql://user:password@db:5432/execgit_db
```

### 4. Nginx Configuration
Create `nginx.conf` in the same directory:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://client:80;
    }

    location /api {
        proxy_pass http://api:8000;
        rewrite ^/api/(.*) /$1 break;
    }
}
```

### 5. Launch
Run the containers:
```bash
docker-compose up -d --build
```

### 6. SSL (HTTPS)
Install Certbot and run it (requires Nginx on host or specialized container setup, for simplicity here assume host Nginx or use Nginx Proxy Manager):
```bash
# Simplest way: Use Nginx Proxy Manager container instead of raw Nginx
```

## Monitoring
Check logs:
```bash
docker-compose logs -f
```
