start-services:
	docker-compose up -d

get-data-marvel-api:
	docker-compose exec python bash -c "python marvel_api.py"

mysql-query-cli:
	docker exec -it mysql bash