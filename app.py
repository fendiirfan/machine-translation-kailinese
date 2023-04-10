import streamlit as st
from utils.translator import Translator

user_input = st.text_input('Input indonesian sentence')
option = st.selectbox(
    'How would you language translate from?',
    ('Indonesian', 'Kailinese'))
button = st.button('Send')

if button==True: # submit text input
    with st.spinner('Translating...'):
      st.markdown("ChatBot Response : \n")
      obj = Translator(user_input)
      st.write(obj.preprocessing())
      st.write(obj.translate())