#Em /home/admin/api-dataviewer executar
get_files:
	curl -O https://github.com/Natalnet/api-dataviewer/blob/main/scripts/compose-prodution/docker-compose.yml
	curl -O https://github.com/Natalnet/api-dataviewer/blob/main/scripts/db/create_database_dataviewer_lop.sql
	curl -O https://github.com/Natalnet/api-dataviewer/blob/main/scripts/db/create_database_dataviewer_users.sql
up_aplication: get_files
	docker-compose up		
#No console usar a seguinte sequência de comandos para subir o compose
#make
#make up_aplication
