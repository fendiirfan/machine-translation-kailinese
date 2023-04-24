import requests
import streamlit as st

def translate_send_request(user_input: str, lang_src: str):
    URL_API = st.secrets["URL_API"]
    
    response = requests.post(f"{URL_API}/translate?user_input={user_input}&lang_src={lang_src}")

    if response.status_code == 200:
        result = response.json()
        prediction = result.get("prediction")
        return prediction
    else:
        return f'⚠️ {response.status_code}: {response.text} ⚠️'

def contribute_send_request(indonesian_user_input: str, kailinese_user_input: str):
    URL_API = st.secrets["URL_API"]

    response = requests.post(f"{URL_API}/contribute?indonesian_user_input={indonesian_user_input}&kailinese_user_input={kailinese_user_input}")
    
    if response.status_code == 200:
        response_json = response.json()
        message = response_json["message"]
        return message
    else:
        return f'⚠️ {response.status_code}: {response.text} ⚠️'

