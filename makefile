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
	sudo nohup sudo streamlit run app.py --server.port 8501 &
	sudo nohup uvicorn main:app --port 8186 --reload &
start_be:
	sudo nohup uvicorn main:app --port 8186 --reload &
start_fe:
	sudo nohup sudo streamlit run app.py --server.port 8501 &
stop:
	sudo pkill -f "streamlit run app.py --server.port 8501"
	sudo kill -9 $(sudo lsof -t -i:8186)

restart: stop start

make gitpush:
	sudo mv /home/fendiirfan/machine-trainslation-kaili/model /home/fendiirfan
	sudo git add .
	sudo git commit -m "updating"
	sudo git push
	sudo mv /home/fendiirfan/model /home/fendiirfan/machine-trainslation-kaili
