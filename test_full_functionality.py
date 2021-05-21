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

    @staticmethod
    def schedule_appointment(patient, vaccine, day, hour, minute, cursor):

        # check if appt is available
        cg_schedule_id = vrs.PutHoldOnAppointmentSlot(vrs(), day, hour, minute, cursor)

        # make sure there are enough doses of the vaccine to hold the appointment
        vax_available = COVID19Vaccine.check_available_doses(vaccine, cursor)

        if cg_schedule_id == 0:
            print('No available appointments on this day.  Please select a new day.')
            return
        elif vax_available < vaccine.doses_per_patient:
            print('Not enough of this vaccine available.  Please select a new vaccine.')

        # if an appointment is available and enough vaccinations, reserve the appointment.
        else:
            COVID19Vaccine.ReserveDoses(vaccine, vaccine.doses_per_patient, cursor)
            VaccinePatient.ReserveAppointment(patient, cg_schedule_id, vaccine, cursor)

            # after reservation schedule the appointment
            VaccinePatient.ScheduleAppointment(patient, cursor)

            print('Appointment scheduled successfully.')
            print('Appointment 1 (scheduled): ' + str(patient.vax_appt_id_1))
            if vaccine.name in ['Pfizer', 'Moderna']:
                print('Appointment 2 (on-hold): ' + str(patient.vax_appt_id_2))
        return

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
                                    available_doses=4,
                                    reserved_doses=0,
                                    total_doses=4,
                                    doses_per_patient=2,
                                    days_between_doses=21,
                                    cursor=dbcursor)

            moderna = COVID19Vaccine(name="Moderna",
                                     supplier="Moderna",
                                     available_doses=1,
                                     reserved_doses=5,
                                     total_doses=6,
                                     doses_per_patient=2,
                                     days_between_doses=28,
                                     cursor=dbcursor)

            j_and_j = COVID19Vaccine(name="Johnson And Johnson",
                                     supplier="Johnson And Johnson",
                                     available_doses=0,
                                     reserved_doses=0,
                                     total_doses=0,
                                     doses_per_patient=1,
                                     days_between_doses=0,
                                     cursor=dbcursor)

            # Add five new patients
            patient_a = VaccinePatient(name="Karl Stavem", status=0, cursor=dbcursor)
            patient_b = VaccinePatient(name="John Doe", status=0, cursor=dbcursor)
            patient_c = VaccinePatient(name="Jane Doe", status=0, cursor=dbcursor)
            patient_d = VaccinePatient(name="John Wayne", status=0, cursor=dbcursor)
            patient_e = VaccinePatient(name="John Doe Jr", status=0, cursor=dbcursor)

            TestFullFunctionality.schedule_appointment(patient=patient_a,
                                                       vaccine=pfizer,
                                                       day=time.strftime('%Y-%m-%d %H:%M:%S'),
                                                       hour=10,
                                                       minute=0,
                                                       cursor=dbcursor)

            # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
