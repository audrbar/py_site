from PIL import Image
import requests
import json
import streamlit as st
import streamlit-lottie as lto

# ---------Load Assets------------------
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://lottie.host/5b073eca-e11c-4391-8593-b28f39ce0870/q0fz2A3kuN.json")
img_first = Image.open("../../VCSPython/py_site/images/about04.png")

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
            On this page I am creating small Python projects to show possibilities Python gives in manipulating a large sets of data and creating a awesome insights with charts.
            """
        )
        st.write("[Youtube Channel >](https://www.youtube.com/)")
    with right_column:
        lto.st_lottie(lottie_coding, height=300, key="coding") # type: ignore

# ----------- My Projects ---------------------
with st.container():
    st.write("---")
    left_column, right_column = st.columns((2, 1))
    with left_column:
        st.image(img_first, width=350)
    with right_column:
        st.subheader("Projects you will find here")
        st.write(
            """
            The projects are:
            - Data Frame explorer;
            - Mortgage Calculator;
            - Charts.
            """
        )

# ---- CONTACT ----
with st.container():
    st.write("---")
    st.header("Get In Touch With Me!")
    st.write("##")

    # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
    contact_form = """
    <form action="https://formsubmit.co/audrbar@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()
