import requests
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import sys


# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Data Science App", page_icon=":🌐:", layout="wide")

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# local_css("/mount/src/py_site/style/style.css")
# local_css("Users/audrius/Documents/VCSPython/py_site/style/style.css")

selected = option_menu(
            menu_title=None,  # required
            options=["Home", "Projects", "Contact"],  # required
            icons=["house", "book", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            # styles={
            #     "container": {"padding": "0!important", "background-color": "#fafafa"},
            #     "icon": {"color": "orange", "font-size": "25px"},
            #     "nav-link": {
            #         "font-size": "25px",
            #         "text-align": "left",
            #         "margin": "0px",
            #         "--hover-color": "#eee",
            #     },
            #     "nav-link-selected": {"background-color": "green"},
            # },
        )

if selected == "Home":
    st.title(f"You have selected {selected}")
if selected == "Projects":
    st.title(f"You have selected {selected}")
if selected == "Contact":
    st.title(f"You have selected {selected}")


# ------------- Page Begins -----------------------
st.title("Data Science Projects Demo Website")
st.header("Data Science Projects Demo Website")
st.subheader("Data Science Projects Demo Website")
st.write("###### The web page explores the *data science* **projects to the _clients_** and other developers.")
user_input = st.text_input("Your Favorite Movie?", "Type in...")
if user_input:
    st.write(f"Your favorite movie is {user_input}.")

st.sidebar.header("About")
is_clicked = st.button("Like")
sidebar_radio = st.sidebar.radio("Choose your answer:", options=["yes", "no"])

data = pd.DataFrame(np.random.randn(20, 5), columns=["a", "b", "c", "d", "e"])
st.write(data)

st.bar_chart(data)
