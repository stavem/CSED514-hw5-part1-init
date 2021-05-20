import unittest
from sql_connection_manager import SqlConnectionManager
from vaccine_patient import VaccinePatient
from COVID19_vaccine import COVID19Vaccine
from vaccine_caregiver import VaccineCaregiver
from vaccine_reservation_scheduler import VaccineReservationScheduler as vrs
import time
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

    def test_reserve_appointment(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new VaccineCaregiver object

                    sample_caregiver = VaccineCaregiver(name="Dr. Fauci", cursor=cursor)
                    sample_patient = VaccinePatient(name="Karl Stavem", status=0, cursor=cursor)
                    sample_vaccine = COVID19Vaccine(name="Pfizer",
                                                    supplier="Pfizer-BioNTech",
                                                    available_doses=5,
                                                    reserved_doses=3,
                                                    total_doses=8,
                                                    doses_per_patient=2,
                                                    days_between_doses=21,
                                                    cursor=cursor)
                    appt = vrs()
                    cg_schedule_id = vrs.PutHoldOnAppointmentSlot(appt, time.strftime('%Y-%m-%d %H:%M:%S'), 10, 0,
                                                                  cursor)
                    print(cg_schedule_id)
                    if cg_schedule_id > 0:
                        VaccinePatient.ReserveAppointment(sample_patient, cg_schedule_id, sample_vaccine, cursor)
                    else:
                        self.fail("Appointment is not available to reserve.")
                    # check if the patient is correctly inserted into the database
                    vax_query = f'SELECT * FROM VaccineAppointments WHERE PatientId = {sample_patient.patientId}'
                    cursor.execute(vax_query)
                    rows = cursor.fetchall()
                    if len(rows) < 1:
                        self.fail("Reserving first appointment failed")

                    if sample_patient.vax_appt_id_2 < 1:
                        self.fail("Failed to create second appointment")
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Reserving appointment failed")


if __name__ == '__main__':
    unittest.main()
