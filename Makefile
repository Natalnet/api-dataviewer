#Tag indica a versão dos códigos. Vai ser definida em .env
login:
	docker login
tag: login
	docker tag api-dataviewer_container-api-lop dataviewer/api-dataviewer:$(TAG)-api-lop
	docker tag api-dataviewer_api-users-container dataviewer/api-dataviewer:$(TAG)-api-users
	docker tag api-dataviewer_update-db-lop-container dataviewer/api-dataviewer:$(TAG)-update-db-lop
	docker tag api-dataviewer_nginx-container dataviewer/api-dataviewer:$(TAG)-nginx		
	docker tag api-dataviewer_certbot dataviewer/api-dataviewer:$(TAG)-certbot			
	docker tag api-dataviewer_db-users-container dataviewer/api-dataviewer:$(TAG)-db-users
	docker tag api-dataviewer_db-lop-container dataviewer/api-dataviewer:$(TAG)-db-lop
push: tag
	docker push dataviewer/api-dataviewer:$(TAG)-api-lop
	docker push dataviewer/api-dataviewer:$(TAG)-api-users
	docker push dataviewer/api-dataviewer:$(TAG)-update-db-lop
	docker push dataviewer/api-dataviewer:$(TAG)-nginx
	docker push dataviewer/api-dataviewer:$(TAG)-certbot	
	docker push dataviewer/api-dataviewer:$(TAG)-db-users
	docker push dataviewer/api-dataviewer:$(TAG)-db-lop

#No console usar a seguinte sequência de comandos para subir a img para o docker hub
#make
#make push
