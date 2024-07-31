import streamlit as st
from pathlib import Path
from src.db_conn import DBEngine
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


def header_section():
    with st.container():
        st.title("Projects Management System")
        st.write("Application is built with *Python*, hosted on *Streamlit Community Cloud*\
                and it's data are stored in *PostgreSQL*, hosted on _Supabase_.")


def main():
    local_css(Path("style/style.css"))
    connection = DBEngine()
    persons_table = Persons(connection.connection)
    projects_table = Projects(connection.connection)
    tasks_table = Tasks(connection.connection)
    person_task_table = PersonTask(connection.connection)
    projects = projects_table.select_projects_managers()
    tasks = tasks_table.select_tasks_assignees()
    persons = persons_table.select_all()
    assignees_tasks = persons_table.select_assignees_tasks()
    select_managers_projects = persons_table.select_managers_projects()
    person_task = person_task_table.select_all()

    header_section()

    with st.container():
        st.write("---")
        st.header("Overview Projects")
        st.write("The section explores the content present on the system:  *projects*, **tasks**, _managers_, \
                **assignees**.")
        tab1, tab2, tab3, tab4 = st.tabs(["projects", "tasks", "managers", "assignees"])
        tab1.write(projects)
        tab2.write(tasks)
        tab3.write(select_managers_projects)
        tab4.write(assignees_tasks)

    # -------------- Insert Project --------------
    with st.container():
        st.write("---")
        st.header("Edit Projects")
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


if __name__ == "__main__":
    main()
