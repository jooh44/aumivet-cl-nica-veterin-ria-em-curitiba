FROM node:14-alpine
ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}
WORKDIR /opt/app
COPY package-new.json ./package.json
RUN npm install --only=production
COPY . .
RUN npm run build
EXPOSE 1337
CMD ["npm", "run", "start"]
