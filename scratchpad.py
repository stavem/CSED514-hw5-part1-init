import COVID19_vaccine
from sql_connection_manager import SqlConnectionManager
from COVID19_vaccine import *
import os
from utils import *

with SqlConnectionManager(Server=os.getenv("Server"),
                          DBname=os.getenv("DBName"),
                          UserId=os.getenv("UserID"),
                          Password=os.getenv("Password")) as sqlClient:
    with sqlClient.cursor(as_dict=True) as cursor:
        # #
        # # # # clear the tables before testing
        # # clear_tables(sqlClient)
        # # #
        # # # # make sure there is a vaccine in the db
        # blah6 = COVID19Vaccine(name="blah6",
        #                     supplier="Pfizer-BioNTech",
        #                     available_doses=9,
        #                     reserved_doses=3,
        #                     total_doses=12,
        #                     doses_per_patient=2,
        #                     days_between_doses=21,
        #                     cursor=cursor)
        # # Add test pfizer doses
    blah6.AddDoses('blah6',3,cursor)
        # blah.AddDoses('blah', 3, cursor)

        #     # check if the vaccine is correctly inserted into the database
        #     sqlQuery = "SELECT AvailableDoses, TotalDoses FROM Vaccines WHERE VaccineName = 'Pfizer'"
        #     cursor.execute(sqlQuery)
        #     rows = cursor.fetchall()
        #     print(rows)
        #     if len(rows) < 1:
        #         self.fail("Less than 1 row")
        #
        #     print(rows[0]['AvailableDoses'])
        # except Exception:
        #     # clear the tables if an exception occurred
        #     clear_tables(sqlClient)
        #     self.fail("Adding doses failed.")
        #
        # # ensure the totals are correct
        # self.assertEqual(3, rows[0]['AvailableDoses'])
        # self.assertEqual(6, rows[0]['TotalDoses'])