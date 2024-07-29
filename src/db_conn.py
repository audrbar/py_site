import streamlit as st


class DBEngine:
    def __init__(self):
        self.connection = self.connect()

    @staticmethod
    def connect():
        try:
            connection = st.connection("postgresql", type="sql")
            print("\nConnected to PostgresSQL database. Congratulations!")
        except (Exception, st.error) as error:
            raise Exception("Error while connecting to PostgresSQL", error)

        return connection

    def __del__(self):
        if self.connection:
            self.connection.session.close()
            print('That is it. Connection closed!')
