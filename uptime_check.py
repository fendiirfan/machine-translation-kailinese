import requests
import time
import subprocess
import streamlit as st

def check_api_status():
    try:
        user_input = ''
        URL_API = st.secrets['URL_API']
        lang_src = 'Indonesian'

        response = requests.post(f"{URL_API}/translate?user_input={user_input}&lang_src={lang_src}", timeout=60)
        if response.status_code == 200:
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
