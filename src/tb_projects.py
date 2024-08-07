"""Projects class and class Methods"""
import streamlit as st
import pandas as pd
from psycopg2 import sql
from sqlalchemy import update, insert, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

SessionLocal = sessionmaker(autocommit=False, autoflush=False)
Base = declarative_base()


class Project(Base):
    __tablename__ = 'projects'
    project_id = Column(Integer, primary_key=True)
    project_name = Column(String, nullable=False)
    project_aim = Column(String, nullable=False)
    project_budget = Column(Float, nullable=False)
    person_id = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return (f"<Project(project_id={self.project_id}, project_name={self.project_name}, "
                f"project_aim={self.project_aim}, project_budget={self.project_budget}, "
                f"person_id={self.person_id})>")


class Projects:
    table_name = "projects"
    columns = ('project_id', 'project_name', 'project_aim', 'project_budget', 'person_id')

    def __init__(self, connection):
        self.db_connection = connection
        self.session = connection.session

    def create_table(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            project_id SERIAL PRIMARY KEY,
            project_name VARCHAR(255) NOT NULL,
            project_aim VARCHAR(255) NOT NULL,
            project_budget NUMBER NOT NULL,
            person_id INT,
            FOREIGN KEY (person_id) REFERENCES Persons(person_id)
            );
        """
        self.db_connection.connection.execute(query)
        print(f"Table '{self.table_name}' was created (if it not existed yet).")

    def insert_data(self, df):
        for _, row in df.iterrows():
            columns = sql.SQL(', ').join(map(sql.Identifier, self.columns))
            values = sql.SQL(', ').join(map(sql.Placeholder, df.keys()))
            table_name = sql.SQL(self.table_name)
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(table_name, columns, values)
            self.db_connection.connection.execute(query, row.to_dict())

        self.db_connection.connection.commit()
        print(f"Data were inserted into the table '{self.table_name}'.")

    def get_all_projects(self) -> object:
        """
        Gets (Streamlit Query) all projects from table joined with manager fullname
        :param: None
        :return object: returns table object
        """
        query = f"SELECT pr.project_id, pr.project_name, pr.project_aim, pr.project_budget,\
                 CONCAT(p.firstname, ' ', p.lastname) as project_manager\
                 FROM {self.table_name} as pr JOIN persons as p ON p.person_id = pr.person_id \
                 ORDER BY pr.project_id ASC"
        return self.db_connection.query(query)

    def update_project_manager(self, project_name, fullname, person_id) -> None:
        """
        Update (SQLAlchemy) Selected Project Manager by Person id with a new value selected by user
        :param project_name: string selected by user
        :param fullname: string selected by user in the form
        :param person_id: number calculated from DataFrame by fullname string
        :return: None
        """
        stmt = (update(Project).where(Project.project_name == project_name)
                .values({"person_id": int(person_id)}))
        self.session.execute(stmt)
        self.session.commit()
        return st.write(f"The manager for project {project_name} was updated to {fullname}.")

    def update_project_budget(self, project_name, project_budget: int) -> None:
        """
        Update (SQLAlchemy) Selected Project Budget with a new value provided by user
        :param project_name: string selected by user
        :param project_budget: number provided by user
        :return: None
        """
        stmt = (update(Project).where(Project.project_name == project_name)
                .values({"project_budget": int(project_budget)}))
        self.session.execute(stmt)
        self.session.commit()
        return st.write(f"The budget for project {project_name} was updated to {project_budget}.")

    def set_new_project(self, project_name: str, project_aim: str, project_budget: float, person_id: int) -> None:
        """
        Insert (SQLAlchemy) New Project with a values provided by the user with a check if project name already exist
        :param project_name: string provided by user
        :param project_aim: string provided by user
        :param project_budget: float provided by user
        :param person_id: number provided by user
        :return: None
        """
        stmt = insert(Project).values({'project_name': project_name, 'project_aim': project_aim,
                                      'project_budget': project_budget, 'person_id': person_id})
        df = self.get_all_projects()
        if project_name in df['project_name'].values:
            return st.write(f"The project _{project_name}_ already exists.")
        else:
            self.session.execute(stmt)
            self.session.commit()
            return st.write(f"The new project _{project_name}_ was created.")

    def set_delete_project(self, project_name):
        """
        Delete (SQLAlchemy) Selected Project selected by project name
        :param project_name: string selected by user
        :return: None
        """
        stmt = delete(Project).where(Project.project_name == project_name)
        self.session.execute(stmt)
        self.session.commit()
        return st.write(f"The project _{project_name}_ was deleted.")
