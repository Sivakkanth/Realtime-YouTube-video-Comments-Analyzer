# Stage 1: build
FROM node:22-alpine AS builder

# Install build tools (needed for some npm packages like sharp)
RUN apk add --no-cache make gcc g++ python3

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install all dependencies
RUN npm install

# Copy the rest of the app
COPY . .

# Build the Next.js app (creates .next folder)
RUN npm run build

# Stage 2: production
FROM node:22-alpine

WORKDIR /app

# Copy built app from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/public ./public

# Install only production dependencies
RUN npm install --production

# Ensure Next.js listens on 0.0.0.0 (needed for Docker/Kubernetes)
ENV HOST=0.0.0.0
ENV PORT=3000

# Expose container port
EXPOSE 3000

# Start the app
CMD ["npm", "start"]