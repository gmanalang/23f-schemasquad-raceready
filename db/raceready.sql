CREATE DATABASE RaceReady;
SHOW DATABASES;
USE RaceReady;


CREATE USER 'race_ready'@'%' IDENTIFIED BY 'temp_password';
GRANT ALL PRIVILEGES ON RaceReady.* TO 'race_ready'@'%';


CREATE TABLE Runner
(
   runnerID       INT AUTO_INCREMENT,
   firstName      varchar(30)             NOT NULL,
   lastName       varchar(30)             NOT NULL,
   gender         ENUM ('Male', 'Female', 'Other') NOT NULL,
   age            INT                     NOT NULL,
   email          varchar(50)             NOT NULL,
   phone          varchar(15)             NOT NULL,
   street         varchar(50)             NOT NULL,
   city           varchar(50)             NOT NULL,
   state          varchar(50)             NOT NULL,
   country        varchar(50)             NOT NULL,
   zip            varchar(10)             NOT NULL,
   CONSTRAINT PRIMARY KEY (runnerID)
);


CREATE TABLE Volunteer
(
   volunteerID INT AUTO_INCREMENT,
   firstName   varchar(30) NOT NULL,
   lastName    varchar(30) NOT NULL,
   age         INT         NOT NULL,
   email       varchar(50) NOT NULL,
   phone       varchar(15) NOT NULL,
   street      varchar(50) NOT NULL,
   city        varchar(50) NOT NULL,
   state       varchar(50) NOT NULL,
   country     varchar(50) NOT NULL,
   zip         varchar(10) NOT NULL,
   CONSTRAINT PRIMARY KEY (volunteerID)
);


CREATE TABLE EventOrganizer
(
   organizerID INT AUTO_INCREMENT,
   name        varchar(50) NOT NULL UNIQUE,
   email       varchar(50) NOT NULL UNIQUE,
   phone       varchar(15) NOT NULL UNIQUE,
   CONSTRAINT PRIMARY KEY (organizerID)
);


CREATE TABLE Sponsor
(
   sponsorID   INT AUTO_INCREMENT,
   name        varchar(50) NOT NULL UNIQUE,
   email       varchar(50) NOT NULL UNIQUE,
   phone       varchar(15) NOT NULL UNIQUE,
   companyType varchar(50) NOT NULL,
   CONSTRAINT PRIMARY KEY (sponsorID)
);


CREATE TABLE Vendor
(
   vendorID   INT AUTO_INCREMENT,
   name       varchar(50) NOT NULL UNIQUE,
   email      varchar(50) NOT NULL UNIQUE,
   phone      varchar(15) NOT NULL UNIQUE,
   vendorType varchar(50) NOT NULL,
   CONSTRAINT PRIMARY KEY (vendorID)
);


CREATE TABLE Police
(
   policeID INT AUTO_INCREMENT,
   name     varchar(50) NOT NULL UNIQUE,
   email    varchar(50) NOT NULL UNIQUE,
   phone    varchar(15) NOT NULL UNIQUE,
   street   varchar(50) NOT NULL,
   city     varchar(50) NOT NULL,
   state    varchar(50) NOT NULL,
   country  varchar(50) NOT NULL,
   zip      varchar(10) NOT NULL,
   CONSTRAINT PRIMARY KEY (policeID)
);

CREATE TABLE Race
(
   raceID      INT AUTO_INCREMENT,
   street      varchar(50)  NOT NULL,
   city        varchar(50)  NOT NULL,
   state       varchar(50)  NOT NULL,
   country     varchar(50)  NOT NULL,
   zip         varchar(10)  NOT NULL,
   date        DATETIME     NOT NULL,
   terrainType varchar(150) NOT NULL,
   raceLength  DEC(3,1)   NOT NULL,
   maxRunners  INT          NOT NULL,
   checkInTime DATETIME     NOT NULL,
   organizerID INT          NOT NULL,
   CONSTRAINT PRIMARY KEY (raceID),
   CONSTRAINT FOREIGN KEY (organizerID) REFERENCES EventOrganizer (organizerID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE RefuelStation
(
   stationID INT,
   venueSpot varchar(50)  NOT NULL,
   amenities varchar(150) NOT NULL,
   raceID    INT          NOT NULL,
   CONSTRAINT PRIMARY KEY (stationID, raceID),
   CONSTRAINT FOREIGN KEY (raceID) REFERENCES Race (raceID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE FirstAidStation
(
   stationID INT,
   venueSpot varchar(50)  NOT NULL,
   services  varchar(150) NOT NULL,
   raceID    INT          NOT NULL,
   CONSTRAINT PRIMARY KEY (stationID, raceID),
   CONSTRAINT FOREIGN KEY (raceID) REFERENCES Race (raceID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE SponsorStation
(
   stationID   INT,
   venueSpot   varchar(50) NOT NULL,
   sponsorName varchar(50) NOT NULL,
   raceID      INT         NOT NULL,
   sponsorID   INT         NOT NULL,
   CONSTRAINT PRIMARY KEY (stationID, raceID, sponsorID),
   CONSTRAINT FOREIGN KEY (raceID) REFERENCES Race (raceID)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT FOREIGN KEY (sponsorID) REFERENCES Sponsor (sponsorID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE BillingInfo
(
   cardNumber         BIGINT,
   cardExpirationDate DATE        NOT NULL,
   cardSecurityCode   INT         NOT NULL,
   billingStreet      varchar(50) NOT NULL,
   billingCity        varchar(50) NOT NULL,
   billingState       varchar(50) NOT NULL,
   billingCountry     varchar(50) NOT NULL,
   billingZip         varchar(10) NOT NULL,
   runnerID           INT         NOT NULL,
   CONSTRAINT PRIMARY KEY (cardNumber, runnerID),
   CONSTRAINT FOREIGN KEY (runnerID) REFERENCES Runner (runnerID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE RaceResults
(
   runnerID    INT,
   bibNumber   INT,
   finishTime  TIME,
   raceID      INT,
   organizerID INT,
   CONSTRAINT PRIMARY KEY (raceID, organizerID, bibNumber, runnerID),
   CONSTRAINT FOREIGN KEY (raceID) REFERENCES Race (raceID)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT FOREIGN KEY (organizerID) REFERENCES EventOrganizer (organizerID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE MileSplits
(
   runnerID    INT,
   bibNumber   INT,
   raceID      INT,
   organizerID INT,
   marker      varchar(15),
   mileSplit   TIME,
   CONSTRAINT PRIMARY KEY (raceID, organizerID, bibNumber, runnerID, marker, mileSplit),
   CONSTRAINT FOREIGN KEY (raceID, organizerID, bibNumber, runnerID)
       REFERENCES RaceResults (raceID, organizerID, bibNumber, runnerID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE Runner_RunsIn_Race
(
   runnerID INT,
   raceID   INT,
   CONSTRAINT PRIMARY KEY (runnerID, raceID),
   CONSTRAINT FOREIGN KEY (runnerID) REFERENCES Runner (runnerID)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT FOREIGN KEY (raceID) REFERENCES Race (raceID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE Runner_ChecksInto_Race
(
   runnerID   INT,
   raceID     INT,
   bib_number INT NOT NULL,
   CONSTRAINT PRIMARY KEY (runnerID, raceID),
   CONSTRAINT FOREIGN KEY (runnerID) REFERENCES Runner (runnerID)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT FOREIGN KEY (raceID) REFERENCES Race (raceID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE Runner_RegistersFor_Race
(
   runnerID INT,
   raceID   INT,
   CONSTRAINT PRIMARY KEY (runnerID, raceID),
   CONSTRAINT FOREIGN KEY (runnerID) REFERENCES Runner (runnerID)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT FOREIGN KEY (raceID) REFERENCES Race (raceID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE Volunteer_ChecksInto_Race
(
   volunteerID INT,
   raceID      INT,
   CONSTRAINT PRIMARY KEY (volunteerID, raceID),
   CONSTRAINT FOREIGN KEY (volunteerID) REFERENCES Volunteer (volunteerID)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT FOREIGN KEY (raceID) REFERENCES Race (raceID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE Volunteer_RegistersFor_Race
(
   volunteerID INT,
   raceID      INT,
   CONSTRAINT PRIMARY KEY (volunteerID, raceID),
   CONSTRAINT FOREIGN KEY (volunteerID) REFERENCES Volunteer (volunteerID)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT FOREIGN KEY (raceID) REFERENCES Race (raceID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE Volunteer_VolunteersFor_RefuelStation
(
   volunteerID INT,
   stationID   INT,
   raceID      INT,
   CONSTRAINT PRIMARY KEY (volunteerID, stationID, raceID),
   CONSTRAINT FOREIGN KEY (volunteerID) REFERENCES Volunteer (volunteerID)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT FOREIGN KEY (stationID, raceID) REFERENCES RefuelStation (stationID, raceID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE Volunteer_VolunteersFor_FirstAidStation
(
   volunteerID INT,
   stationID   INT,
   raceID      INT,
   CONSTRAINT PRIMARY KEY (volunteerID, stationID, raceID),
   CONSTRAINT FOREIGN KEY (volunteerID) REFERENCES Volunteer (volunteerID)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT FOREIGN KEY (stationID, raceID) REFERENCES FirstAidStation (stationID, raceID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE Sponsor_Sponsors_Race
(
   raceID          INT,
   sponsorID       INT,
   companyOverview varchar(300) NOT NULL,
   websiteLink     varchar(100) NOT NULL,
   CONSTRAINT PRIMARY KEY (raceID, sponsorID),
   CONSTRAINT FOREIGN KEY (raceID) REFERENCES Race (raceID)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT FOREIGN KEY (sponsorID) REFERENCES Sponsor (sponsorID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE Organizer_CommunicatesWith_Police
(
   organizerID INT,
   policeID    INT,
   CONSTRAINT PRIMARY KEY (organizerID, policeID),
   CONSTRAINT FOREIGN KEY (organizerID) REFERENCES EventOrganizer (organizerID)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT FOREIGN KEY (policeID) REFERENCES Police (policeID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE Organizer_CommunicatesWith_Volunteer
(
   volunteerID INT,
   organizerID INT,
   CONSTRAINT PRIMARY KEY (volunteerID, organizerID),
   CONSTRAINT FOREIGN KEY (volunteerID) REFERENCES Volunteer (volunteerID)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT FOREIGN KEY (organizerID) REFERENCES EventOrganizer (organizerID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE Sponsor_MakesDealWith_Organizer
(
   sponsorID   INT,
   organizerID INT,
   CONSTRAINT PRIMARY KEY (sponsorID, organizerID),
   CONSTRAINT FOREIGN KEY (sponsorID) REFERENCES Sponsor (sponsorID)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT FOREIGN KEY (organizerID) REFERENCES EventOrganizer (organizerID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE Organizer_BuysFrom_Vendor
(
   organizerID INT,
   vendorID    INT,
   CONSTRAINT PRIMARY KEY (organizerID, vendorID),
   CONSTRAINT FOREIGN KEY (organizerID) REFERENCES EventOrganizer (organizerID)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT FOREIGN KEY (vendorID) REFERENCES Vendor (vendorID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);

-- # inserting sample data into the Runner table
-- INSERT INTO Runner (firstName, lastName, gender, age, email,
--                     phone, street, city, state, country, zip)
-- VALUES ('Josh', 'Adreani', 'Male', 20, 'j.adreani@gmail.com',
--         '123-456-7890', '360 Huntington Ave', 'Boston', 'MA', 'USA', '02115'),
--         ('Sydney', 'McLaughlin', 'Female', 25, 's.mclaughlin@gmail.com',
--         '234-567-8901', '1 First Pl', 'Los Angeles', 'CA', 'USA', '90001');

-- # inserting sample data into the Volunteer table
-- INSERT INTO Volunteer (firstName, lastName, age, email, phone,
--                        street, city, state, country, zip)
-- VALUES ('Olivia', 'Gonzalez', 56, 'o.gonzales@hotmail.com', '111-222-3333',
--         '2 Woodland Dr', 'Rye', 'NY', 'USA', '10528'),
--         ('Bob', 'Smith', 33, 'b.smith@hotmail.com', '222-333-4444',
--          '3 Pleasant St', 'Albany', 'NY', 'USA', '12084');

-- # inserting sample data into the EventOrganizer table
-- INSERT INTO EventOrganizer (name, email, phone)
-- VALUES ('Tenafly Running Association', 'tenaflyrunningassociation@aol.com', '201-201-2012'),
--        ('Hartford Marathon Foundation', 'hartfordmarathon@aol.com', '333-444-5555');

-- # inserting sample data into the Sponsor table
-- INSERT INTO Sponsor (name, email, phone, companyType)
-- VALUES ('RaceTech Fitness Gear', 'racetech@gmail.com', '444-555-6666', 'Running Gear'),
-- ('PIVOT Physical Therapy', 'pivotpt@gmail.com', '543-210-9876', 'Sports Therapy');

-- # inserting sample data into the Vendor table
-- INSERT INTO Vendor (name, email, phone, vendorType)
-- VALUES ('Dominos', 'dominospizza@dominos.com', '121-212-1212', 'Fast Food'),
-- ('Magic Music', 'magicmusic@gmail.com', '777-777-7777', 'Entertainment');

-- # inserting sample data into the Police table
-- INSERT INTO Police (name, email, phone, street, city, state, country, zip)
-- VALUES  ('Tenafly Police Department', 'tenaflypd@tenafly.com', '201-333-3333',
--          '5 Riveredge Rd', 'Tenafly', 'NJ', 'USA', '07670'),
--         ('Hartford Police Department', 'hartfordpd@hartford.com', '201-444-4444',
--          '8 Washington Ave', 'Hartford', 'CT', 'USA', '06101');

-- # inserting sample data into the Race table
-- INSERT INTO Race (street, city, state, country, zip, date, terrainType,
--                   raceLength, maxRunners, checkInTime, organizerID)
-- VALUES ('19 Columbus Ave', 'Tenafly', 'NJ', 'USA', '07670', '2024-04-14 09:00:00', 'trail',
--         26.2, 3000, '2024-04-13 19:00:00', 1),
--         ('400 Second St', 'Hartford', 'CT', 'USA', '06101', '2023-11-30 08:00:00', 'road',
--         13.1, 2500, '2023-11-30 6:00:00', 2);

-- # inserting sample data into the RefuelStation table
-- INSERT INTO RefuelStation (stationID, venueSpot, amenities, raceID)
-- VALUES (1, 'Mile 12', 'Water, GU Energy Gels', 1),
--        (2, 'Mile 6', 'Water, Gatorade', 2);

-- # inserting sample data into the FirstAidStation table
-- INSERT INTO FirstAidStation (stationID, venueSpot, services, raceID)
-- VALUES (1, 'Start and Finish Line', 'First Aid Supplies, EMT', 1),
--        (2, 'Hartford Park', 'First Aid Kit, Ambulance on Site', 2);

-- # inserting sample data into the SponsorStation table
-- INSERT INTO SponsorStation (stationID, venueSpot, sponsorName, raceID, sponsorID)
-- VALUES (1, 'Pond in Hartford Park', 'RaceTech Fitness Gear', 1, 1),
--        (2, 'Fountain in Hartford Park', 'XYZ Supplies', 2, 2);

-- # inserting sample data into the BillingInfo table
-- INSERT INTO BillingInfo (cardNumber, cardExpirationDate, cardSecurityCode, billingStreet,
--                          billingCity, billingState, billingCountry, billingZip, runnerID)
-- VALUES (1234567898765432, '2028-12-31', 303, '55 Wait St', 'Boston', 'MA', 'USA', '02115', 1),
--        (9876543212345678, '2026-06-30', 753, '1 First Pl', 'Los Angeles', 'CA', 'USA', '90001', 2);

-- # inserting sample data into the RaceResults table
-- INSERT INTO RaceResults (runnerID, bibNumber, finishTime, raceID, organizerID)
-- VALUES  (1, 835, '03:38:12', 1, 1),
--         (2, 201, '04:02:21', 2, 2);

-- # inserting sample data into the MileSplits table
-- INSERT INTO MileSplits (runnerID, bibNumber, raceID, organizerID, marker, mileSplit)
-- VALUES
-- (1, 835, 1, 1, 'Mile 3', '00:21:05'),
-- (1, 835, 1, 1, 'Mile 6', '00:43:12'),
-- (2, 201, 2, 2, 'Mile 5', '00:39:51'),
-- (2, 201, 2, 2, 'Mile 13', '01:39:46');

-- # inserting sample data into the Runner_RunsIn_Race table
-- INSERT INTO Runner_RunsIn_Race (runnerID, raceID)
-- VALUES (1, 1),
--        (2, 2);

-- # inserting sample data into the Runner_ChecksInto_Race table
-- INSERT INTO Runner_ChecksInto_Race (runnerID, raceID, bib_number)
-- VALUES (1, 1, 835),
--        (2, 2, 201);

-- # inserting sample data into the Runner_RegistersFor_Race table
-- INSERT INTO Runner_RegistersFor_Race (runnerID, raceID)
-- VALUES (1, 1),
--        (2, 2);

-- # inserting sample data into the Volunteer_ChecksInto_Race table
-- INSERT INTO Volunteer_ChecksInto_Race (volunteerID, raceID)
-- VALUES (1, 1),
--        (2, 2);

-- # inserting sample data into the Volunteer_RegistersFor_Race table
-- INSERT INTO Volunteer_RegistersFor_Race (volunteerID, raceID)
-- VALUES (1, 1),
--        (2, 2);

-- # inserting sample data into the Volunteer_VolunteersFor_RefuelStation table
-- INSERT INTO Volunteer_VolunteersFor_RefuelStation (volunteerID, stationID, raceID)
-- VALUES (1, 1, 1),
--        (2, 2, 2);

-- # inserting sample data into the Volunteer_VolunteersFor_FirstAidStation table
-- INSERT INTO Volunteer_VolunteersFor_FirstAidStation (volunteerID, stationID, raceID)
-- VALUES (1, 1, 1),
--        (2, 2, 2);

-- # inserting sample data into the Sponsor_Sponsors_Race table
-- INSERT INTO Sponsor_Sponsors_Race (raceID, sponsorID, companyOverview, websiteLink)
-- VALUES (1, 1, 'RaceTech Fitness Gear is an established company in the sports and fitness equipment gear industry.',
--         'https://racetechfitnessgear.com'),
--        (2, 2, 'PIVOT Physical Therapy delivers the best physical therapy in the U.S.',
--         'https://pivotpt.com');

-- # inserting sample data into the Organizer_CommunicatesWith_Police table
-- INSERT INTO Organizer_CommunicatesWith_Police (organizerID, policeID)
-- VALUES (1, 1),
--        (2, 2);

-- # inserting sample data into the Organizer_CommunicatesWith_Volunteer table
-- INSERT INTO Organizer_CommunicatesWith_Volunteer (volunteerID, organizerID)
-- VALUES (1, 1),
--        (2, 2);

-- # inserting sample data into the Sponsor_MakesDealWith_Organizer table
-- INSERT INTO Sponsor_MakesDealWith_Organizer (sponsorID, organizerID)
-- VALUES (1, 1),
--        (2, 2);

-- # inserting sample data into the Organizer_BuysFrom_Vendor table
-- INSERT INTO Organizer_BuysFrom_Vendor (organizerID, vendorID)
-- VALUES (1, 1),
--        (2, 2);