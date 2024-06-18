import mysql.connector
import pandas as pd


class Conexion:

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost", 
            user="root",
            password="",
            database="northwind"
        )

    def use_database(self,script):
        mycursor = self.mydb.cursor()
        mycursor.execute(script)
       
       
    
    def execute_query(self,query):
        mycursor = self.mydb.cursor()
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        column_names = [i[0] for i in mycursor.description]
        df = pd.DataFrame(myresult, columns=column_names)
        return df

        

