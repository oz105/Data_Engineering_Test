
import mysql.connector


class SqlDB:

    # static var
    db = None
    my_cursor = None

    # init the connection and the database
    def __init__(self):
        if self.db is None:
            self.mydb = mysql.connector.connect(host="localhost", user="root", password="pass123",
                                                port="3306", database="data_engineering_test")
            self.my_cursor = self.mydb.cursor()
            print("created")

        else:
            self.mydb = self.db

    # This function insert one row to the database
    def insert_one_row(self, values):

        sql_insert_query = "INSERT INTO jobs (JobNum, JobTitle, Country, City, JobDescription) VALUES (%s, %s, %s, %s, %s)"

        try:
            # Executing the SQL command
            # Commit your changes in the database

            self.my_cursor.execute(sql_insert_query, values)
            self.mydb.commit()
            print("Row added")

        except:
            # Rolling back in case of error
            print("Error")
            self.mydb.rollback()

    # this function insert many rows to the database
    def insert_many(self, values):

        sql_insert_query = "INSERT INTO jobs (JobNum, JobTitle, Country, City, JobDescription) VALUES (%s, %s, %s, %s, %s)"

        try:
            # Executing the SQL command
            # Commit your changes in the database

            self.my_cursor.executemany(sql_insert_query, values)
            self.mydb.commit()
            print("Rows added")

        except:
            # Rolling back in case of error
            print("Error")
            self.mydb.rollback()

    # This function print all rows of the database
    def select_all(self):
        sql_select_query = "SELECT * FROM jobs"
        try:
            self.my_cursor.execute(sql_select_query)
            rows = self.my_cursor.fetchall()
            print("The rows are: \n")
            for row in rows:
                print(row)
                print('\n')
        except:
            # Rolling back in case of error
            print("Error")
            self.mydb.rollback()

    # This function delete all rows in the database

    def delete_all_rows(self):

        try:
            sql_delete_query = "TRUNCATE TABLE jobs"
            self.my_cursor.execute(sql_delete_query)
            self.mydb.commit()

            print("All rows deleted")
        except:
            # Rolling back in case of error
            print("Error")
            self.mydb.rollback()

