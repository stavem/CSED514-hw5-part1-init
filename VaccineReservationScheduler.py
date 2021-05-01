import datetime
from enum import IntEnum

import VaccineCaregiver as vc
# import COVID19Vaccine as covid
# import VaccinePatient as patient

import pymssql
import traceback


class AppointmentStatus (IntEnum):
    OPEN = 0
    ONHOLD = 1
    SCHEDULED = 2
    COMPLETED = 3
    MISSED = 4


class SqlConnectionManager:
    def __init__(self, Server, UserId, Password, DBname=""):
        '''context manager for the SQL Server connection '''
        self.Server = Server
        self.DBname = DBname
        self.UserId = UserId
        self.Password = Password
        self.SqlConnection = None

    def __enter__(self):
        try:
            if self.DBname == "":
                self.SqlConnection = pymssql.connect(server=self.Server, 
                                    user=self.UserId, 
                                    password=self.Password)
            else:
                self.SqlConnection = pymssql.connect(server=self.Server, 
                                    database=self.DBname, 
                                    user=self.UserId, 
                                    password=self.Password)
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1]) 
        return self.SqlConnection

    def __exit__(self, exctype=None, excinst=None, exctb=None):
        if self.SqlConnection is None:
            pass
        else:
            self.SqlConnection.close()
        if exctype is None:
            print('Program terminated and MS SQL connection closed')
        else:
            print("Exception captured: " + str(exctype))
            callstack = traceback.extract_tb(exctb)
            print(excinst)
            print("stack trace: " + str(callstack))


class VaccineReservationScheduler:

    def __init__(self):
        return

    def PutHoldOnAppointmentSlot(self, cursor):
        ''' Method that reserves a CareGiver appointment slot &
        returns the unique scheduling slotid
        Should return 0 if no slot is available  or -1 if there is a database error'''
        # Note to students: this is a stub that needs to replaced with your code
        self.slotSchedulingId = 0
        self.getAppointmentSQL = "SELECT something..."
        try:
            cursor.execute(self.getAppointmentSQL)
            cursor.connection.commit()
            return self.slotSchedulingId
        
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])           
            print("SQL text that resulted in an Error: " + self.getAppointmentSQL)
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
    # This is the Main driver
    #

    vrs = VaccineReservationScheduler()
    server = 'REDHOOK\\PDB'
    dbname = 'CoronaVirus'  # students probably do not need to specify a DBname 
    userid = 'REDHOOK\\markf'
    password = 'xxxxxxxx'

    with SqlConnectionManager(server, userid, password, dbname) as connMgr:
        # get a cursor from the SQL connection
        dbcursor = connMgr.cursor(as_dict=True)

        # Iniialize the caregivers, patients & vaccine supply
        caregiversList = []
        caregiversList.append(vc.VaccineCaregiver('Carrie Nation', dbcursor))
        caregiversList.append(vc.VaccineCaregiver('Clare Barton', dbcursor))
        caregivers = {}
        for cg in caregiversList:
            cgid = cg.caregiverId
            caregivers[cgid] = cg

        # Add a vaccine and Add doses to inventory of the vaccine
        # Ass patients
        # Schedule the patients
        
        # Test cases done!
