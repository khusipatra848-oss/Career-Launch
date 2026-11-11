
import mysql.connector
from db_config import db_config

try:
    connection = mysql.connector.connect(**db_config)

    if connection.is_connected():
        print("CareerLaunch Database Connected Successfully!")

    connection.close()

except mysql.connector.Error as error:
    print("Database Connection Failed:", error)
