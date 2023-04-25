import streamlit as st
from src.send_request import contribute_send_request


def contribute_page():
    st.markdown(
        """
        <h1 style='text-align: center; font-size: 25px;'>Input Indonesian and Kailinese Sentence to Improve our AI</h1>
        """,
        unsafe_allow_html=True
    )

    indonesian, kailinese = st.columns(2)
    with indonesian:
        indonesian_contribute_input = str(st.text_area('Input Indonesian sentence', height=140, key='indonesian_contribute'))
    with kailinese:
        kailinese_contribute_input = str(st.text_area('Input Kailinese sentence', height=140, key='kailinese_contribute'))
    
    button = st.button('Send Contribute')
    if button == True:
        if indonesian_contribute_input=='' or kailinese_contribute_input=='':
            st.warning('Indonesian sentence or Kailinese sentence input can not be empty', icon="⚠️")
        else:
            with st.spinner('Sending to Database...'):
                st.write(contribute_send_request(indonesian_contribute_input, kailinese_contribute_input))
