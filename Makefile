dev:
	python main.py

docker-compose-up:
	docker compose --env-file .env up -d

docker-compose-down:
	docker compose down