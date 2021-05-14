import COVID19_vaccine
import os
from sql_connection_manager import SqlConnectionManager

with SqlConnectionManager(Server=os.getenv("Server"),
                          DBname=os.getenv("DBName"),
                          UserId=os.getenv("UserID"),
                          Password=os.getenv("Password")) as sqlClient:
    with sqlClient.cursor(as_dict=True) as cursor:
        COVID19_vaccine.ReserveDoses('Pfizer', 3, cursor)