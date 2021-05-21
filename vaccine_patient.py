from datetime import datetime
from datetime import timedelta
import pymssql


# from vaccine_reservation_scheduler import VaccineReservationScheduler


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

        sql_reserve = """BEGIN TRAN reserveappt
                        DECLARE @status INT
                       
                        
                        -- Confirm the slot status is 0
                        SET @status = (SELECT SlotStatus FROM CareGiverSchedule 
                        WHERE CaregiverSlotSchedulingId = {cg_id})	
                        
                        
                        -- CREATE INITIAL ENTRY INTO VaccineAppt Table AND FLAG PATIENT as queued for 1 dose
                        IF (@status = 1) 
                            BEGIN
                            INSERT INTO [dbo].[VaccineAppointments] 
                            ([VaccineName],[PatientId],[CaregiverId],[ReservationDate],
                            [ReservationStartHour],[ReservationStartMinute],[AppointmentDuration],
                            [SlotStatus],[DoseNumber]) 
                            SELECT
                            '{vaccine_name}',
                            {patientid}, 
                            CaregiverId,
                            WorkDay, 
                            SlotHour, 
                            SlotMinute, 
                            15, 
                            1, 
                            1
                            FROM
                            CareGiverSchedule
                            WHERE CaregiverSlotSchedulingId = {cg_id}
                            UPDATE Patients SET VaccineStatus = 1 WHERE PatientId = {patientid}
                            COMMIT TRAN reserveappt
                            END
                        ELSE
                            BEGIN
                            ROLLBACK TRAN reserveappt
                            END
        """.format(cg_id=caregiver_scheduling_id,
                   vaccine_name=vaccine.name,
                   patientid=self.patientId)

        try:
            cursor.execute(sql_reserve)
            cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
            _identityRow = cursor.fetchone()
            self.vax_appt_id_1 = _identityRow['Identity']
            print(self.vax_appt_id_1)
            cursor.connection.commit()
            print('added to the vaccine appts.')

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Patients! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + sql_reserve)

        sql_next_appt = """BEGIN TRAN nextappt
                            
                            DECLARE @apptid  INT = (SELECT TOP 1 CaregiverSlotSchedulingId 
                                                    FROM CareGiverSchedule 
                                                    WHERE WorkDay >= DATEADD(DAY, {days}, '2021-05-19')
                                                    AND SlotStatus = 0)
                                                    
                            UPDATE CareGiverSchedule SET SlotStatus = 1 WHERE CaregiverSlotSchedulingId = @apptid
                            
                            INSERT INTO [dbo].[VaccineAppointments] 
                            ([VaccineName],[PatientId],[CaregiverId],[ReservationDate],
                            [ReservationStartHour],[ReservationStartMinute],[AppointmentDuration],
                            [SlotStatus],[DoseNumber]) 
                            SELECT 
                            '{vaccine_name}', 
                            {patient_id}, 
                            CaregiverId, 
                            WorkDay, 
                            SlotHour, 
                            SlotMinute,
                            15,
                            SlotStatus,
                            2
                            FROM CareGiverSchedule 
                            WHERE CaregiverSlotSchedulingId = @apptid
                            
                            COMMIT TRAN nextappt""".format(vaccine_name=vaccine.name,
                                                           days=vaccine.days_between_doses,
                                                           patient_id=self.patientId)
        if vaccine.doses_per_patient > 1:
            try:
                cursor.execute(sql_next_appt)
                cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
                _identityRow = cursor.fetchone()
                self.vax_appt_id_2 = _identityRow['Identity']
                print(self.vax_appt_id_1)
                cursor.connection.commit()
                print('added to the vaccine appts.')

            except pymssql.Error as db_err:
                print("Database Programming Error in SQL Query processing for Patients! ")
                print("Exception code: " + str(db_err.args[0]))
                if len(db_err.args) > 1:
                    print("Exception message: " + db_err.args[1])
                print("SQL text that resulted in an Error: " + sql_next_appt)
        return

    def ScheduleAppointment(self, cursor):
        """mark the appointment as scheduled
        update the patient vaccine status
        maintain the vaccine inventory
        and any other scheduling actions for the caregiver to administer the vaccine doses to the patient"""

        sql_text = """ BEGIN TRAN schedule_appt
                    
                        UPDATE VaccineAppointments
                            SET SlotStatus = 2
                            WHERE VaccineAppointmentId = {vax_appt_id}
    
    
                        UPDATE Patients
                            SET VaccineStatus = 2
                            WHERE PatientId = {patientId}

                    COMMIT TRAN schedule_appt""".format(vax_appt_id=self.vax_appt_id_1,
                                                        patientId=self.patientId)
        try:
            cursor.execute(sql_text)
            cursor.connection.commit()
            print('Scheduled the vaccine appts.')

        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Patients! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + sql_text)
        return
