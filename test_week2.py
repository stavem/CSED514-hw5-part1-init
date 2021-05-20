import unittest
from sql_connection_manager import SqlConnectionManager
from vaccine_patient import VaccinePatient
from utils import *
import os


class TestVaccinePatient(unittest.TestCase):
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
                    self.patient_a = VaccinePatient(name="Karl Stavem",
                                                      status=0,
                                                      cursor=cursor)
                    # check if the patient is correctly inserted into the database
                    sqlQuery = '''
                               SELECT *
                               FROM Patients
                               WHERE PatientName = 'Karl Stavem'
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) < 1:
                        self.fail("Creating patient failed")
                    # clear the tables after testing, just in-case
                    # clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Creating patient failed")


if __name__ == '__main__':
    unittest.main()
