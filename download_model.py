import gdown
import streamlit as st

url = st.secrets["folder_gdown_model"]
gdown.download_folder(url, quiet=True)
print('---- DONE ----')
