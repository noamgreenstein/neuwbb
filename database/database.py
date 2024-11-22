import sqlite3


class Database:
    def __init__(self):
        self.cursor = sqlite3.connect("db")

    def execute(self, statement):
        return self.cursor.execute(statement)

    def get_one(self, statement):
        return self.execute(statement).fetchone()

    def get_all(self, statement):
        return self.execute(statement).fetchall()

    def execute_insert(self, insert):
        self.execute(insert)
        self.cursor.commit()
        return 'Success'
