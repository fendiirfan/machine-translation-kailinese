import streamlit as st
from templates.contribute_page import contribute_page
from templates.translate_page import translate_page

st.set_page_config(page_title='Kaili Dev',
    page_icon=f'{st.secrets["base_dir"]}images/favicon.ico')    

hide_st = """
<style>
footer {visibility:hidden;}
ul[role="option"]:last-child,
ul[role="option"]:nth-last-child(2),
ul[role="option"]:nth-last-child(3),
ul[role="option"]:nth-last-child(4) {
    display: none;
}
"""
st.markdown(hide_st,unsafe_allow_html=True)

# Create sidebar menu
menu = ["Translate", "Contribute"]
choice = st.sidebar.selectbox("Select a page", menu)

if choice == "Translate":
    translate_page()
elif choice == "Contribute":
    contribute_page()



