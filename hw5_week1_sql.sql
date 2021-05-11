--CREATE PROCEDURE initDataModel AS

	-- If tables already exist, drop them	
	IF OBJECT_ID(N'dbo.CareGiverSchedule', N'U') IS NOT NULL  
	   DROP TABLE [dbo].[CareGiverSchedule];  

	IF OBJECT_ID(N'dbo.Appointments', N'U') IS NOT NULL  
	   DROP TABLE [dbo].Appointments;  

	IF OBJECT_ID(N'dbo.PatientDoseHistory', N'U') IS NOT NULL  
	   DROP TABLE [dbo].PatientDoseHistory;  

	IF OBJECT_ID(N'dbo.Vaccines', N'U') IS NOT NULL  
	   DROP TABLE [dbo].Vaccines; 

	IF OBJECT_ID(N'dbo.Caregivers', N'U') IS NOT NULL  
	   DROP TABLE [dbo].[Caregivers];  

	IF OBJECT_ID(N'dbo.AppointmentStatusCodes', N'U') IS NOT NULL  
	   DROP TABLE [dbo].[AppointmentStatusCodes];  

	IF OBJECT_ID(N'dbo.VaccineBrands', N'U') IS NOT NULL  
	   DROP TABLE [dbo].VaccineBrands; 

	IF OBJECT_ID(N'dbo.Patients', N'U') IS NOT NULL  
	   DROP TABLE [dbo].Patients;  

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
		BrandName NVARCHAR(50),
		MinimumAge INT,
		RequiredDoses INT,
		TimeBetweenDoses INT
	);

	CREATE TABLE Patients(
		PatientID INT IDENTITY PRIMARY KEY,
		PantientName NVARCHAR(50),
		PhoneNumber VARCHAR(50),
		EmailAddress VARCHAR(100)
	);

	CREATE TABLE Vaccines(
		VaccineID INT PRIMARY KEY REFERENCES VaccineBrands(VaccineID),
		AvailableDoses INT NOT NULL DEFAULT 0,
		ReservedDoses INT NOT NULL DEFAULT 0
	);

	CREATE TABLE PatientDoseHistory(
		PatientID INT PRIMARY KEY REFERENCES Patients(PatientID),
		VaccineID INT REFERENCES VaccineBrands(VaccineID),
		AdministeredDate DATETIME
	);

	CREATE TABLE Appointments(
		AppointmentID INT IDENTITY PRIMARY KEY,
		PatientID INT REFERENCES Patients(PatientID),
		CaregiverID INT,
		VaccineID INT REFERENCES Vaccines(VaccineID),
		StatusCodeID INT REFERENCES AppointmentStatusCodes(StatusCodeId),
		ApptDay date,
		ApptHour int,
		ApptMinute int 
	);
	
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
		VaccineAppointmentId int DEFAULT 0 NOT NULL
		);

	-- insert starter values into tables
	INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode) VALUES 
		(0, 'Open'), 
		(1, 'OnHold'),
		(2, 'Scheduled'), 
		(3, 'Completed'), 
		(4, 'Missed');

	INSERT INTO VaccineBrands VALUES
		(1, 'Pfizer-BioNTech', 16, 2, 21),
		(2, 'Moderna', 18, 2, 28),
		(3, 'Johnson And Johnson', 18, 1, null);		

	--INSERT INTO Caregivers VALUES 
	--	('Anthony Fauci'), 
	--	('Hippocrates'),
	--	('Jonas Salk')
GO