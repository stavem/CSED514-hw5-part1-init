import datetime
from enum import IntEnum
import os
import pymssql
import traceback

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from COVID19_vaccine import COVID19Vaccine
from vaccine_patient import VaccinePatient


# from vaccine_patient import VaccinePatient as patient


class VaccineReservationScheduler:

    def __init__(self):
        return

    def PutHoldOnAppointmentSlot(self, caregiver_id, work_day, slot_hour, slot_minute, cursor):
        ''' Method that reserves a CareGiver appointment slot &
        returns the unique scheduling slotid
        Should return 0 if no slot is available  or -1 if there is a database error'''
        # Note to students: this is a stub that needs to replaced with your code
        self.slotSchedulingId = 0

        getAppointmentSQL = f"SELECT CaregiverSlotSchedulingId FROM CareGiverSchedule " \
                            f"WHERE " \
                            f"SlotStatus = 0 " \
                            f"AND CaregiverId = {caregiver_id} " \
                            f"AND WorkDay = '{work_day}' " \
                            f"AND SlotHour = {slot_hour} " \
                            f"AND SlotMinute = {slot_minute} "
        try:
            cursor.execute(getAppointmentSQL)
            results = cursor.fetchall()
            if len(results) > 0:
                self.slotSchedulingId = results[0]['CaregiverSlotSchedulingId']
                cursor.execute("""UPDATE CareGiverSchedule SET SlotStatus = 1 
                                WHERE CaregiverSlotSchedulingId = {slotSchedulingId}""".format(
                    slotSchedulingId=self.slotSchedulingId))
            cursor.connection.commit()
            return self.slotSchedulingId

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + getAppointmentSQL)
            cursor.connection.rollback()
            return -1

    def ScheduleAppointmentSlot(self, slotid, cursor):
        '''method that marks a slot on Hold with a definite reservation  
        slotid is the slot that is currently on Hold and whose status will be updated 
        returns the same slotid when the database update succeeds 
        returns 0 is there if the database update dails 
        returns -1 the same slotid when the database command fails
        returns 21 if the slotid parm is invalid '''
        # Note to students: this is a stub that needs to replaced with your code
        if slotid < 1:
            return -2
        self.slotSchedulingId = slotid
        self.getAppointmentSQL = "SELECT something... "
        try:
            cursor.execute(self.getAppointmentSQL)
            return self.slotSchedulingId
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + db_err.args[0])
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))
            print("SQL text that resulted in an Error: " + self.getAppointmentSQL)
            return -1


if __name__ == '__main__':
    with SqlConnectionManager(Server=os.getenv("Server"),
                              DBname=os.getenv("DBName"),
                              UserId=os.getenv("UserID"),
                              Password=os.getenv("Password")) as sqlClient:
        clear_tables(sqlClient)
        vrs = VaccineReservationScheduler()

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

        # Add patients
        patient_a = VaccinePatient(name="Karl Stavem",
                                   status=0,
                                   cursor=dbcursor)

        patient_b = VaccinePatient(name="John Doe",
                                   status=0,
                                   cursor=dbcursor)

        patient_c = VaccinePatient(name="Jane Doe",
                                   status=0,
                                   cursor=dbcursor)

        patient_d = VaccinePatient(name="John Wayne",
                                   status=0,
                                   cursor=dbcursor)

        patient_e = VaccinePatient(name="John Doe Jr",
                                   status=0,
                                   cursor=dbcursor)

        # check appointment and reserve
        cg_schedule_id = vrs.PutHoldOnAppointmentSlot(1, '2021-05-19', 10, 30, dbcursor)
        print(cg_schedule_id)
        if cg_schedule_id > 0:
            VaccinePatient.ReserveAppointment(patient_b, cg_schedule_id, pfizer, dbcursor)
            COVID19Vaccine.ReserveDoses(j_and_j, j_and_j.doses_per_patient, dbcursor)

        # Schedule the patients
        # patient_e.ReserveAppointment(caregiver_scheduling_id=5, vaccine=pfizer, cursor=dbcursor)

        # Test cases done!
        # clear_tables(sqlClient)
