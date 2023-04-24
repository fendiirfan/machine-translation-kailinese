import streamlit as st
from src.send_request import translate_send_request

lang_src = 'Indonesian'
lang_dist = 'Kailinese'
flag = 0

def translate_page():
    

    global lang_src
    global lang_dist
    global flag

    st.markdown(
        """
        <h1 style='text-align: center; font-size: 30px;'>Welcome to our AI Translation Platform</h1>
        """,
        unsafe_allow_html=True
    )

    indonesian, kailinese = st.columns(2)

    with indonesian:
        user_input = st.text_area(lang_src, height=170)
    
    translation_schema = st.selectbox(
    'Choose a translation schema',
    ['Indonesian ➜ Kailinese','Kailinese ➜ Indonesian'])

    if translation_schema=='Indonesian ➜ Kailinese' and flag==0:
        lang_src = 'Indonesian'
        lang_dist = 'Kailinese'
        flag = 1
        st.experimental_rerun()
    elif translation_schema=='Kailinese ➜ Indonesian' and flag==1:
        lang_src = 'Kailinese'
        lang_dist = 'Indonesian'
        flag = 0
        st.experimental_rerun()
    
    if translation_schema=='Indonesian ➜ Kailinese':
        lang_src = 'Indonesian'
        lang_dist = 'Kailinese'
    elif translation_schema=='Kailinese ➜ Indonesian':
        lang_src = 'Kailinese'
        lang_dist = 'Indonesian'
    
    button = st.button('Translate')
    if button == True:
        with st.spinner('Translating...'):
            indonesian_result = translate_send_request(user_input,lang_src)
            with kailinese:
                st.text_area(lang_dist, value=indonesian_result, height=170)