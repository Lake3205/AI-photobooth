FROM node:alpine
RUN mkdir -p /opt/app/dist
EXPOSE 3000
WORKDIR /opt/app
COPY ./package.json ./package.json
COPY ./package-lock.json .
RUN npm install
COPY . .
RUN npm run build
ENTRYPOINT ["npx", "http-server", "-p", "3000", "./dist"]