FROM node:22-alpine AS builder

ARG ENV_FILE=.env
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Copy environment file if it exists
COPY ${ENV_FILE} .env* ./

RUN npm run build

FROM node:22-alpine

WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist /app/dist

EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
