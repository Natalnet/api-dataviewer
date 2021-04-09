FROM nginx:alpine

RUN rm /etc/nginx/conf.d/*

COPY ./container-nginx/default.conf /etc/nginx/conf.d/

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;" ]
