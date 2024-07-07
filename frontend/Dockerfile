FROM node:22-alpine

WORKDIR /codelab-frontend
COPY package* .
RUN npm install
COPY . .

CMD ["/usr/local/bin/npm", "run", "build"]
