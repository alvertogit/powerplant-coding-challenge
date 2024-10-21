run:
	@docker compose up -d

stop:
	@docker compose down

test:
	@docker compose up -d
	@docker compose exec api pytest
	@docker compose down
