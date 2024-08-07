"""Persons class and class Methods"""
import streamlit as st
import pandas as pd
from psycopg2 import sql
from sqlalchemy import update, insert, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

SessionLocal = sessionmaker(autocommit=False, autoflush=False)
Base = declarative_base()


class Person(Base):
    __tablename__ = 'persons'
    person_id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    email = Column(String, nullable=False)

    def __repr__(self) -> str:
        return (f"<Person(project_id={self.project_id}, project_name={self.project_name}, "
                f"project_aim={self.project_aim}, project_budget={self.project_budget}, "
                f"person_id={self.person_id})>")


class Persons:
    table_name = "Persons"
    columns = ('person_id', 'firstname', 'lastname', 'salary', 'email')

    def __init__(self, connection):
        self.db_connection = connection
        self.session = connection.session

    def create_table(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            person_id SERIAL PRIMARY KEY,
            firstname VARCHAR(40) NOT NULL,
            lastname VARCHAR(40) NOT NULL,
            salary NUMBER NOT NULL,
            email VARCHAR(30) UNIQUE NOT NULL)"""
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

    def get_all_persons(self) -> object:
        """
        Gets (Streamlit Query) all persons from table
        :param: None
        :return object: returns table object
        """
        query = f"SELECT * FROM {self.table_name} ORDER BY person_id"
        return self.db_connection.query(query)

    def select_assignees_tasks(self) -> object:
        """
        Gets (Streamlit Query) all assignees tasks from two tables
        :param: None
        :return object: returns table object
        """
        query = f"SELECT p.person_id, CONCAT(p.firstname, ' ', p.lastname) as assignee, t.task_name, t.start_date, t.due_date, \
                t.status FROM persons as p JOIN persontask as pt ON p.person_id = pt.person_id \
                JOIN tasks as t ON pt.task_id = t.task_id GROUP BY p.person_id, t.task_name, t.start_date, t.due_date, \
                t.status ORDER BY p.firstname ASC, t.status ASC"
        return self.db_connection.query(query)

    def select_managers_projects(self) -> object:
        """
        Gets (Streamlit Query) all managers projects from two tables
        :param: None
        :return object: returns table object
        """
        query = f"SELECT p.person_id, CONCAT(p.firstname, ' ', lastname) as manager, p.email, p.salary, pr.project_name, \
                pr.project_budget FROM persons as p JOIN projects as pr ON p.person_id = pr.person_id \
                ORDER BY p.firstname"
        return self.db_connection.query(query)

    def set_persons_salary(self, fullname, salary, person_id) -> None:
        """
        Update (SQLAlchemy) Selected Person Salary with a new value provided by user
        :param fullname: string selected by user in the form
        :param person_id: number calculated from DataFrame by fullname string
        :param salary: float provided by user
        :return: None
        """
        stmt = (update(Person).where(Person.person_id == person_id).values({"salary": int(salary)}))
        query = f"UPDATE {self.table_name} SET salary = salary * 1.5 WHERE person_id = '{person_id}'"
        self.session.execute(stmt)
        self.session.commit()
        return st.write(f"The salary for _{fullname}_ was updated to _{salary}_.")

    # 'firstname', 'lastname', 'salary', 'email'
    def set_new_person(self, firstname: str, lastname: str, email: str, salary: float) -> None:
        """
        Insert (SQLAlchemy) New Person with a values provided by the user with a check if person already exist
        :param firstname: string provided by user
        :param lastname: string provided by user
        :param email: string provided by user
        :param salary: number provided by user
        :return: None
        """
        stmt = insert(Person).values({'firstname': firstname, 'lastname': lastname,
                                      'email': email, 'salary': salary})
        df = self.get_all_persons()
        if firstname + lastname in df['firstname'].values + df['lastname']:
            return st.write(f"The person _{firstname + ' ' + lastname}_ already exists.")
        else:
            self.session.execute(stmt)
            self.session.commit()
            return st.write(f"The new person _{firstname + ' ' + lastname}_ was added.")

    def has_data(self):
        query = f"SELECT EXISTS (SELECT 1 FROM {self.table_name} LIMIT 1);"
        self.db_connection.cursor.execute(query)
        is_data = self.db_connection.cursor.fetchall()[0][0]
        if is_data:
            print(f"Table '{self.table_name}' has some data already.")
        else:
            print(f"Table '{self.table_name}' has any data.")
        return is_data

    def delete_all(self):
        query = f"TRUNCATE ONLY {self.table_name} RESTART IDENTITY"
        self.db_connection.cursor.execute(query)
        print(f"All Data from table '{self.table_name}' were deleted.")

    def drop_table(self):
        query = f"DROP TABLE IF EXISTS {self.table_name}"
        self.db_connection.cursor.execute(query)
        print(f"Table '{self.table_name}' was entirely deleted and indexes reset.")
