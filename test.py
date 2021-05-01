import unittest
from VaccineReservationScheduler import SqlConnectionManager
from COVID19Vaccine import COVID19Vaccine
from VaccinePatient import VaccinePatient
from VaccineCaregiver import VaccineCaregiver
import os


def _truncate_vaccine(client):
    sqlQuery = '''TRUNCATE TABLE Vaccines'''
    client.cursor().execute(sqlQuery)
    client.commit()


def _truncate_patient(client):
    sqlQuery = '''DELETE FROM Patients'''
    client.cursor().execute(sqlQuery)
    client.commit()


def _truncate_caregiver(client):
    sqlQuery = '''Truncate Table CareGiverSchedule'''
    client.cursor().execute(sqlQuery)
    client.commit()
    sqlQuery = '''Delete From Caregivers'''
    client.cursor().execute(sqlQuery)
    client.commit()


class TestDB(unittest.TestCase):

    def test_db_connection(self):
        try:
            self.connection_manager = SqlConnectionManager(Server=os.getenv("Server"),
                                                           DBname=os.getenv("DBName"),
                                                           UserId=os.getenv("UserID"),
                                                           Password=os.getenv("Password"))
            self.conn = self.connection_manager.Connect()
        except Exception:
            self.fail("Connection to databse failed")


class TestCOVID19Vaccine(unittest.TestCase):

    def test_init(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor() as cursor:
                try:
                    _truncate_vaccine(sqlClient)
                    # creating a new Vaccine
                    self.vaccine_a = COVID19Vaccine(vaccineName="a",
                                                    vaccineSupplier="steve",
                                                    dosesPerPatient=2,
                                                    daysBetweenDoses=30,
                                                    cursor=sqlClient.cursor())
                    # check if the vaccine is inserted into the DB
                    sqlQuery = '''
                               SELECT *
                               FROM Vaccines
                               WHERE vaccineName = 'a' AND vaccineSupplier = 'Steve' AND dosesPerPatient = 2
                               AND daysBetweenDoses = 30
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) != 1:
                        self.fail("Creating vaccine failed")
                    _truncate_vaccine(sqlClient)
                except Exception:
                    _truncate_vaccine(sqlClient)
                    self.fail("Creating vaccine failed")

    def test_add_doses(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor() as cursor:
                try:
                    _truncate_vaccine(sqlClient)
                    # creating a new Vaccine
                    self.vaccine_a = COVID19Vaccine(vaccineName="a",
                                                    vaccineSupplier="steve",
                                                    dosesPerPatient=2,
                                                    daysBetweenDoses=30,
                                                    cursor=sqlClient.cursor())
                    # add doses to the vaccine
                    added = self.vaccine_a.AddDoses(DosesToAdd=2, cursor=cursor)
                    self.assertEqual(added, 2)
                    # check the db
                    sqlQuery = '''
                               SELECT AvailableDoses
                               FROM Vaccines
                               WHERE vaccineName = 'a' AND vaccineSupplier = 'Steve' AND dosesPerPatient = 2
                               AND daysBetweenDoses = 30
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) != 1 or rows[0][0] != 2:
                        self.fail("Add doses to vaccine failed")
                    _truncate_vaccine(sqlClient)
                except Exception:
                    _truncate_vaccine(sqlClient)
                    self.fail("Add doses to vaccine failed")

    def test_reserve_doses_exceed_available_doses(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor() as cursor:
                try:
                    _truncate_vaccine(sqlClient)
                    # creating a new Vaccine
                    self.vaccine_a = COVID19Vaccine(vaccineName="a",
                                                    vaccineSupplier="steve",
                                                    dosesPerPatient=2,
                                                    daysBetweenDoses=30,
                                                    cursor=sqlClient.cursor())
                    self.vaccine_a.AddDoses(DosesToAdd=2, cursor=cursor)
                    res = self.vaccine_a.ReserveDoses(DosesToReserve=3, cursor=cursor)
                    self.assertEqual(res, -1)
                    _truncate_vaccine(sqlClient)
                except Exception:
                    _truncate_vaccine(sqlClient)
                    self.fail("Reserve doses failed")

    def test_reserve_doses_success(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor() as cursor:
                try:
                    _truncate_vaccine(sqlClient)
                    # creating a new Vaccine
                    self.vaccine_a = COVID19Vaccine(vaccineName="a",
                                                    vaccineSupplier="steve",
                                                    dosesPerPatient=2,
                                                    daysBetweenDoses=30,
                                                    cursor=sqlClient.cursor())
                    self.vaccine_a.AddDoses(DosesToAdd=3, cursor=cursor)
                    res = self.vaccine_a.ReserveDoses(DosesToReserve=2, cursor=cursor)
                    self.assertEqual(res, 2)
                    # check the db
                    sqlQuery = '''
                               SELECT AvailableDoses
                               FROM Vaccines
                               WHERE vaccineName = 'a' AND vaccineSupplier = 'Steve' AND dosesPerPatient = 2
                               AND daysBetweenDoses = 30
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) != 1 or rows[0][0] != 1:
                        self.fail("Reserve doses failed")
                    _truncate_vaccine(sqlClient)
                except Exception:
                    _truncate_vaccine(sqlClient)
                    self.fail("Reserve doses failed")


class TestVaccineCaregiver(unittest.TestCase):
    def test_init(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor() as cursor:
                try:
                    _truncate_caregiver(sqlClient)
                    # creating a new caregiver
                    self.caregiver_a = VaccineCaregiver(name="ABC",
                                                    cursor=sqlClient.cursor())
                    # check if the patient is inserted into the DB
                    sqlQuery = '''
                               SELECT *
                               FROM Caregivers
                               WHERE CaregiverName = 'ABC'
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) != 1:
                        self.fail("Creating caregiver failed")
                    _truncate_caregiver(sqlClient)
                except Exception:
                    _truncate_caregiver(sqlClient)
                    self.fail("Creating caregiver failed")

class TestVaccinePatient(unittest.TestCase):

    def test_init(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor() as cursor:
                try:
                    _truncate_patient(sqlClient)
                    # creating a new patient
                    self.patient_a = VaccinePatient(PatientName="Steve",
                                                    cursor=sqlClient.cursor())
                    # check if the patient is inserted into the DB
                    sqlQuery = '''
                               SELECT *
                               FROM Patients
                               WHERE PatientName = 'Steve'
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) != 1:
                        self.fail("Creating patient failed")
                    _truncate_patient(sqlClient)
                except Exception:
                    _truncate_patient(sqlClient)
                    self.fail("Creating patient failed")

    # def test_reserve_appointment_success(self):
    #     with SqlConnectionManager(Server=os.getenv("Server"),
    #                               DBname=os.getenv("DBName"),
    #                               UserId=os.getenv("UserID"),
    #                               Password=os.getenv("Password")) as sqlClient:
    #         with sqlClient.cursor() as cursor:
    #             try:
    #                 _truncate_patient(sqlClient)
    #                 # creating a new patient
    #                 self.patient_a = VaccinePatient(PatientName="Steve",
    #                                                 cursor=sqlClient.cursor())
    #                 # add care giver
    #                 self.patient_a.ReserveAppointment(CaregiverSchedulingID=, Vaccine=, cursor=cursor)
    #
    #                 _truncate_patient(sqlClient)
    #             except Exception:
    #                 _truncate_patient(sqlClient)
    #                 self.fail("Reserve appointment failed")



if __name__ == '__main__':
    unittest.main()
