def clear_tables(client):
    sqlQuery = '''
               DELETE FROM VaccineAppointments
               DBCC CHECKIDENT ('VaccineAppointments', RESEED, 0)
               Truncate Table CareGiverSchedule
               DBCC CHECKIDENT ('CareGiverSchedule', RESEED, 1)
               Delete From Caregivers
               DBCC CHECKIDENT ('Caregivers', RESEED, 0)
               TRUNCATE TABLE Vaccines
               DELETE FROM Patients
               DBCC CHECKIDENT ('Patients', RESEED, 0)
               
               '''
    client.cursor().execute(sqlQuery)
    client.commit()
