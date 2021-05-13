import pymssql


class COVID19Vaccine:
    def __init__(self, name, supplier, available_doses, reserved_doses, total_doses,
                 doses_per_patient, days_between_doses, cursor):
        self.sqltext = f"INSERT INTO Vaccines (VaccineName, VaccineSupplier, AvailableDoses, ReservedDoses," \
                       f"TotalDoses, DosesPerPatient, DaysBetweenDoses) VALUES ('{name}', '{supplier}'," \
                       f"{available_doses}, {reserved_doses}, {total_doses}, {doses_per_patient}," \
                       f"{days_between_doses})"

        try:
            cursor.execute(self.sqltext)
            cursor.connection.commit()
            print('Query executed successfully. Vaccine : ' + name + ' added to the database.')
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Vaccines! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + self.sqltext)
    pass

def AddDoses(vaccine_name, doses, cursor):
    sql_text = f"UPDATE Vaccines SET TotalDoses = TotalDoses + {doses}," \
    f"AvailableDoses = AvailableDoses + {doses} " \
    f"WHERE VaccineName = '{vaccine_name}'"

    try:
        cursor.execute(sql_text)
        cursor.connection.commit()
        print(f"Query executed successfully. {doses} available doses added to {vaccine_name} vaccine.")
    except pymssql.Error as db_err:
        print("Database Programming Error in SQL Query processing for Vaccines! ")
        print("Exception code: " + str(db_err.args[0]))
        if len(db_err.args) > 1:
            print("Exception message: " + db_err.args[1])
        print("SQL text that resulted in an Error: " + sql_text)
    return
# def ReserveDoses():
#     return
