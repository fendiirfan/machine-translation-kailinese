import streamlit as st
from src.send_request import translate_send_request
from src.send_request import contribute_send_request
import  streamlit_toggle as tog




lang_src = 'Indonesian'
lang_dist = 'Kailinese'

flag = 0



def callback():
    st.session_state.button_clicked = True

def translate_page():

    global lang_src
    global lang_dist
    global flag
    translated_result = ''

    st.markdown(
        """
        <h1 style='text-align: center; font-size: 30px;'>Welcome to our AI Translation Platform</h1>
        """,
        unsafe_allow_html=True
    )

    indonesian, kailinese = st.columns(2)

    with indonesian:
        user_input = st.text_area(lang_src, height=140)
    
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
    
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False
    
    
    if (st.button('Translate', on_click=callback, type='primary') or st.session_state.button_clicked):
        with st.spinner('Translating...'):
            translated_result = translate_send_request(user_input,lang_src)
            with kailinese:
                st.text_area(lang_dist, value=translated_result, height=140)
    
    
    
        switch = tog.st_toggle_switch(label="Want to improve the translation results above?", 
                            key="Key1", 
                            default_value=False, 
                            label_after = False, 
                            inactive_color = '#D3D3D3', 
                            active_color="#11567f", 
                            track_color="#29B5E8"
                            )
        if switch:
            with st.form("form"):
                correctness_translation = st.text_area('Input the correct translation', height=140)
                if st.form_submit_button("Submit Contribute"):
                    if (translated_result=='' 
                    or 'Limit the word count to' in translated_result
                    or correctness_translation==''):
                        st.warning('You have not translated anything in the above section', icon="⚠️")
                    else:
                        with st.spinner('Sending to Database...'):
                            st.success(contribute_send_request(user_input, correctness_translation), icon="✅")
                            st.write('Thanks for being a part of this community')
        
