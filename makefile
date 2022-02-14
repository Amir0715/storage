start:
	docker-compose --env-file .env.prod up -d
	docker-compose exec django pipenv run python manage.py makemigrations
	docker-compose exec django pipenv run python manage.py migrate
	docker-compose exec django pipenv run python manage.py collectstatic --noinput
	docker-compose exec django pipenv run python manage.py setup_test_data
stop:
	docker-compose down
build:
	docker-compose build
restart:
	docker-compose down
	docker-compose up -d
	docker-compose exec django pipenv run python manage.py makemigrations
	docker-compose exec django pipenv run python manage.py migrate
	docker-compose exec django pipenv run python manage.py collectstatic --noinput
	docker-compose exec django pipenv run python manage.py setup_test_data
admin:
	docker-compose exec django pipenv run python manage.py createsuperuser