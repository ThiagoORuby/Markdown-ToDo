run-dev:
	@uvicorn app:app --reload --port 8000

run:
	@uvicorn main:app --port 8000

migrate:
	@alembic revision --autogenerate -m "$(msg)"

upgrade:
	@alembic upgrade head

downgrade:
	@alembic downgrade -1