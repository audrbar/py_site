import streamlit as st
import streamlit_lottie as lto
from datetime import datetime
from PIL import Image
import requests
from pathlib import Path


# dir_path = os.path.dirname(os.path.realpath(__file__))
# Set  Page Configuration
# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
# ------ Hide Streamlit elements ------
st.set_page_config(
    page_title="Data Science App",
    page_icon=":globe_with_meridians:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)

hide_st_style = """
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)


# ------- Use local CSS ---------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css(Path("style/style.css"))


# ---------Load Assets------------------
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_coding = load_lottieurl("https://lottie.host/5b073eca-e11c-4391-8593-b28f39ce0870/q0fz2A3kuN.json")
img_first = Image.open(Path("images/about04.png"))


def footer_section() -> None:
    """
    Render Streamlit Page footer section with Streamlit Title and Write Methods
    :return: None
    """
    with st.container():
        st.write("---")
        year = datetime.now().year
        st.write(f"© {year} audrbar. All rights reserved.")


# --------- Header Section ------------------
with st.container():
    st.title("Data Science Projects Demo Website")
    st.subheader("Hi, I am Audrius :wave:")
    st.write("A Data Scientist from Lithuania.")
    st.write("I am passionate about finding ways to use Python libraries to explore the data sets.")

# ----------- What I Do ---------------------
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2, gap="small")
    with left_column:
        st.subheader("What I Do")
        st.write(
            """
            On this page I am creating small Python projects to show possibilities Python gives in manipulating\
             a large sets of data and creating a awesome insights with charts.
            """
        )
        st.write("[Youtube Channel >](https://www.youtube.com/)")
    with right_column:
        lto.st_lottie(lottie_coding, height=300, key="coding")  # type: ignore

# ----------- My Projects ---------------------
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2, gap="small")
    with left_column:
        st.image(img_first, width=250)
    with right_column:
        st.subheader("Projects you will find here")
        st.write("""The projects are:
            - Data Frame explorer;
            - Charting experiments;
            - Mortgage Calculator;
            - Projects Management System.
        """)

# -------------- Contact me --------------
with st.container():
    st.write("---")
    st.header("Get In Touch With Me!")
    # Attention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
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

footer_section()
