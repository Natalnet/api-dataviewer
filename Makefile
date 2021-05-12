#Tag indica a versão dos códigos. Vai ser definida em .env
export_env:
	export TAG
	env | grep TAG
login:
	docker login
tag: export_env login
	docker tag api-lop dataviewer/api-dataviewer:$(TAG)-api-lop
	docker tag api-users dataviewer/api-dataviewer:$(TAG)-api-users
	docker tag update-db-lop dataviewer/api-dataviewer:$(TAG)-update-db-lop
	docker tag nginx dataviewer/api-dataviewer:$(TAG)-nginx			
push: tag
	docker push dataviewer/api-dataviewer:$(TAG)-api-lop
	docker push dataviewer/api-dataviewer:$(TAG)-api-users
	docker push dataviewer/api-dataviewer:$(TAG)-update-db-lop
	docker push dataviewer/api-dataviewer:$(TAG)-nginx

#No console usar a seguinte sequência de comandos para subir a img para o docker hub
#make
#make push
