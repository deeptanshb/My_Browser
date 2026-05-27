.PHONY: build up down logs shell status health restart pull-model clean

build:
	docker compose build

up:
	docker compose up -d
	@echo ""
	@echo "  Browser running at: http://localhost:6080/vnc.html"
	@echo ""

up-fg:
	docker compose up

down:
	docker compose down

logs:
	docker compose logs -f mybrowser

shell:
	docker exec -it mybrowser bash

status:
	docker exec mybrowser supervisorctl status

health:
	docker exec mybrowser bash /app/docker/healthcheck.sh

restart:
	docker compose restart mybrowser

pull-model:
	@read -p "Model name (e.g. mistral, llama3.2): " model; \
	docker exec -it ollama ollama pull $$model

clean:
	docker compose down -v
	docker image rm browser-mybrowser 2>/dev/null || true
	docker system prune -f
