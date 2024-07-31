from psycopg2 import sql


class Persons:
    table_name = "Persons"
    columns = ('person_id', 'firstname', 'lastname', 'salary', 'email')

    def __init__(self, connection):
        self.db_connection = connection

    def create_table(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            person_id SERIAL PRIMARY KEY,
            firstname VARCHAR(40) NOT NULL,
            lastname VARCHAR(40) NOT NULL,
            salary MONEY NOT NULL,
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

    def append_data(self, data):
        for item in data:
            query = f"INSERT INTO {self.table_name} (firstname, lastname, salary, email) VALUES {item}"
            self.db_connection.cursor.execute(query)

        self.db_connection.connection.commit()
        print(f"Table '{self.table_name}' were appended with new data.")

    def select_all(self):
        query = f"SELECT * FROM {self.table_name}"
        return self.db_connection.query(query)

    def select_assignees_tasks(self):
        query = f"SELECT CONCAT(p.firstname, ' ', p.lastname) as assignee, t.task_name, t.start_date, t.due_date, \
                t.status FROM persons as p JOIN persontask as pt ON p.person_id = pt.person_id \
                JOIN tasks as t ON pt.task_id = t.task_id GROUP BY p.person_id, t.task_name, t.start_date, t.due_date, \
                t.status ORDER BY p.firstname ASC, t.status ASC"
        return self.db_connection.query(query)

    def select_managers_projects(self):
        query = f"SELECT CONCAT(p.firstname, ' ', lastname) as manager, p.email, p.salary, pr.project_name, \
                pr.project_budget FROM persons as p JOIN projects as pr ON p.person_id = pr.person_id \
                ORDER BY p.firstname"
        return self.db_connection.query(query)

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

    def update_salary(self, person_id):
        query = f"UPDATE {self.table_name} SET salary = salary * 1.5 WHERE person_id = '{person_id}'"
        self.db_connection.cursor.execute(query)
        self.db_connection.connection.commit()
        print("Person's 'Salary' was changed.")

    def drop_table(self):
        query = f"DROP TABLE IF EXISTS {self.table_name}"
        self.db_connection.cursor.execute(query)
        print(f"Table '{self.table_name}' was entirely deleted and indexes reset.")
