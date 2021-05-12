#Tag indica a versão dos códigos. Vai ser definida em .env
build:
	docker build -t api-lop ./container-api-lop/
	docker build -t update-db-lop ./container-update-db-lop/
	docker build -t api-users ./container-api-users/
	docker build -t nginx-container ./container-nginx/
login:
	docker login
tag: login
	docker tag api-lop dataviewer/api-dataviewer:$(TAG)
	docker tag api-users dataviewer/api-dataviewer:$(TAG)
	docker tag update-db-lop dataviewer/api-dataviewer:$(TAG)
	docker tag nginx-container dataviewer/api-dataviewer:$(TAG)
push: tag
	docker push dataviewer/api-dataviewer:$(TAG)

#No console usar a seguinte sequência de comandos para subir a img para o docker hub
#make
#make push
