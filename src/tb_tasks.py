"""Tasks class and class Methods"""
import streamlit as st
from psycopg2 import sql
from sqlalchemy import update, insert, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

SessionLocal = sessionmaker(autocommit=False, autoflush=False)
Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True)
    task_name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    done_date = Column(Date, nullable=True)
    status = Column(String, nullable=False)
    person_id = Column(Integer, nullable=False)
    project_id = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return (f"<Task(project_id={self.task_id}, project_name={self.task_name}, "
                f"start_date={self.start_date}, due_date={self.due_date}, done_date={self.done_date},"
                f"status={self.status}, person_id={self.person_id}, project_id={self.project_id})>")


class Tasks:
    table_name = "tasks"
    columns = ('task_id', 'task_name', 'start_date', 'due_date', 'done_date', 'status', 'person_id', 'project_id')

    def __init__(self, connection):
        self.db_connection = connection
        self.session = connection.session

    def create_table(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            task_id SERIAL PRIMARY KEY,
            task_name VARCHAR(255) NOT NULL,
            start_date DATE NOT NULL,
            due_date DATE NOT NULL,
            done_date DATE,
            status VARCHAR(30) NOT NULL,
            person_id INT,
            project_id INT,
            FOREIGN KEY (person_id) REFERENCES Persons(person_id),
            FOREIGN KEY (project_id) REFERENCES Projects(project_id)
            );
        """
        self.db_connection.cursor.execute(query)
        self.db_connection.connection.commit()
        print(f"Table '{self.table_name}' was created (if it not existed yet).")

    def insert_data(self, df):
        for _, row in df.iterrows():
            columns = sql.SQL(', ').join(map(sql.Identifier, self.columns))
            values = sql.SQL(', ').join(map(sql.Placeholder, df.keys()))
            table_name = sql.SQL(self.table_name)
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(table_name, columns, values)
            self.db_connection.cursor.execute(query, row.to_dict())

        self.db_connection.connection.commit()
        print(f"Data were inserted into the table '{self.table_name}'.")

    def __get_all_tasks(self) -> object:
        """
        Gets (Streamlit Query) all tasks from table
        :param: None
        :return object: returns table object
        """
        query = f"SELECT * FROM {self.table_name} ORDER BY task_id"
        return self.db_connection.query(query)

    def get_tasks_assignees(self) -> object:
        """
        Gets (Streamlit Query) all tasks from table joined with person fullname
        :param: None
        :return object: returns table object
        """
        query = f"SELECT t.task_id, t.task_name, t.start_date, t.due_date, t.status, \
                CONCAT(p.firstname, ' ', p.lastname) as Assignee FROM tasks as t JOIN persons as p ON \
                t.person_id = p.person_id ORDER BY t.task_id"
        return self.db_connection.query(query)

    def set_task_assignee(self, task_name, fullname, person_id) -> None:
        """
        Updates (SQLAlchemy) Selected Task Assignee by Person id with a new value selected by user
        :param task_name: string selected by user
        :param fullname: string selected by user in the form
        :param person_id: number calculated from DataFrame by fullname string
        :return: None
        """
        stmt = (update(Task).where(Task.task_name == task_name).values({"person_id": int(person_id)}))
        self.session.execute(stmt)
        self.session.commit()
        return st.write(f"The assignee for the task {task_name} was updated to {fullname}.")

    def set_task_status(self, task_name, status) -> None:
        """
        Updates (SQLAlchemy) Selected Task Status with a new value selected by user
        :param task_name: string selected by user in the form
        :param status: string selected by user in the form
        :return: None
        """
        stmt = (update(Task).where(Task.task_name == task_name).values({"status": status}))
        self.session.execute(stmt)
        self.session.commit()
        return st.write(f"The status for the task _{task_name}_ was updated to _{status}_.")

    def set_new_task(self, selected_project: str, task_name: str, start_date: Date, due_date: Date, person_id: int,
                     project_id: int, status: str = 'not_started') -> None:
        """
        Insert (SQLAlchemy) New Task with a values provided by the user with a check if task already exist
        :param selected_project: string provided for message purpose
        :param task_name: string provided by user
        :param start_date: Date provided by user
        :param due_date: Date provided by user
        :param status: string - default value
        :param person_id: number selected by user
        :param project_id: number selected by user
        :return: None
        """
        stmt = insert(Task).values({'task_name': task_name, 'start_date': start_date, 'due_date': due_date,
                                    'person_id': person_id, 'project_id': project_id, 'status': status})
        df = self.__get_all_tasks()
        if task_name in df['task_name'].values:
            return st.write(f"The project _{task_name}_ already exists.")
        else:
            self.session.execute(stmt)
            self.session.commit()
            return st.write(f"The new task _{task_name}_ was for the project _{selected_project}_ was created.")

    def set_delete_task(self, task_name):
        """
        Delete (SQLAlchemy) Selected Task by task name
        :param task_name: string selected by user
        :return: None
        """
        stmt = delete(Task).where(Task.task_name == task_name)
        self.session.execute(stmt)
        self.session.commit()
        return st.write(f"The project _{task_name}_ was deleted.")
