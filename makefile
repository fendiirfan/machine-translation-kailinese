APP_NAME=my_app

build:
	docker-compose build

up:
	docker-compose up -d

restart:
	docker-compose restart

stop:
	docker-compose stop

clean:
	docker-compose down --rmi all -v --remove-orphans

rebuild: stop clean build up

.PHONY: build up restart stop clean rebuild
