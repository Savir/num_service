makemigrations:
	docker-compose exec backend python manage.py makemigrations squares_diff pythagorean_triplet

migrate:
	docker-compose exec backend python manage.py migrate

un-migrate:
	docker-compose exec backend python manage.py migrate squares_diff zero
	docker-compose exec backend python manage.py migrate pythagorean_triplet zero

run:
	docker-compose exec backend python manage.py runserver 0.0.0.0:8000

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

logs:
	docker-compose logs -f backend

