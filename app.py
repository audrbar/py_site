import requests
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(st.session_state['page_config'])

# ------------- Page Begins -----------------------
st.title("Data Science Projects Demo Website")
st.header("Data Science Projects Demo Website")
st.subheader("Data Science Projects Demo Website")
st.write("###### The web page explores the *data science* **projects to the _clients_** and other developers.")

data = pd.DataFrame(np.random.randn(20, 5), columns=["a", "b", "c", "d", "e"])
st.write(data)

st.bar_chart(data)
