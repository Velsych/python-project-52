install:
	uv sync

build_uv:
	uv build


package-install:
	uv tool install dist/*.whl


package-reinstall: build
	uv tool install --force dist/*.whl


lint:
	uv run ruff check task_manager


fix:
	uv run ruff check task_manager --fix


build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

migrate:
	uv run manage.py migrate

collectstatic:
	uv run manage.py collectstatic --no-input

start:
	uv run manage.py runserver