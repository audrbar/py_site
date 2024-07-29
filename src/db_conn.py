import os
import streamlit as st
import psycopg2.extras
from dotenv import load_dotenv
from pathlib import Path


# load_dotenv(Path("/secrets.toml"))


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
