# Clean Dockerfile for CalloutRacing Frontend
FROM node:18-alpine

# Set work directory
WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy frontend source
COPY frontend/ .

# Build the application
RUN npm run build

# Install serve for production
RUN npm install -g serve

# Remove dev dependencies
RUN npm prune --production

# Expose port
EXPOSE 3000

# Start the application
CMD ["serve", "-s", "dist", "-l", "3000"] 