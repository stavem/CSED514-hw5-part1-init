import unittest
from sql_connection_manager import SqlConnectionManager
from vaccine_patient import VaccinePatient
from COVID19_vaccine import COVID19Vaccine
from vaccine_caregiver import VaccineCaregiver
from vaccine_reservation_scheduler import VaccineReservationScheduler as vrs
import time
from utils import *
import os


class TestFullFunctionality(unittest.TestCase):
    def test_full_scope(self):
        """This unit test performs all actions outlined in the homework:
        * Allocates two caregivers
        * Adds three vaccines
        * Creates and schedules 5 patients, only two of which have vaccines supplied"""
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            clear_tables(sqlClient)
            # get a cursor from the SQL connection
            dbcursor = sqlClient.cursor(as_dict=True)

            # Iniialize the caregivers
            caregiversList = []
            caregiversList.append(VaccineCaregiver('Anthony Fauci', dbcursor))
            caregiversList.append(VaccineCaregiver('Jonas Salk', dbcursor))
            caregivers = {}
            for cg in caregiversList:
                cgid = cg.caregiverId
                caregivers[cgid] = cg

            # Add vaccine and Add doses to inventory of the vaccine
            pfizer = COVID19Vaccine(name="Pfizer",
                                    supplier="Pfizer-BioNTech",
                                    available_doses=5,
                                    reserved_doses=3,
                                    total_doses=8,
                                    doses_per_patient=2,
                                    days_between_doses=21,
                                    cursor=dbcursor)

            moderna = COVID19Vaccine(name="Moderna",
                                     supplier="Moderna",
                                     available_doses=10,
                                     reserved_doses=2,
                                     total_doses=12,
                                     doses_per_patient=2,
                                     days_between_doses=28,
                                     cursor=dbcursor)

            j_and_j = COVID19Vaccine(name="Johnson And Johnson",
                                     supplier="Johnson And Johnson",
                                     available_doses=10,
                                     reserved_doses=4,
                                     total_doses=14,
                                     doses_per_patient=1,
                                     days_between_doses=0,
                                     cursor=dbcursor)

            # Add five new patients
            patient_a = VaccinePatient(name="Karl Stavem", status=0, cursor=dbcursor)
            patient_b = VaccinePatient(name="John Doe", status=0, cursor=dbcursor)
            patient_c = VaccinePatient(name="Jane Doe", status=0, cursor=dbcursor)
            patient_d = VaccinePatient(name="John Wayne", status=0, cursor=dbcursor)
            patient_e = VaccinePatient(name="John Doe Jr", status=0, cursor=dbcursor)

            # check appointment and reserve one

            cg_schedule_id = vrs.PutHoldOnAppointmentSlot(vrs(), time.strftime('%Y-%m-%d %H:%M:%S'), 10, 0, dbcursor)
            print(cg_schedule_id)
            if cg_schedule_id > 0:
                VaccinePatient.ReserveAppointment(patient_b, cg_schedule_id, moderna, dbcursor)
                COVID19Vaccine.ReserveDoses(moderna, moderna.doses_per_patient, dbcursor)
            else:
                print('No available appointments during this time.  Please select a new time')

                # Schedule the patients
            VaccinePatient.ScheduleAppointment(patient_b, dbcursor)

            # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
