import streamlit as st
from utils.translator import Predict

user_input = st.text_input('Input sentence')
option = st.selectbox(
    'How would you language translate from?',
    ('Indonesian', 'Kailinese'))
button = st.button('Tranlsate')

if button==True: # submit text input
    with st.spinner('Translating...'):
      st.markdown("Translate Result : \n")
      obj = Predict(user_input)
    #   st.write(obj.preprocessing())
      st.write(obj.translate())