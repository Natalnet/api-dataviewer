#Em /home/admin executar
make_dir:
	mkdir api-dataviewer
get_files: make_dir
	curl -O https://github.com/Natalnet/api-dataviewer/blob/main/scripts/compose-prodution/docker-compose.yml
	curl -O https://github.com/Natalnet/api-dataviewer/blob/main/scripts/db/create_database_dataviewer_lop.sql
	curl -O https://github.com/Natalnet/api-dataviewer/blob/main/scripts/db/create_database_dataviewer_users.sql
up_aplication: get_files
	docker-compose up		
#No console usar a seguinte sequência de comandos para subir a img para o docker hub
#make
#make up_aplication
