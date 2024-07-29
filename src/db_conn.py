import streamlit as st


class DBEngine:
    def __init__(self):
        self.connection = self.connect()

    @staticmethod
    def connect():
        try:
            connection = st.connection("postgresql", type="sql")
            print("Connected to PostgreSQL database.")
        except (Exception, st.error) as error:
            raise Exception("Error while connecting to PostgreSQL", error)

        return connection

    def __del__(self):
        if self.connection:
            self.connection.session.close()
            print('Connection to PostgreSQL database closed!')
