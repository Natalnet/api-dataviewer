#Tag indica a versão dos códigos. Vai ser definida em .env
login:
	docker login
tag: login
	docker tag api-lop dataviewer/api-dataviewer:$(TAG)-api-lop
	docker tag api-users dataviewer/api-dataviewer:$(TAG)-api-users
	docker tag update-db-lop dataviewer/api-dataviewer:$(TAG)-update-db-lop
	docker tag nginx dataviewer/api-dataviewer:$(TAG)-nginx			
	docker tag db-users dataviewer/api-dataviewer:$(TAG)-db-users
	docker tag db-lop dataviewer/api-dataviewer:$(TAG)-db-lop
push: tag
	docker push dataviewer/api-dataviewer:$(TAG)-api-lop
	docker push dataviewer/api-dataviewer:$(TAG)-api-users
	docker push dataviewer/api-dataviewer:$(TAG)-update-db-lop
	docker push dataviewer/api-dataviewer:$(TAG)-nginx
	docker push dataviewer/api-dataviewer:$(TAG)-db-users
	docker push dataviewer/api-dataviewer:$(TAG)-db-lop

#No console usar a seguinte sequência de comandos para subir a img para o docker hub
#make
#make push
