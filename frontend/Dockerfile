# =============================================================================
# Apex AI Marketing - Frontend Dockerfile
# =============================================================================
# Multi-stage build: Node.js builds the React SPA, nginx serves it.
#
# Build:  docker build -t apex-frontend ./frontend
# Run:    docker run -p 8102:80 apex-frontend
# =============================================================================

# ── Stage 1: Build the React application ─────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first for better layer caching
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci --no-audit --no-fund 2>/dev/null || npm install --no-audit --no-fund

# Copy source code
COPY . .

# Build the production bundle
RUN npm run build

# ── Stage 2: Serve with nginx ────────────────────────────────────────────
FROM nginx:1.27-alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 (mapped to 8102 in docker-compose)
EXPOSE 80

# nginx runs in the foreground
CMD ["nginx", "-g", "daemon off;"]
