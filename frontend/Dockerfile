FROM node:alpine

WORKDIR /opt/app

# Copy dependency files first
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy all source files
COPY . .

# Build the application
RUN npm run build

EXPOSE 3000

# Run the server
ENTRYPOINT ["npx", "http-server", "-p", "3000", "./dist"]
