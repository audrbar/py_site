import requests
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# dir_path = os.path.dirname(os.path.realpath(__file__))
# Set  Page Configuration
# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
page_config = st.set_page_config(
    page_title="Data Science App",
    page_icon=":🌐:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)
st.session_state['page_config'] = page_config

# ------ Hide Streamlit elements ------
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
# st.markdown(hide_st_style, unsafe_allow_html=True)

# ------- Use local CSS ---------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css(Path("style/style.css"))

# ------------- Page Begins -----------------------
st.title("Data Science Projects Demo Website")
st.header("Data Science Projects Demo Website")
st.subheader("Data Science Projects Demo Website")
st.write("###### The web page explores the *data science* **projects to the _clients_** and other developers.")

data = pd.DataFrame(np.random.randn(20, 5), columns=["a", "b", "c", "d", "e"])
st.write(data)

st.bar_chart(data)
