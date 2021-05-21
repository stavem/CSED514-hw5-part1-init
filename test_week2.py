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

        # check if appointment is available
        cg_schedule_id = vrs.PutHoldOnAppointmentSlot(vrs(), day, hour, minute, cursor)

        # make sure there are enough doses of the vaccine to hold the appointment
        vax_available = COVID19Vaccine.check_available_doses(vaccine, cursor)

        if cg_schedule_id == 0:
            print('No available appointments on this day.  Please select a new day.')
            return -1
        elif vax_available < vaccine.doses_per_patient:
            print('Not enough of this vaccine available.  Please select a new vaccine.')
            return -1

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
            return 1

    def test_full_scope(self):
        """This unit test performs all actions outlined in the homework:
        * Allocates two caregivers
        * Adds three vaccines
        * Creates and schedules 5 patients, only two of which succeed."""
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            clear_tables(sqlClient)

            # get a cursor from the SQL connection
            dbcursor = sqlClient.cursor(as_dict=True)

            # Initialize the caregivers
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

            tff = TestFullFunctionality()
            # test successfully scheduling a patient today
            appointment_1 = tff.schedule_appointment(patient=patient_a,
                                                     vaccine=pfizer,
                                                     day=time.strftime('%Y-%m-%d %H:%M:%S'),
                                                     hour=10,
                                                     minute=0,
                                                     cursor=dbcursor)

            # test successfully scheduling a patient for the same time window today
            appointment_2 = tff.schedule_appointment(patient=patient_b,
                                                     vaccine=pfizer,
                                                     day=time.strftime('%Y-%m-%d %H:%M:%S'),
                                                     hour=10,
                                                     minute=0,
                                                     cursor=dbcursor)

            # test unsuccessfully scheduling a patient for the same time window today
            # no available caregivers
            appointment_3 = tff.schedule_appointment(patient=patient_c,
                                                     vaccine=pfizer,
                                                     day=time.strftime('%Y-%m-%d %H:%M:%S'),
                                                     hour=10,
                                                     minute=0,
                                                     cursor=dbcursor)

            # test unsuccessfully scheduling a patient today
            # not enough moderna vaccine available
            appointment_4 = tff.schedule_appointment(patient=patient_d,
                                                     vaccine=moderna,
                                                     day=time.strftime('%Y-%m-%d %H:%M:%S'),
                                                     hour=10,
                                                     minute=15,
                                                     cursor=dbcursor)

            # test unsuccessfully scheduling a patient today
            # not enough J&J vaccine available
            appointment_5 = tff.schedule_appointment(patient=patient_e,
                                                     vaccine=j_and_j,
                                                     day=time.strftime('%Y-%m-%d %H:%M:%S'),
                                                     hour=10,
                                                     minute=30,
                                                     cursor=dbcursor)

            self.assertEqual(appointment_1, 1)  # valid appointment should pass
            self.assertEqual(appointment_2, 1)  # same time slot, different caregiver should pass
            self.assertEqual(appointment_3, -1)  # no caregivers available during timeslot
            self.assertEqual(appointment_4, -1)  # not enough moderna vaccine available
            self.assertEqual(appointment_5, -1)  # not enough j&j vaccine available


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

    def test_schedule_appointment(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
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
                    VaccinePatient.ReserveAppointment(sample_patient, cg_schedule_id, sample_vaccine, cursor)
                    VaccinePatient.ScheduleAppointment(sample_patient, cursor)

                    # check if the patient is correctly inserted into the database
                    vax_query = f'SELECT TOP 1 SlotStatus FROM VaccineAppointments WHERE PatientId = {sample_patient.patientId} ORDER BY ReservationDate'
                    cursor.execute(vax_query)
                    rows = cursor.fetchall()
                    if len(rows) < 1:
                        self.fail("No Appointment Available To Schedule")
                    elif rows[0]['SlotStatus'] != 2:
                        self.fail("Failed to set the appointment status to scheduled.")

                    pat_query = f'SELECT VaccineStatus FROM Patients WHERE PatientId = {sample_patient.patientId}'
                    cursor.execute(pat_query)
                    rows = cursor.fetchall()

                    if len(rows) < 1:
                        self.fail("No Patient Available To Schedule")
                    elif rows[0]['VaccineStatus'] != 2:
                        self.fail("Failed to set the vaccine status to queued.")

                except Exception:
                    # clear the tables if an exception occurred
                    # clear_tables(sqlClient)
                    self.fail("scheduling the appointment failed")


if __name__ == '__main__':
    unittest.main()
