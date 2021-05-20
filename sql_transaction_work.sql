BEGIN TRAN reserveappt
                        DECLARE @status INT
                        
                        -- Confirm the slot status is 0
                        SET @status = (SELECT SlotStatus FROM CareGiverSchedule 
                        WHERE CaregiverSlotSchedulingId = 2)	
                        
                        -- CREATE INITIAL ENTRY INTO VaccineAppt Table AND FLAG PATIENT as queued for 1 dose
                        IF (@status = 1) 
                            BEGIN
INSERT INTO [dbo].[VaccineAppointments] 
([VaccineName],[PatientId],[CaregiverId],[ReservationDate],
[ReservationStartHour],[ReservationStartMinute],[AppointmentDuration],
[SlotStatus],[DoseNumber]) 
SELECT
'Pfizer',
1, 
CaregiverId,
WorkDay, 
SlotHour, 
SlotMinute, 
15, 
1, 
1
FROM
CareGiverSchedule
WHERE CaregiverSlotSchedulingId = 2
                            UPDATE Patients SET VaccineStatus = 1 WHERE PatientId = 2
                            COMMIT TRAN reserveappt
                            END
                        ELSE
                            BEGIN
                            ROLLBACK TRAN reserveappt
                            END

BEGIN TRAN nextappt

	DECLARE @apptid  INT = (SELECT TOP 1 CaregiverSlotSchedulingId 
							FROM CareGiverSchedule 
							WHERE WorkDay >= DATEADD(DAY, 21, '2021-05-19')
							AND SlotStatus = 0)

	UPDATE CareGiverSchedule SET SlotStatus = 1 WHERE CaregiverSlotSchedulingId = @apptid

	INSERT INTO [dbo].[VaccineAppointments] 
		([VaccineName],[PatientId],[CaregiverId],[ReservationDate],
		[ReservationStartHour],[ReservationStartMinute],[AppointmentDuration],
		[SlotStatus],[DoseNumber]) 
		SELECT 
		'pfizer', 
		1, 
		CaregiverId, 
		WorkDay, 
		SlotHour, 
		SlotMinute,
		15,
		SlotStatus,
		2
		FROM CareGiverSchedule 
		WHERE CaregiverSlotSchedulingId = @apptid

COMMIT TRAN nextappt



	-- find next available appt

	
	-- Confirm the slot status is 0
	SET @status = (SELECT SlotStatus FROM CareGiverSchedule WHERE CaregiverSlotSchedulingId = 2)	
	
	-- CREATE INITIAL ENTRY INTO VaccineAppt Table AND FLAG PATIENT as queued for 1 dose
	IF (@status = 0) 
		BEGIN
		INSERT INTO [dbo].[VaccineAppointments] 
		([VaccineName],[PatientId],[CaregiverId],[ReservationDate],
		[ReservationStartHour],[ReservationStartMinute],[AppointmentDuration],
		[SlotStatus],[DateAdministered],[DoseNumber]) 
		VALUES 
		('pfizer',1, 2,'2021-05-18', 10, 0, 15, 3, '2021-05-18', 1)
		UPDATE Patients SET VaccineStatus = 1 WHERE PatientId = 1
		COMMIT TRAN reserveappt
		END
	ELSE
		BEGIN
		ROLLBACK TRAN reserveappt
		END


SELECT * FROM VaccineAppointments


