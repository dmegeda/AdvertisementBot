FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

RUN addgroup -g 1001 -S nodejs
RUN adduser -S botuser -u 1001

RUN chown -R botuser:nodejs /app
USER botuser

EXPOSE 3000

CMD ["node", "index.js"]