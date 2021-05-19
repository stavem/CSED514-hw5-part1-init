from datetime import datetime
from datetime import timedelta
import pymssql


class VaccinePatient:
    ''' Adds the CareGiver to the DB and adds vaccine scheduling slots '''
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
