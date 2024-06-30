import requests
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from pathlib import Path


# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
page_config = st.set_page_config(
    page_title="Data Science App",
    page_icon=":🌐:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)
st.session_state['page_config'] = page_config

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
# st.markdown(hide_st_style, unsafe_allow_html=True)

# Use local CSS
# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# local_css("/mount/src/py_site/style/style.css")
# local_css(Path("style/style.css"))

# ------------- Page Begins -----------------------
st.title("Data Science Projects Demo Website")
st.header("Data Science Projects Demo Website")
st.subheader("Data Science Projects Demo Website")
st.write("###### The web page explores the *data science* **projects to the _clients_** and other developers.")
user_input = st.text_input("Your Favorite Movie?", "Type in...")
if user_input:
    st.write(f"Your favorite movie is {user_input}.")
is_clicked = st.button("Like")
if is_clicked:
    st.balloons()


with st.sidebar:
    selected = option_menu(
                menu_title="Main Meniu",  # required
                options=["Home", "About", "Mortgage Calc", "Data Explorer"],  # required
                icons=["house", "book", "book", "envelope"],  # # https://icons.getbootstrap.com/
                menu_icon="cast",  # optional
                default_index=0,  # optional
                # orientation="horizontal",
            )

    if selected == "Home":
        st.page_link("pages/1_home.py")
    if selected == "About":
        st.page_link("pages/2_about.py")
    if selected == "Mortgage Calc":
        st.page_link("pages/3_mortgage_calc.py")
    if selected == "Data Explorer":
        st.page_link("pages/4_data_explorer.py")

st.sidebar.radio("Choose your answer:", options=["yes", "no"])

data = pd.DataFrame(np.random.randn(20, 5), columns=["a", "b", "c", "d", "e"])
st.write(data)

st.bar_chart(data)
