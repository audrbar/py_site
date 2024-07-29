import streamlit as st
from pathlib import Path
from src.tb_persons import Persons
from src.tb_projects import Projects
from src.tb_tasks import Tasks
from src.tb_persontask import PersonTask


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

persons_table = Persons()
projects_table = Projects()
tasks_table = Tasks()
person_task_table = PersonTask()
projects = projects_table.select_projects_managers()
tasks = tasks_table.select_tasks_assignees()
persons = persons_table.select_all()
person_task = person_task_table.select_all()

# --------- Header Section ------------------
with st.container():
    st.title("Projects Management System")
    st.write("Application is built with *Python*, hosted on *Streamlit Community Cloud*\
            and it's data are stored in *PostgreSQL*, hosted on _Supabase_.")

with st.container():
    st.write("---")
    st.write("The section explores the content:  *projects*, **tasks**, _managers_, **assignees**.")
    tab1, tab2, tab3, tab4 = st.tabs(["projects", "tasks", "managers", "assignees"])
    tab1.write(projects)
    tab2.write(tasks)
    tab3.write(persons)
    tab4.write(persons)


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
