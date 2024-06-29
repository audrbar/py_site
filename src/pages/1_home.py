import requests
import streamlit as st
from streamlit_lottie import st_lottie


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://lottie.host/embed/b1c3df48-f1f4-40aa-972d-e3d8d2625d4e/gNF8nWxT6m.json")

# ---------Header Section------------------
with st.container():
    st.subheader("Hi, I am Audrius :wave:")
    st.write("A Data Scientist from Lithuania.")
    st.write("I am passionate about finding ways to use Python libraries to explore the data sets.")

# -----------What I Do ---------------------
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("What I Do")
        st.write(
            """
            On this page I am creating small Python projects to show possibilities Python gives us in manipulating a large sets of data and creating a awesome insights with charts.
            """
        )
        st.write("[Youtube Channel >](https://www.youtube.com/)")
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")
