# Use Node.js 18 as base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install ALL dependencies (including dev dependencies for build)
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Install serve to run the built app
RUN npm install -g serve

# Remove dev dependencies to reduce image size
RUN npm prune --production

# Make start script executable
RUN chmod +x start.sh

# Expose port 8000 (Railway will override with $PORT if needed)
EXPOSE 8000

# Start the application using the start script
CMD ["./start.sh"] 