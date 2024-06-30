import streamlit as st
from streamlit_option_menu import option_menu
from pathlib import Path

st.set_page_config(st.session_state['page_config'])

st.title("About")
st.write("This is the page about different built in Streamlit possibilities.")

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2, gap = "medium")
    with left_column:
        st.link_button("Home", url="/home")
    with right_column:
        is_clicked = st.button("Like")
        if is_clicked:
            st.balloons()

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2, gap = "medium")
    with left_column:
        with st.expander("Click to read more"):
            st.write("Hello, here are more details on this topic that you are interested in.")
    with right_column:
        st.metric(label="Temperature", value="60 Celsius", delta="3 Celsius")

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2, gap = "medium")
    with left_column:
        user_input = st.text_input("Your Favorite Movie?", placeholder = "Type in...")
        if user_input:
            st.write(f"Your favorite movie is {user_input}.")
    with right_column:
        st.metric(label="Pressure", value="256 Hg", delta="-25 Hg")

with st.container():
    st.write("---")
    tab1 , tab2 = st.tabs(["audio" , "video"])
    tab1.write("Relax and listen.")
    tab1.audio("https://www.youtube.com/watch?v=51zjlMhdSTE")
    tab2.write("Awesome video.")
    tab2.video("https://www.youtube.com/watch?v=NTpbbQUBbuo")


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
    st.page_link("pages/1_Home.py")
if selected == "About":
    st.page_link("pages/2_About.py")
if selected == "Mortgage Calc":
    st.page_link("pages/3_Mortgage_Calc.py")
if selected == "Data Explorer":
    st.page_link("pages/4_Data_Explorer.py")

st.write("---")
st.sidebar.radio("Do you like this site?", options=["yes", "no"])
