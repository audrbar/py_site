# from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(
    page_title="Data Science App",
    page_icon=":🌐:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)

# ------ Hide Streamlit elements ------
hide_st_style = """
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
            </style>
            """


st.title("Various Streamlit Elements")
st.write("This is the page about different built in Streamlit possibilities.")

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2, gap="medium")
    with left_column:
        st.link_button("Home", url="/")
    with right_column:
        is_clicked = st.button("Like")
        if is_clicked:
            st.balloons()

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2, gap="medium")
    with left_column:
        with st.expander("Click to read more"):
            st.write("Hello, here are more details on this topic that you are interested in.")
    with right_column:
        st.metric(label="Temperature", value="60 Celsius", delta="3 Celsius")

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2, gap="medium")
    with left_column:
        user_input = st.text_input("Your Favorite Movie?", placeholder="Type in...")
        if user_input:
            st.write(f"Your favorite movie is {user_input}.")
    with right_column:
        st.metric(label="Pressure", value="256 Hg", delta="-25 Hg")

with st.container():
    st.write("---")
    st.write("###### The section explores the *tabs* with **audio and video _inserts_**.")
    tab1, tab2 = st.tabs(["audio", "video"])
    tab1.write("Relax and listen.")
    tab1.audio("https://www.youtube.com/watch?v=51zjlMhdSTE")
    tab2.write("Awesome video.")
    tab2.video("https://www.youtube.com/watch?v=NTpbbQUBbuo")

with st.container():
    st.write("---")
    st.write("###### The section explores the *random data frame* **table and _chart_**.")

    data = pd.DataFrame(np.random.randn(20, 5), columns=["a", "b", "c", "d", "e"])
    st.write(data)

    st.bar_chart(data)


st.write("---")
st.sidebar.radio("Do you like this site?", options=["yes", "no"])
