from src.translator import Predict
import streamlit as st
import requests
from transformers import AutoModelForSeq2SeqLM

user_input = 'yaku ante bereiku naturu ri jimbaran ane hau ri bali.'
lang_src = 'Kailinese'

URL_API = st.secrets["URL_API"]
    
response = requests.post(f"{URL_API}/translate?user_input={user_input}&lang_src={lang_src}")

print(response)

# model = AutoModelForSeq2SeqLM.from_pretrained('/home/fendiirfan/machine-trainslation-kaili/model/kaili_ke_indo')
# print(model)