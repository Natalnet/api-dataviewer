#Tag indica a versão dos códigos. Vai ser definida em .env
build:
	docker build -t api-lop ./container-api-lop/
	docker build -t update-db-lop ./container-update-db-lop/
	docker build -t api-users ./container-api-users/
	docker build -t nginx-container ./container-nginx/
login:
	docker login
tag: login
	docker tag api-lop dataviewer/api-lop:$(TAG)
	docker tag api-users dataviewer/api-users:$(TAG)
	docker tag update-db-lop dataviewer/update-db-lop:$(TAG)
	docker tag nginx-container dataviewer/nginx-container:$(TAG)
push: tag
	docker push dataviewer/api-lop:$(TAG)
	docker push dataviewer/api-users:$(TAG)
	docker push dataviewer/update-db-lop:$(TAG)
	docker push dataviewer/nginx-container:$(TAG)

#No console usar a seguinte sequência de comandos para subir a img para o docker hub
#make
#make push
