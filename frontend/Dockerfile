FROM node:22-slim
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
EXPOSE 19006
CMD ["npx", "expo", "start", "--web", "--no-interactive"]
