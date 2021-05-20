

BEGIN TRAN reserveappt
	DECLARE @rc_patient INT
	DECLARE @status INT
	
	-- Confirm the slot status is 0
	SET @status = (SELECT SlotStatus FROM CareGiverSchedule WHERE CaregiverSlotSchedulingId = 2)	

	-- FLAG PATIENT AS queued for 1 dose
	SELECT * FROM VaccineAppointments WHERE PatientId = 1 AND VaccineName = 'pfizer'
	SET @rc_patient = @@ROWCOUNT
	SELECT @rc_patient
	
	-- CREATE INITIAL ENTRY INTO VaccineAppt Table AND FLAG PATIENT as queued for 1 dose
	IF (@status = 0 AND @rc_patient > 0) 
		begin
		INSERT INTO [dbo].[VaccineAppointments] 
		([VaccineName],[PatientId],[CaregiverId],[ReservationDate],
		[ReservationStartHour],[ReservationStartMinute],[AppointmentDuration],
		[SlotStatus],[DateAdministered],[DoseNumber]) 
		VALUES 
		('pfizer',1, 2,'2021-05-18', 10, 0, 15, 3, '2021-05-18', 1)
		UPDATE Patients SET VaccineStatus = 1 WHERE PatientId = 1
		COMMIT TRAN reserveappt
		end
	ELSE
		BEGIN
		ROLLBACK TRAN reserveappt
		END



SELECT * FROM VaccineAppointments




	-- Create a a second appt 3-6 weeks after first appt  (retain both primary keys vaccineappointment slot ids)
	SELECT TOP 1 * FROM CareGiverSchedule WHERE WorkDay > DATEADD(DAY, 21, '2021-05-18') AND SlotStatus = 0 ORDER BY CaregiverSlotSchedulingId ASC
	SET @rc = @@ROWCOUNT

	IF @rc <> 1 OR
	ELSE
		UPDATE CareGiverSchedule
		SET SlotStatus = 2
		WHERE
		CaregiverSlotSchedulingId = (SELECT TOP 1 CaregiverSlotSchedulingId FROM CareGiverSchedule WHERE WorkDay > DATEADD(DAY, 21, '2021-05-18') AND SlotStatus = 0 ORDER BY CaregiverSlotSchedulingId ASC)

		INSERT INTO [dbo].[VaccineAppointments] 
		([VaccineName],[PatientId],[CaregiverId],[ReservationDate],
		[ReservationStartHour],[ReservationStartMinute],[AppointmentDuration],
		[SlotStatus],[DateAdministered],[DoseNumber]) 
		VALUES 
		('pfizer',1, 2,'2021-05-21', 10, 0, 15, 3, '2021-05-18', 1) 
		COMMIT TRAN reserveappt


