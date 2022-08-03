# production environment
FROM nginx:alpine
# Passando o pacote de produção para o Nginx
COPY ./container-front/build /usr/share/nginx/html
# Apagando e passando o novo arquivo de configuração
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx/nginx.conf /etc/nginx/conf.d
# Passando a porta
EXPOSE 443
EXPOSE 80
# Comando de inicialização do front
CMD ["nginx","-g","daemon off;"]