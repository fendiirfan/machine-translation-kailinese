import requests
import time
import subprocess

def check_api_status():
    try:
        user_input = ''

        response1 = requests.post(f"http://localhost:8186/translate_indonesian?user_input={user_input}", timeout=50)
        response2 = requests.post(f"http://localhost:8186/translate_kailinese?user_input={user_input}", timeout=50)
	if response1.status_code == 200 and response2.status_code == 200:
            print('API is up and running.')
        else:
            print(f'API is down with status code {response.status_code}.')
            restart_api()
    except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
        print('API is down.')
        restart_api()

def restart_api():
    print('Restarting API...')
    
    print(subprocess.run('sudo pkill -9 uvicorn', shell=True))
    print(subprocess.run('sudo pkill -9 uvicorn', shell=True))
    print(subprocess.run('sudo pkill -9 uvicorn', shell=True))
    
    time.sleep(10)

    print(subprocess.run('sudo nohup uvicorn main:app --port 8186 --reload &', shell=True))
    time.sleep(10)
    

check_api_status()
