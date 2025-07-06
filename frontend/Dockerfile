# Use Node.js 18 Alpine image
FROM node:18-alpine

# Set work directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Install serve to run the built app
RUN npm install -g serve

# Expose port (will be overridden by Railway's PORT environment variable)
EXPOSE $PORT

# Start the application using Railway's PORT environment variable
CMD ["sh", "-c", "npx serve -s dist -l $PORT"] 