start-mysql:
	docker-compose up -d

build-python:
	docker build -t env-python .
        
start-python:
	docker run -it --rm  env-python

mysql-query-cli:
	docker exec -it marvel-api_db_1 bash	
