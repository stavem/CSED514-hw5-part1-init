import unittest
import os

from sql_connection_manager import SqlConnectionManager
from COVID19_vaccine import *
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
                    # create a new Vaccine object
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

    def test_add_doses(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # make sure there is a vaccine in the db
                    self.vaccine_b = COVID19Vaccine(name="Pfizer",
                                                    supplier="Pfizer-BioNTech",
                                                    available_doses=1,
                                                    reserved_doses=3,
                                                    total_doses=4,
                                                    doses_per_patient=2,
                                                    days_between_doses=21,
                                                    cursor=cursor)
                    # Add test pfizer doses
                    AddDoses('Pfizer', 2, cursor)

                    # check if the vaccine is correctly inserted into the database
                    sqlQuery = "SELECT AvailableDoses, TotalDoses FROM Vaccines WHERE VaccineName = 'Pfizer'"
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    print(rows)
                    if len(rows) < 1:
                        self.fail("Less than 1 row")

                    print(rows[0]['AvailableDoses'])
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Adding doses failed.")

                # ensure the totals are correct
                self.assertEqual(3, rows[0]['AvailableDoses'])
                self.assertEqual(6, rows[0]['TotalDoses'])

    def test_reserve_doses(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # make sure there is a vaccine in the db
                    self.vaccine_b = COVID19Vaccine(name="Pfizer",
                                                    supplier="Pfizer-BioNTech",
                                                    available_doses=5,
                                                    reserved_doses=3,
                                                    total_doses=8,
                                                    doses_per_patient=2,
                                                    days_between_doses=21,
                                                    cursor=cursor)
                    # Add test pfizer doses
                    ReserveDoses('Pfizer', 2, cursor)

                    # check if the vaccine is correctly inserted into the database
                    sqlQuery = "SELECT AvailableDoses, ReservedDoses, TotalDoses FROM Vaccines WHERE VaccineName = 'Pfizer'"
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    print(rows)
                    if len(rows) < 1:
                        self.fail("Less than 1 row")

                    print(rows[0])
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Reserving doses failed.")

                # ensure the totals are correct
                self.assertEqual(3, rows[0]['AvailableDoses'])
                self.assertEqual(8, rows[0]['TotalDoses'])
                self.assertEqual(5, rows[0]['ReservedDoses'])

    def test_check_available_doses(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)

                    # make sure there is a vaccine in the db
                    self.vaccine_b = COVID19Vaccine(name="Pfizer",
                                                    supplier="Pfizer-BioNTech",
                                                    available_doses=5,
                                                    reserved_doses=3,
                                                    total_doses=8,
                                                    doses_per_patient=2,
                                                    days_between_doses=21,
                                                    cursor=cursor)
                    # Add test pfizer doses
                    check_available_doses('Pfizer', cursor)

                    # check if the vaccine is correctly inserted into the database
                    sqlQuery = "SELECT AvailableDoses FROM Vaccines WHERE VaccineName = 'Pfizer'"
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    print(rows)
                    if len(rows) < 1:
                        self.fail("Less than 1 row")

                    print(rows[0])
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Checking doses failed.")

                # ensure the totals are correct
                self.assertEqual(5, rows[0]['AvailableDoses'])

if __name__ == '__main__':
    unittest.main()