# frontend dockerfile
FROM node:22

WORKDIR /frontend

COPY package*.json ./

RUN npm config set legacy-peer-deps true
RUN npm install --force

COPY . .

ENV PORT=3000

EXPOSE 3000

CMD ["npm", "run", "dev"]
