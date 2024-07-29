import streamlit as st
from pathlib import Path
from src.tb_projects import Projects
from src.db_conn import DBEngine

st.set_page_config(
    page_title="Data Science App",
    page_icon=":🌐:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css(Path("style/style.css"))

# --------- Header Section ------------------
with st.container():
    st.title("Projects Management System")
    st.write("Projects Management System is built on Python and PostgresSQL hosted on Supabase.")
    projects_table = Projects()
    pro = projects_table.select_all()
    st.write(pro)


# -------------- Insert Project --------------
with st.container():
    st.write("---")
    st.header("Insert Project")
    # Attention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
    contact_form = """
    <form action="https://formsubmit.co/audrbar@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Project name" required>
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
