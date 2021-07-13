# Imagem de Origem
FROM node:alpine as build
# Diretório de trabalho(é onde a aplicação ficará dentro do container).
WORKDIR /app
# Adicionando `/app/node_modules/.bin` para o $PATH
ENV PATH /app/node_modules/.bin:$PATH
# Armazenando as dependências no app
COPY ./container-front/package.json /app/package.json
# Pegando o lock para reconhecer o comando yarn
COPY ./container-front/yarn.lock /app/yarn.lock
# Instalando dependências da aplicação e armazenando em cache.
RUN yarn
RUN yarn global add react-scripts
# Copiando todos os outros arquivos
COPY ./container-front .
# Criando o pacote de produção
RUN yarn build

# production environment
FROM nginx:alpine
# Passando o pacote de produção para o Nginx
COPY --from=build /app/build /usr/share/nginx/html
# Apagando e passando o novo arquivo de configuração
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx/nginx.conf /etc/nginx/conf.d
# Passando a porta
EXPOSE 443
EXPOSE 80
# Comando de inicialização do front
CMD ["nginx","-g","daemon off;"]
