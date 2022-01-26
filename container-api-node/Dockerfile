FROM node:alpine

WORKDIR /usr/apinode

COPY ./package.json .

RUN yarn

COPY . .

EXPOSE 3333

CMD ["yarn", "dev"]