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
	docker system prune -a

rebuild: 
	docker-compose up -d --remove-orphans --no-deps --build mt-kaili

.PHONY: build up restart stop clean rebuild

download_model:
	sudo python3 download_model.py

setup_cache:
	sudo python3 setup_cache_indobenchmark.py

install:
	sudo pip3 install -r requirements.txt

setup_init: download_model setup_cache

start:
	nohup sudo streamlit run app.py --server.port 8501 &
