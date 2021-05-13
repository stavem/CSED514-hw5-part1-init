import unittest
import os

from sql_connection_manager import SqlConnectionManager
from COVID19_vaccine import COVID19Vaccine
from utils import *


class TestCovid19Vaccine(unittest.TestCase):
    def test_init(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new VaccineCaregiver object
                    self.vaccine_a = COVID19Vaccine(name="Pfizer",
                                                    supplier="Pfizer-BioNTech",
                                                    available_doses=1,
                                                    reserved_doses=3,
                                                    total_doses=4,
                                                    doses_per_patient=2,
                                                    days_between_doses=21,
                                                    cursor=cursor)

                    # check if the vaccine is correctly inserted into the database
                    sqlQuery = "SELECT * FROM Vaccines WHERE VaccineName = 'Pfizer'"
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) < 1:
                        self.fail("Less than 1 row")
                    # clear the tables after testing, just in-case
                    # clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Creating vaccine failed")


if __name__ == '__main__':
    unittest.main()
