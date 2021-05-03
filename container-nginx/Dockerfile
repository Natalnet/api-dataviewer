FROM nginx:alpine

#Config Nginx
RUN rm /etc/nginx/conf.d/*

COPY ./container-nginx/default.conf /etc/nginx/conf.d/

EXPOSE 443


#Config Certbot
RUN apk add python3 python3-dev py3-pip build-base libressl-dev 

musl-dev libffi-dev

RUN pip3 install pip --upgrade

RUN pip3 install certbot-nginx

RUN mkdir /etc/letsencrypt

CMD [ "nginx", "-g", "daemon off;" ]
