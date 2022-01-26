FROM node:14

WORKDIR /usr/apinode

ENV PATH /usr/apinode/node_modules/.bin:$PATH

COPY ./package.json .

RUN yarn

COPY . .

EXPOSE 3333

CMD ["yarn", "dev"]