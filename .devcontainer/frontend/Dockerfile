FROM node:20-slim

# Install development tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    ca-certificates \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /app

# Install global tools
RUN npm install -g @angular/cli@19

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Default command
CMD ["npm", "start"]

