from COVID19_vaccine import COVID19Vaccine
import os
from sql_connection_manager import SqlConnectionManager
from vaccine_patient import VaccinePatient

with SqlConnectionManager(Server=os.getenv("Server"),
                          DBname=os.getenv("DBName"),
                          UserId=os.getenv("UserID"),
                          Password=os.getenv("Password")) as sqlClient:
    with sqlClient.cursor(as_dict=True) as cursor:

        vaccine_a = COVID19Vaccine(name="Pfizer5",
                                        supplier="Pfizer-BioNTech",
                                        available_doses=1,
                                        reserved_doses=3,
                                        total_doses=4,
                                        doses_per_patient=2,
                                        days_between_doses=21,
                                        cursor=cursor)

        # patient_a = VaccinePatient(name="Karl Stavem",
        #                            status=0,
        #                            cursor=cursor)
        COVID19Vaccine.AddDoses(vaccine_a, vaccine_a.name, 21, cursor)
        # print(patient_a.patientId)
        # VaccinePatient.ReserveAppointment(patient_a.patientId, 2, vaccine_a, cursor)