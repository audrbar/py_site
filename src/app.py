import requests
import streamlit as st
import pandas as pd
import numpy as np
import sys


# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Data Science App", page_icon=":🌐:", layout="wide")

# Download your emoji
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("/mount/src/py_site/style/style.css")

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
