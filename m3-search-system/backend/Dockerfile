FROM node:alpine

WORKDIR /app

COPY package.json ./

ENV PORT 3001

RUN npm install --silent

RUN mkdir node_modules/.cache && chmod -R 777 node_modules/.cache

COPY . ./

EXPOSE 3001

CMD ["npm", "start"]
