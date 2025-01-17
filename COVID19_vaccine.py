import pymssql



class COVID19Vaccine:
    def __init__(self, name, supplier, available_doses, reserved_doses, total_doses,
                 doses_per_patient, days_between_doses, cursor):
        self.name = name
        self.doses_per_patient = doses_per_patient
        self.days_between_doses = days_between_doses
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

    def AddDoses(self, doses, cursor):
        """Increase the number of available vaccines doses."""
        sql_text = f"UPDATE Vaccines SET TotalDoses = TotalDoses + {doses}," \
        f"AvailableDoses = AvailableDoses + {doses} " \
        f"WHERE VaccineName = '{self.name}'"

        try:
            cursor.execute(sql_text)
            cursor.connection.commit()
            print(f"Query executed successfully. {doses} available doses added to {self.name} vaccine.")
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Vaccines! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + sql_text)
        return

    def check_available_doses(self, cursor):
        """Verify that enough available doses are present in the db."""
        sql_query = f"SELECT AvailableDoses FROM Vaccines WHERE VaccineName = '{self.name}'"

        try:
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            return rows[0]['AvailableDoses']
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Vaccines! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + sql_query)
        return

    def ReserveDoses(self, doses, cursor):
        """Move doses from available to reserved."""
        if COVID19Vaccine.check_available_doses(self, cursor) < doses:
            print('Not enough doses available to reserve!')
            return -1
        elif doses < 1:
            print('Number of doses must be greater than zero.')
        else:
            sql_update = f"UPDATE Vaccines SET ReservedDoses = ReservedDoses + {doses}," \
                       f"AvailableDoses = AvailableDoses - {doses} " \
                       f"WHERE VaccineName = '{self.name}'"
            try:
                cursor.execute(sql_update)
                cursor.connection.commit()
                print(f"Query executed successfully. {doses} dose(s) of the {self.name} vaccine have been reserved.")
            except pymssql.Error as db_err:
                print("Database Programming Error in SQL Query processing for Vaccines! ")
                print("Exception code: " + str(db_err.args[0]))
                if len(db_err.args) > 1:
                    print("Exception message: " + db_err.args[1])
                print("SQL text that resulted in an Error: " + sql_update)
            return