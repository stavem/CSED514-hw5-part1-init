from sql_connection_manager import SqlConnectionManager
from COVID19_vaccine import COVID19Vaccine
import os
from utils import *

with SqlConnectionManager(Server=os.getenv("Server"),
                          DBname=os.getenv("DBName"),
                          UserId=os.getenv("UserID"),
                          Password=os.getenv("Password")) as sqlClient:
    with sqlClient.cursor(as_dict=True) as cursor:

        # Add test pfizer doses
        COVID19Vaccine.AddDoses('Pfizer', 2, cursor)
