"""Streamlit Page render script"""
import streamlit as st
from Home import footer_section
from src.db_conn import DBEngine
from src.tb_persons import Persons
from src.tb_projects import Projects
from src.tb_tasks import Tasks
from src.tb_persontask import PersonTask

# ------ Hide Streamlit elements ------
hide_st_style = """
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                layout="wide",
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


def header_section() -> None:
    """
    Render Streamlit Page header section with Streamlit Title and Write Methods
    :return: None
    """
    with st.container():
        st.title("Project Management System")
        st.write("Application is built with *Python*, hosted on *Streamlit Community Cloud*\
                and it's data are stored in *PostgreSQL*, hosted on _Supabase_.")


def next_section(section_name: str, section_description) -> None:
    """
    Render Streamlit Page section with Streamlit Header and Write Methods
    :param section_name string
    :param section_description string
    :return: None
    """
    with st.container():
        st.write("---")
        st.header(section_name)
        st.write(section_description)


def make_a_list(df, col_name_1, col_name_2=None) -> list:
    """
    Make a list from DataFrame from one or two columns values
    :param df: pandas.DataFrame - data to remake
    :param col_name_1 pandas.DataFrame column name
    :param col_name_2 pandas.DataFrame column name optional
    :return: list
    """
    if col_name_2 is not None:
        made_list = (df[col_name_1] + ' ' + df[col_name_2]).tolist()
    else:
        made_list = df[col_name_1].tolist()
    return made_list


def find_person_id(df, fullname) -> int:
    """
    Find a Person id from DataFrame by Person full name
    :param df: pandas.DataFrame - data to search from
    :param fullname value to search by
    :return: int
    """
    df = df.reset_index()
    for index, row in df.iterrows():
        if row['firstname'] + ' ' + row['lastname'] == fullname:
            return row['person_id']


def find_project_id(df, project_name) -> int:
    """
    Find a Project id from DataFrame by Project name
    :param df: pandas.DataFrame - data to search from
    :param project_name value to search by
    :return: int
    """
    df = df.reset_index()
    for index, row in df.iterrows():
        if row['project_name'] == project_name:
            return row['project_id']


def main():
    connection = DBEngine()
    persons_table = Persons(connection.connection)
    projects_table = Projects(connection.connection)
    tasks_table = Tasks(connection.connection)
    PersonTask(connection.connection)
    projects = projects_table.get_all_projects()
    persons = persons_table.get_all_persons()
    tasks = tasks_table.get_tasks_assignees()

    header_section()
    # -------------- Overview Projects Section --------------
    next_section("Data Overview", "The section explores the content present \
                on the system:  *projects*, **tasks**, _managers_, **assignees**.")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["projects", "managers", "tasks", "assignees", "persons"])
    tab1.dataframe(projects, hide_index=True)
    tab2.dataframe(persons_table.select_managers_projects(), hide_index=True)
    tab3.dataframe(tasks, hide_index=True)
    tab4.dataframe(persons_table.select_assignees_tasks(), hide_index=True)
    tab5.dataframe(persons, hide_index=True)

    # -------------- Edit Items Section --------------
    with (st.container()):
        st.write("---")
        left_column, right_column = st.columns([1, 3])
        with left_column:
            st.header("Edit Items")
            st.write('Edit different aspects of your projects and choose for that the tab accordingly \
                and check the results write above.')
        with right_column:
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["assign manager", "edit budget", "assign assignee",
                                                    "change status", "set salary"])
            with tab1:
                with st.form('project_manager', clear_on_submit=True):
                    st.write("Assign Project Manager:")
                    select_project = st.selectbox('Select a Project to edit', make_a_list(projects, 'project_name'))
                    select_person = st.selectbox('Assign Manager', make_a_list(persons, 'firstname', 'lastname'))
                    select_person_id = find_person_id(persons, select_person)
                    submit_button = st.form_submit_button(label='Submit')
                    if submit_button:
                        projects_table.update_project_manager(select_project, select_person, select_person_id)
                        st.cache_data.clear()
                    else:
                        st.write('To succeed please select and fill inputs and smash a Submit button.')
            with tab2:
                with st.form('project_budget', clear_on_submit=True):
                    st.write("Edit Project Budget:")
                    select_project = st.selectbox('Select a Project to edit', make_a_list(projects, 'project_name'))
                    project_budget = st.number_input('Provide budget value, $')
                    submit_button = st.form_submit_button(label='Submit')
                    if submit_button:
                        projects_table.update_project_budget(select_project, project_budget)
                        st.cache_data.clear()
                    else:
                        st.write('To succeed please select and fill inputs and smash a Submit button.')

            with tab3:
                with st.form('assign_assignee', clear_on_submit=True):
                    st.write('Assign Task Assignee:')
                    select_task = st.selectbox('Select a task to edit:', make_a_list(tasks, 'task_name'))
                    select_person = st.selectbox('Select a Assignee to assign:', make_a_list(persons,
                                                                                             'firstname', 'lastname'))
                    select_person_id = find_person_id(persons, select_person)
                    submit_button = st.form_submit_button(label='Submit')
                    if submit_button:
                        tasks_table.set_task_assignee(select_task, select_person, select_person_id)
                        st.cache_data.clear()
                    else:
                        st.write('To succeed please select and fill inputs and smash a Submit button.')
            with tab4:
                with st.form('change_status', clear_on_submit=True):
                    st.write('Change Task status:')
                    select_task = st.selectbox('Select a task to edit:', make_a_list(tasks, 'task_name'))
                    select_status = st.selectbox('Select a Task status to set', ['not_started', 'in_progres', 'done'])
                    submit_button = st.form_submit_button(label='Submit')
                    if submit_button:
                        tasks_table.set_task_status(select_task, select_status)
                        st.cache_data.clear()
                    else:
                        st.write('To succeed please select input and smash a Submit button.')
            with tab5:
                with st.form('set_salary', clear_on_submit=True):
                    st.write('Set Persons salary:')
                    select_person = st.selectbox('Select a person to edit:',
                                                 make_a_list(persons, 'firstname', 'lastname'))
                    persons_salary = st.number_input('Provide salary value, $')
                    select_person_id = find_person_id(persons, select_person)
                    submit_button = st.form_submit_button(label='Submit')
                    if submit_button:
                        persons_table.set_persons_salary(select_person, persons_salary, select_person_id)
                        st.cache_data.clear()
                    else:
                        st.write('To succeed please select and fill inputs and smash a Submit button.')

        # -------------- Insert New Item Section --------------
        with st.container():
            st.write("---")
            left_column, right_column = st.columns([2, 1])
            with right_column:
                st.header("Insert New Item")
                st.write('Insert any new item - project, task, person - to the system and provide \
                        the item details accordingly.')
            with left_column:
                tab1, tab2, tab3 = st.tabs(["add project", "add task", "add person"])
                with tab1:
                    with st.form('add project', clear_on_submit=True):
                        st.write("Add New Project:")
                        project_name = st.text_input('Provide project name:')
                        project_aim = st.text_area('Describe project aim:')
                        project_budget = st.number_input('Provide budget value, $:', min_value=0.0,
                                                         max_value=10000000.0,
                                                         step=1.0, value=0.0)
                        selected_person = st.selectbox('Select a manager:',
                                                       make_a_list(persons, 'firstname', 'lastname'))
                        select_person_id = find_person_id(persons, selected_person)
                        submit_button = st.form_submit_button(label='Submit')
                        if submit_button:
                            projects_table.set_new_project(project_name, project_aim, project_budget, select_person_id)
                            st.cache_data.clear()
                        else:
                            st.write('To succeed please fill and select inputs and smash a Submit button.')
                with tab2:
                    with st.form('add task', clear_on_submit=True):
                        st.write("Add New Task:")
                        selected_task = st.text_input('Provide task name:')
                        selected_start_date = st.date_input('Provide start date:', value=None, format="YYYY/MM/DD")
                        selected_due_date = st.date_input('Provide due date:', value=None, format="YYYY/MM/DD")
                        selected_person = st.selectbox('Select a assignee:', make_a_list(persons, 'firstname',
                                                                                         'lastname'))
                        select_person_id = find_person_id(persons, selected_person)
                        selected_project = st.selectbox('Select a Project task is for:',
                                                        make_a_list(projects, 'project_name'))
                        select_project_id = find_project_id(projects, selected_project)
                        submit_button = st.form_submit_button(label='Submit')
                        if submit_button:
                            tasks_table.set_new_task(selected_project, selected_task, selected_start_date,
                                                     selected_due_date,
                                                     select_person_id, select_project_id)
                            st.cache_data.clear()
                        else:
                            st.write('To succeed please select and fill inputs and smash a Submit button.')
                with tab3:
                    with st.form('add person', clear_on_submit=True):
                        st.write("Add New Person:")
                        provided_firstname = st.text_input('Provide first name:')
                        provided_lastname = st.text_input('Provide last name:')
                        provided_email = st.text_input('Provide email:')
                        provided_salary = st.number_input('Provide salary value, $:', min_value=40000.0,
                                                          max_value=100000.0, step=10.0, value=50000.0)
                        submit_button = st.form_submit_button(label='Submit')
                        if submit_button:
                            persons_table.set_new_person(provided_firstname, provided_lastname, provided_email,
                                                         provided_salary)
                            st.cache_data.clear()
                        else:
                            st.write('To succeed please fill inputs and smash a Submit button.')

    # -------------- Delete Items Section --------------
    with (st.container()):
        st.write("---")
        left_column, right_column = st.columns([1, 3])
        with left_column:
            st.header("Get Ride of the Item")
            st.write('Delete selected unnecessary items.')
        with right_column:
            tab1, tab2, tab3 = st.tabs(["delete task", "delete person", "delete project"])
            with tab1:
                with st.form('delete_task', clear_on_submit=True):
                    st.write("Delete task:")
                    select_task = st.selectbox('Select a Task to delete', make_a_list(tasks, 'task_name'))
                    submit_button = st.form_submit_button(label='Submit')
                    if submit_button:
                        tasks_table.set_delete_task(select_task)
                        st.cache_data.clear()
                    else:
                        st.write('To succeed please select input and smash a Submit button.')
            with tab2:
                with st.form('delete_person', clear_on_submit=True):
                    st.write("Delete person:")
                    select_person = st.selectbox('Select a Person to delete',
                                                 make_a_list(persons, 'firstname', 'lastname'))
                    select_person_id = find_person_id(persons, select_person)
                    submit_button = st.form_submit_button(label='Submit')
                    if submit_button:
                        persons_table.set_delete_person(select_person, select_person_id)
                        st.cache_data.clear()
                    else:
                        st.write('To succeed please select input and smash a Submit button.')
            with tab3:
                with st.form('delete_project', clear_on_submit=True):
                    st.write("Delete Project:")
                    select_project = st.selectbox('Select a Project to delete',
                                                  make_a_list(projects, 'project_name'))
                    submit_button = st.form_submit_button(label='Submit')
                    if submit_button:
                        projects_table.set_delete_project(select_project)
                        st.cache_data.clear()
                    else:
                        st.write('To succeed please select input and smash a Submit button.')

    footer_section()


if __name__ == "__main__":
    main()
