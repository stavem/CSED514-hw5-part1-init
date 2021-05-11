ALTER PROCEDURE InitDataModel AS

	-- If tables already exist, drop them	
	IF OBJECT_ID(N'dbo.CareGiverSchedule', N'U') IS NOT NULL  
	   DROP TABLE [dbo].[CareGiverSchedule];  

	IF OBJECT_ID(N'dbo.Caregivers', N'U') IS NOT NULL  
	   DROP TABLE [dbo].[Caregivers];  

	IF OBJECT_ID(N'dbo.AppointmentStatusCodes', N'U') IS NOT NULL  
	   DROP TABLE [dbo].[AppointmentStatusCodes];  

	IF OBJECT_ID(N'dbo.VaccineBrands', N'U') IS NOT NULL  
	   DROP TABLE [dbo].VaccineBrands;  

	-- recreate tables
	CREATE TABLE Caregivers(
		CaregiverId int IDENTITY PRIMARY KEY,
		CaregiverName varchar(50)
		);

	CREATE TABLE AppointmentStatusCodes(
		StatusCodeId int PRIMARY KEY,
		StatusCode   varchar(30)
	);
	
	CREATE TABLE VaccineBrands(
	VaccineID INT PRIMARY KEY,
	Brand NVARCHAR(50),
	MinimumAge INT,
	RequiredDoses INT,
	TimeBetweenDoses INT
	)

	CREATE TABLE CareGiverSchedule(
		CaregiverSlotSchedulingId INT IDENTITY PRIMARY KEY, 
		CaregiverId int DEFAULT 0 NOT NULL
			CONSTRAINT FK_CareGiverScheduleCaregiverId FOREIGN KEY (caregiverId)
				REFERENCES Caregivers(CaregiverId),
		WorkDay date,
		SlotTime time,
		SlotHour int DEFAULT 0 NOT NULL,
		SlotMinute int DEFAULT 0 NOT NULL,
		SlotStatus int  DEFAULT 0 NOT NULL
			CONSTRAINT FK_CaregiverStatusCode FOREIGN KEY (SlotStatus) 
				 REFERENCES AppointmentStatusCodes(StatusCodeId),
		VaccineAppointmentId int DEFAULT 0 NOT NULL);

		-- insert starter values into tables
		INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
		VALUES (0, 'Open'), (1, 'OnHold'), (2, 'Scheduled'), (3, 'Completed'), (4, 'Missed');

		INSERT INTO VaccineBrands
		VALUES
		(1, 'Pfizer-BioNTech', 16, 2, 21),
		(2, 'Moderna', 18, 2, 28),
		(3, 'Johnson And Johnson', 18, 1, null);		

		INSERT INTO Caregivers
		VALUES ('Anthony Fauci'), ('Hippocrates'), ('Jonas Salk')
GO