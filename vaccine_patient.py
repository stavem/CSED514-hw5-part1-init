from datetime import datetime
from datetime import timedelta
import pymssql
from vaccine_reservation_scheduler import VaccineReservationScheduler


class VaccinePatient:
    ''' Adds patient to the db '''
    def __init__(self, name, status, cursor):
        self.sql_text = f"INSERT INTO Patients (PatientName, VaccineStatus) VALUES ('{name}', {status})"
        self.patientId = 0
        try:
            cursor.execute(self.sql_text)
            cursor.connection.commit()
            cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
            _identityRow = cursor.fetchone()
            self.patientId = _identityRow['Identity']
            # cursor.connection.commit()
            print('Query executed successfully. Patient : ' + name
                  + ' added to the database using Patient ID = ' + str(self.patientId))
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Patients! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + self.sql_text)

    def ReserveAppointment(self, caregiver_scheduling_id, vaccine, cursor):
        """Reserve an appointment
        validate the caregiver schedule slot id parm,
        create an initial entry in the vaccine appointment table
        flag the patient as queued for 1st dose
        then create a second appoint 3-6 weeks after the 1st appt
        be sure to retain the the identitys from the two vaccineappts reserved
        """

        # check status
        update_sql = f'UPDATE CareGiverSchedule ' \
                     f'SET SlotStatus = 1 WHERE CaregiverSlotSchedulingId = {caregiver_scheduling_id}'

        try:
            cursor.execute(f"SELECT SlotStatus FROM [CareGiverSchedule] WHERE CaregiverSlotSchedulingId = {caregiver_scheduling_id}")

            if len(cursor.fetchall()) < 1:
                print('Invalid scheduling id')
                return

            results_row = cursor.fetchone()
            slot_status = results_row['SlotStatus']

            if slot_status != 0:
                print('Appointment Unavailable')
                return

            cursor.execute(update_sql)
            cursor.connection.commit()
            print('Query executed successfully.')
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Caregivers! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])

        # sql
        print('you made it here')

