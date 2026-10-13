import sqlite3
import datetime

# Define DBOperation class to manage all data into the database.
# Give a name of your choice to the database


class DBOperations:
# reusable SQL statements
  sql_create_pilot_table = '''CREATE TABLE IF NOT EXISTS Pilot(PilotID INTEGER PRIMARY KEY AUTOINCREMENT, Name VARCHAR(40) NOT NULL, DoB DATE NOT NULL, ContactNumber INTEGER NOT NULL)'''
  sql_create_plane_table = '''CREATE TABLE IF NOT EXISTS Plane(PlaneID INTEGER PRIMARY KEY AUTOINCREMENT, Location INTEGER NOT NULL, TypeID INTEGER NOT NULL, FOREIGN KEY (TypeID) REFERENCES PlaneType(TypeID), FOREIGN KEY (Location) REFERENCES Airport(AirportID))'''
  sql_create_planetype_table = '''CREATE TABLE IF NOT EXISTS PlaneType(TypeID INTEGER PRIMARY KEY AUTOINCREMENT, TypeName VARCHAR(100) NOT NULL, MaxPassengers INTEGER NOT NULL)'''
  sql_create_flight_table = '''CREATE TABLE IF NOT EXISTS Flight(FlightID INTEGER PRIMARY KEY AUTOINCREMENT, PlannedArrivalDateTime DATETIME, PlannedDepartureDateTime DATETIME, ActualArrivalDateTime DATETIME, ActualDepartureDateTime DATETIME, PlaneID INTEGER NOT NULL, DestinationAirportID INTEGER NOT NULL, OriginAirportID INTEGER NOT NULL, FirstOfficer INTEGER, Captain INTEGER, Status TEXT NOT NULL CHECK (Status IN ('Planned', 'Boarding', 'Departed', 'Landed', 'Complete')), FOREIGN KEY (PlaneID) REFERENCES Plane(PlaneID), FOREIGN KEY (DestinationAirportID) REFERENCES Airport(AirportID), FOREIGN KEY (OriginAirportID) REFERENCES Airport(AirportID), FOREIGN KEY (FirstOfficer) REFERENCES Pilot(PilotID), FOREIGN KEY (Captain) REFERENCES Pilot(PilotID))'''
  sql_create_airport_table = '''CREATE TABLE IF NOT EXISTS Airport(AirportID INTEGER PRIMARY KEY AUTOINCREMENT, AirportName VARCHAR(100) NOT NULL, CountryCode VARCHAR(3) NOT NULL, FOREIGN KEY (CountryCode) REFERENCES Country(CountryCode))'''
  sql_create_country_table = '''CREATE TABLE IF NOT EXISTS Country(CountryCode VARCHAR(3) NOT NULL, CountryName VARCHAR(100) NOT NULL, Continent VARCHAR (100) NOT NULL, PRIMARY KEY (CountryCode))'''
  sql_create_journeytime_table = '''CREATE TABLE IF NOT EXISTS JourneyTime(OriginID INTEGER, DestinationID INTEGER, TotalTravelTimeMins INTEGER NOT NULL, PRIMARY KEY (OriginID, DestinationID), FOREIGN KEY (DestinationID) REFERENCES Airport(AirportID), FOREIGN KEY (OriginID) REFERENCES Airport(AirportID))'''
  sql_insert = '''INSERT INTO Flight(PlannedArrivalDateTime, PlannedDepartureDateTime, ActualArrivalDateTime, ActualDepartureDateTime, PlaneID, DestinationAirportID, OriginAirportID, FirstOfficer, Captain, Status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
  sql_search_flight = '''SELECT * FROM Flight WHERE FlightID = ?'''
  sql_search_pilot = '''SELECT * FROM Flight WHERE FirstOfficer = ? OR Captain = ?'''
  sql_journey_time = '''SELECT TotalTravelTimeMins FROM JourneyTime WHERE OriginID = ? AND DestinationID = ?'''
  sql_available_pilots = "SELECT PilotID, Name, DoB FROM Pilot WHERE PilotID != ? AND PilotID NOT IN (SELECT Captain FROM Flight WHERE FlightID != ? AND Captain IS NOT NULL AND PlannedDepartureDateTime < ? AND PlannedArrivalDateTime > ? UNION SELECT FirstOfficer FROM Flight WHERE FlightID != ? AND FirstOfficer IS NOT NULL AND PlannedDepartureDateTime < ? AND PlannedArrivalDateTime > ?)"
  sql_update = '''UPDATE Flight SET PlannedArrivalDateTime = ?, PlannedDepartureDateTime = ?, ActualArrivalDateTime = ?, ActualDepartureDateTime = ?, PlaneID = ?, DestinationAirportID = ?, OriginAirportID = ?, FirstOfficer = ?, Captain = ?, Status = ? WHERE FlightID = ?'''


#database initialisation where tables are created if 
#they dont exist and populate the tables with test data if the tables are empty
  def __init__(self):
    try:
      self.conn = sqlite3.connect("FlightManagement.db")
      self.conn.execute("PRAGMA foreign_keys = ON")
      self.cur = self.conn.cursor()
      self.cur.execute(self.sql_create_country_table)
      self.cur.execute(self.sql_create_airport_table)
      self.cur.execute(self.sql_create_planetype_table)
      self.cur.execute(self.sql_create_plane_table)
      self.cur.execute(self.sql_create_pilot_table)
      self.cur.execute(self.sql_create_flight_table)
      self.cur.execute(self.sql_create_journeytime_table)
      self.cur.execute("SELECT COUNT(*) FROM Country")
      count = self.cur.fetchone()[0]
      if count == 0:
        self.cur.executescript("INSERT INTO Country VALUES('GBR','United Kingdom','Europe');INSERT INTO Country VALUES('FRA','France','Europe');INSERT INTO Country VALUES('DEU','Germany','Europe'); INSERT INTO Country VALUES('ESP','Spain','Europe'); INSERT INTO Country VALUES('ITA','Italy','Europe'); INSERT INTO Country VALUES('USA','United States','North America'); INSERT INTO Country VALUES('CAN','Canada','North America'); INSERT INTO Country VALUES('MEX','Mexico','North America'); INSERT INTO Country VALUES('BRA','Brazil','South America'); INSERT INTO Country VALUES('ARG','Argentina','South America'); INSERT INTO Country VALUES('AUS','Australia','Oceania'); INSERT INTO Country VALUES('NZL','New Zealand','Oceania'); INSERT INTO Country VALUES('JPN','Japan','Asia'); INSERT INTO Country VALUES('CHN','China','Asia'); INSERT INTO Country VALUES('IND','India','Asia');")
      self.cur.execute("SELECT COUNT(*) FROM Airport")
      count = self.cur.fetchone()[0]
      if count == 0:
        self.cur.executescript("INSERT INTO Airport VALUES(1,'Manchester Airport','GBR'); INSERT INTO Airport VALUES(2,'Heathrow Airport','GBR'); INSERT INTO Airport VALUES(3,'Charles de Gaulle','FRA'); INSERT INTO Airport VALUES(4,'Frankfurt Airport','DEU'); INSERT INTO Airport VALUES(5,'Madrid Airport','ESP');INSERT INTO Airport VALUES(6,'Rome Fiumicino','ITA'); INSERT INTO Airport VALUES(7,'JFK International','USA');INSERT INTO Airport VALUES(8,'Toronto Pearson','CAN'); INSERT INTO Airport VALUES(9,'Mexico City Airport','MEX'); INSERT INTO Airport VALUES(10,'Sao Paulo Airport','BRA'); INSERT INTO Airport VALUES(11,'Buenos Aires Airport','ARG');INSERT INTO Airport VALUES(12,'Sydney Airport','AUS'); INSERT INTO Airport VALUES(13,'Auckland Airport','NZL'); INSERT INTO Airport VALUES(14,'Tokyo Haneda','JPN'); INSERT INTO Airport VALUES(15,'Delhi Airport','IND');")
      self.cur.execute("SELECT COUNT(*) FROM PlaneType")
      count = self.cur.fetchone()[0]
      if count == 0:
        self.cur.executescript("INSERT INTO PlaneType VALUES(1,'Airbus A320',180);INSERT INTO PlaneType VALUES(2,'Airbus A321',220);INSERT INTO PlaneType VALUES(3,'Airbus A330',300);INSERT INTO PlaneType VALUES(4,'Airbus A350',350);INSERT INTO PlaneType VALUES(5,'Boeing 737-800',189);INSERT INTO PlaneType VALUES(6,'Boeing 737 MAX',210);INSERT INTO PlaneType VALUES(7,'Boeing 747',416);INSERT INTO PlaneType VALUES(8,'Boeing 757',239);INSERT INTO PlaneType VALUES(9,'Boeing 767',290);INSERT INTO PlaneType VALUES(10,'Boeing 777',396);INSERT INTO PlaneType VALUES(11,'Boeing 787',330);INSERT INTO PlaneType VALUES(12,'Embraer E190',114);INSERT INTO PlaneType VALUES(13,'ATR 72',78);INSERT INTO PlaneType VALUES(14,'Bombardier CRJ900',90);INSERT INTO PlaneType VALUES(15,'Airbus A220',145);")
      self.cur.execute("SELECT COUNT(*) FROM Plane")
      count = self.cur.fetchone()[0]
      if count == 0:
        self.cur.executescript("INSERT INTO Plane (Location,TypeID) VALUES(1,1);INSERT INTO Plane (Location,TypeID) VALUES(2,2);INSERT INTO Plane (Location,TypeID) VALUES(3,3);INSERT INTO Plane (Location,TypeID) VALUES(4,4);INSERT INTO Plane (Location,TypeID) VALUES(5,5);INSERT INTO Plane (Location,TypeID) VALUES(6,6);INSERT INTO Plane (Location,TypeID) VALUES(7,7);INSERT INTO Plane (Location,TypeID) VALUES(8,8);INSERT INTO Plane (Location,TypeID) VALUES(9,9);INSERT INTO Plane (Location,TypeID) VALUES(10,10);INSERT INTO Plane (Location,TypeID) VALUES(11,11);INSERT INTO Plane (Location,TypeID) VALUES(12,12);INSERT INTO Plane (Location,TypeID) VALUES(13,13);INSERT INTO Plane (Location,TypeID) VALUES(14,14);INSERT INTO Plane (Location,TypeID) VALUES(15,15);INSERT INTO Plane (Location,TypeID) VALUES(1,2);INSERT INTO Plane (Location,TypeID) VALUES(1,3);INSERT INTO Plane (Location,TypeID) VALUES(1,5);INSERT INTO Plane (Location,TypeID) VALUES(1,11);INSERT INTO Plane (Location,TypeID) VALUES(1,15);")
      self.cur.execute("SELECT COUNT(*) FROM Pilot")
      count = self.cur.fetchone()[0]
      if count == 0:
        self.cur.executescript("INSERT INTO Pilot VALUES(1,'John Smith','1980-05-10',447700000001);INSERT INTO Pilot VALUES(2,'Alice Brown','1985-03-12',447700000002);INSERT INTO Pilot VALUES(3,'David Wilson','1978-07-21',447700000003);INSERT INTO Pilot VALUES(4,'Emma Jones','1987-11-02',447700000004);INSERT INTO Pilot VALUES(5,'Michael Taylor','1982-01-14',447700000005);INSERT INTO Pilot VALUES(6,'Sophia Evans','1990-06-30',447700000006);INSERT INTO Pilot VALUES(7,'Daniel White','1979-04-11',447700000007);INSERT INTO Pilot VALUES(8,'Olivia Hall','1988-09-19',447700000008);INSERT INTO Pilot VALUES(9,'James Walker','1981-08-22',447700000009);INSERT INTO Pilot VALUES(10,'Grace Young','1991-02-17',447700000010);INSERT INTO Pilot VALUES(11,'Benjamin King','1983-12-25',447700000011);INSERT INTO Pilot VALUES(12,'Mia Scott','1989-10-15',447700000012);INSERT INTO Pilot VALUES(13,'Ethan Green','1984-07-04',447700000013);INSERT INTO Pilot VALUES(14,'Chloe Baker','1992-01-09',447700000014);INSERT INTO Pilot VALUES(15,'Henry Adams','1986-05-28',447700000015);")
      self.cur.execute("SELECT COUNT(*) FROM Flight")
      count = self.cur.fetchone()[0]
      if count == 0:
        self.cur.executescript("INSERT INTO Flight VALUES(1,'2026-11-01 08:00','2026-11-01 06:00',NULL,NULL,1,2,1,2,1,'Planned');INSERT INTO Flight VALUES(2,'2026-11-01 10:30','2026-11-01 08:00',NULL,NULL,2,3,2,4,3,'Planned');INSERT INTO Flight VALUES(3,'2026-11-02 14:00','2026-11-02 11:00',NULL,NULL,3,4,3,6,5,'Boarding');INSERT INTO Flight VALUES(4,'2026-11-02 18:00','2026-11-02 15:00',NULL,NULL,4,5,4,8,7,'Boarding');INSERT INTO Flight VALUES(5,'2026-11-03 12:00','2026-11-03 09:00',NULL,'2026-11-03 09:12',5,6,5,10,9,'Departed');INSERT INTO Flight VALUES(6,'2026-11-03 15:30','2026-11-03 12:00',NULL,'2026-11-03 12:04',6,7,6,12,11,'Departed');INSERT INTO Flight VALUES(7,'2026-11-04 21:00','2026-11-04 18:00','2026-11-04 20:52','2026-11-04 18:07',7,8,7,14,13,'Landed');INSERT INTO Flight VALUES(8,'2026-11-05 07:30','2026-11-05 05:00','2026-11-05 07:28','2026-11-05 05:03',8,9,8,1,15,'Landed');INSERT INTO Flight VALUES(9,'2026-11-05 13:00','2026-11-05 10:30',NULL,NULL,9,10,9,3,2,'Planned');INSERT INTO Flight VALUES(10,'2026-11-06 17:45','2026-11-06 14:15',NULL,NULL,10,11,10,5,4,'Planned');INSERT INTO Flight VALUES(11,'2026-11-07 09:15','2026-11-07 06:45',NULL,NULL,11,12,11,7,6,'Boarding');INSERT INTO Flight VALUES(12,'2026-11-07 20:00','2026-11-07 17:00',NULL,NULL,12,13,12,9,8,'Planned');INSERT INTO Flight VALUES(13,'2026-11-08 12:30','2026-11-08 09:30',NULL,NULL,13,14,13,11,10,'Planned');INSERT INTO Flight VALUES(14,'2026-11-08 18:15','2026-11-08 15:15',NULL,NULL,14,15,14,13,12,'Planned');INSERT INTO Flight VALUES(15,'2026-11-09 22:00','2026-11-09 18:30',NULL,NULL,15,1,15,15,14,'Planned');")
      self.cur.execute("SELECT COUNT(*) FROM JourneyTime")
      count = self.cur.fetchone()[0]
      if count == 0:
        routes = ""
        for originid in range(1, 16):
          for destinationid in range(1, 16):
            if originid != destinationid:
              if originid in [1, 2] and destinationid in [1, 2]:
                mins = 60
              elif originid <= 6 and destinationid <= 6:
                mins = 120
              elif destinationid in [7, 8, 9]:
                mins = 480
              elif destinationid in [10, 11]:
                mins = 720
              elif destinationid in [12, 13]:
                mins = 1320
              elif destinationid in [14, 15]:
                mins = 600
              else:
                mins = 180
              routes += f"INSERT INTO JourneyTime VALUES({originid},{destinationid},{mins});"
        self.cur.executescript(routes)
      self.conn.commit()
    except Exception as e:
      print(e)

# Creates connection for database operations
  def get_connection(self):
    self.conn = sqlite3.connect("FlightManagement.db")
    self.cur = self.conn.cursor()


# Funtion to manage the creation of new Flight records

  def addNewFlight(self):
    newFlight = Flight()
    result = self.runWizard([newFlight.setOriginCountry, newFlight.setOriginAirport, newFlight.setDestinationCountry, newFlight.setDestinationAirport, newFlight.setDepartureDateTime, newFlight.setPlane, newFlight.setCaptain, newFlight.setFirstOfficer, newFlight.confirmBooking],self)
    if (result != "cancel" and newFlight.originAirport is not None and newFlight.destinationAirport is not None and newFlight.plannedDeparture is not None and newFlight.plannedArrival is not None and newFlight.planeId is not None):
     newFlight.setAutoStatus("Planned")
     self.storeFlight(newFlight)

# Function to create a new entry in the flight table based on the values stored within the Flight object

  def storeFlight(self, Flight):
    try:
      self.cur.execute(self.sql_insert, (Flight.plannedArrival, Flight.plannedDeparture, Flight.actualArrival, Flight.actualDeparture, Flight.planeId, Flight.destinationAirport, Flight.originAirport, Flight.firstOfficer, Flight.captain, Flight.status))
      self.conn.commit()
      print("Inserted data successfully")
    except Exception as e:
      self.conn.rollback()
      print(e)


#Updates flights records based on changes made to the values within the flight object 
  def updateFlight(self, flight):
    try:
        self.cur.execute(self.sql_update,(flight.plannedArrival,flight.plannedDeparture,flight.actualArrival,flight.actualDeparture,flight.planeId,flight.destinationAirport,flight.originAirport,flight.firstOfficer,flight.captain, flight.status,flight.flightID))
        self.conn.commit()
    except Exception as e:
        self.conn.rollback()
        print(e)


#Function to search flight records based on none or multiple criteria

  def viewFlightsByCriteria(self):
    while True:
      params = []
      sql = "SELECT * FROM Flight WHERE TRUE"
      valid = True
      self.cur.execute("SELECT AirportID, AirportName FROM Airport")
      airports = self.cur.fetchall()

      print("\nAirports:")
      for airport in airports:
        print(f"{airport[0]}. {airport[1]}")
      print("\nSearch By:\n")
      destination = input("Destination Airport ID (B to return): ").upper()
      if destination == "B":
          return
      status = input("1.Status: \n")
      departureDate = input("1.Departure Date: \n")
      if destination != "":
        self.cur.execute('''SELECT AirportID FROM Airport WHERE AirportID = ?''',(destination,))
        airport = self.cur.fetchone()
        if airport is None:
          print("Destination is not valid")
          valid = False
        else:
          sql += " AND DestinationAirportID = ?"
          params.append(destination)
      if status != "":
        if status not in ['Planned', 'Boarding','Departed','Landed', 'Complete'] :
          print("Status is not valid")
          valid = False
        else:
          sql += " AND Status = ?"
          params.append(status)
      if departureDate != "":  
        try:
          departureDate = datetime.datetime.strptime(departureDate, "%d/%m/%Y %H:%M")
        except ValueError:
          print("Please enter a valid date and time.")
          valid = False
        else:
          sql += " AND PlannedDepartureDateTime = ?"
          params.append(departureDate)        
      if not valid:
        continue
      self.cur.execute(sql,params)
      results = self.cur.fetchall()
      if not results:
        print("No Flight found.")
        return
      for i in results:
       self.displayFlightSummary(i)
      return


 
# Function to search for flights where the pilot is the first officer or captain.

  def getPilotFlight(self):
    while True:
      try:
        pilotID = int(input("Enter PilotID: "))
        self.cur.execute("SELECT Name FROM Pilot WHERE PilotID = ?",(pilotID,))
        pilot = self.cur.fetchone()
        if pilot is None:
          print("Pilot not found")
          return
        self.cur.execute(self.sql_search_pilot, (pilotID,pilotID))
        results = self.cur.fetchall()
        if not results:
          print("No Flight found.")
          return
        for i in results:
         self.displayFlightSummary(i)
        return
      except ValueError:
        print("Please enter a valid Pilot ID.")
        continue

    
    
#Function to edit a flight details through a workflow based on the flight status.

  def updateFlightInformation(self):
    flight = self.getFlight()
    if flight is None:
     return
    self.displayFlightObject(flight)
    if flight.status == "Planned":
      self.PlannedFlightMenu(flight)
    elif flight.status == "Boarding":
      self.BoardingFlightMenu(flight)
    elif flight.status == "Departed":
      self.DepartedFlightMenu(flight)
    elif flight.status == "Landed":
      self.LandedFlightMenu(flight)
    return


#Edit menu for a planned flight
  def PlannedFlightMenu(self, flight):
    while True:
          self.cur.execute("SELECT AirportName FROM Airport WHERE AirportID = ?", (flight.originAirport,))
          origin = self.cur.fetchone()

          self.cur.execute("SELECT AirportName FROM Airport WHERE AirportID = ?", (flight.destinationAirport,))
          destination = self.cur.fetchone()

          originName = origin[0] if origin else flight.originAirport
          destinationName = destination[0] if destination else flight.destinationAirport
          try:
            print(f"1. Edit Origin: {originName}")
            print(f"2. Edit Destination: {destinationName}")
            print(f"3. Edit Departure Date Time: {flight.plannedDeparture}")
            print(f"4. Edit Plane: {flight.planeId}")
            print(f"5. Edit Captain: {flight.captain}")
            print(f"6. Edit First Officer: {flight.firstOfficer}")
            print(f"7. Set Status To Boarding: {flight.status}")
            print("8. Save Changes and Return to Main Menu")
            print("-" * 50)
            choice = input("Select a field to edit (or B to return): ")
            if choice.upper() == "B":
              return
            try:
              choice = int(choice)
              if 1<= choice <= 8:
                if choice == 1:
                  if flight.planeId is not None:
                    print("Origin cannot be changed once a plane has been assigned.")
                  else:
                    self.runWizard([flight.setOriginCountry,flight.setOriginAirport],self)
                elif choice == 2:
                  self.runWizard([flight.setDestinationCountry,flight.setDestinationAirport],self)
                elif choice == 3:
                  result = flight.setDepartureDateTime(self)
                  if result in ("back","cancel"):
                    continue
                elif choice == 4:
                  result = flight.setPlane(self)
                  if result in ("back","cancel"):
                    continue
                elif choice == 5:
                  result = flight.setCaptain(self)
                  if result in ("back","cancel"):
                    continue
                elif choice == 6:
                  result = flight.setFirstOfficer(self)
                  if result in ("back","cancel"):
                    continue
                elif choice == 7:
                  result = flight.setAutoStatus("Boarding")
                  if result in ("back","cancel"):
                    continue
                elif choice == 8:
                  self.updateFlight(flight)
                  return
                else:
                   print("please choose a valid option.")
            except ValueError:
              print("Please enter a number.")
          except Exception as e:
            print(e)


#Edit menu for a boarding flight - Only actual departure time can be edited here. Possible overide could be developed at a later date, discussion with client required
  def BoardingFlightMenu(self,flight):
      while True:
            try:
              print(f"1. Set Departure Date Time: {flight.actualDeparture}")
              print("2. Save Changes and Return to Main Menu")
              print("-" * 50)
              choice = input("Select a field to edit (or B to return): ")
              if choice.upper() == "B":
                return
              try:
                choice = int(choice)
                if 1<= choice <= 2:
                  if choice == 1:
                    result = flight.setActualDeparture(self)
                    if result in ("back","cancel"):
                      continue
                  elif choice == 2:
                    self.updateFlight(flight)
                    return
                  else:
                     print("please choose a valid option.")
              except ValueError:
                print("Please enter a number.")
            except Exception as e:
              print(e)


#Edit Menu for a departed flight - Only Arrival time can be edited here as its in the air
  def DepartedFlightMenu(self,flight):
      while True:
            try:
              print(f"1. Set Arrival Time: {flight.actualArrival}")
              print("2. Save Changes and Return to Main Menu")
              print("-" * 50)
              choice = input("Select a field to edit (or B to return): ")
              if choice.upper() == "B":
                return
              try:
                choice = int(choice)
                if 1<= choice <= 2:
                  if choice == 1:
                    result = flight.setActualArrival()
                    if result in ("back","cancel"):
                      continue
                  elif choice == 2:
                    self.updateFlight(flight)
                    return
                  else:
                     print("please choose a valid option.")
              except ValueError:
                print("Please enter a number.")
            except Exception as e:
              print(e)


#Edit menu for a landed flight - Setting the Flight to complete allows the plane to be rescheduled.
  def LandedFlightMenu(self,flight):
      while True:
            try:
              print(f"1. Set Status to'Complete: {flight.status}")
              print("2. Save Changes and Return to Main Menu")
              print("-" * 50)
              choice = input("Select a field to edit (or B to return): ")
              if choice.upper() == "B":
                return
              try:
                choice = int(choice)
                if 1<= choice <= 2:
                  if choice == 1:
                   self.completeFlight(flight)
                   return
                  elif choice == 2:
                    self.updateFlight(flight)
                    return
                  else:
                     print("please choose a valid option.")
              except ValueError:
                print("Please enter a number.")
            except Exception as e:
              print(e)


#CompleteFlight sequence to set staus and update the database.
  def completeFlight(self, flight):
    try:
        flight.setAutoStatus("Complete")
        self.cur.execute(self.sql_update,(flight.plannedArrival,flight.plannedDeparture,flight.actualArrival,flight.actualDeparture,flight.planeId,flight.destinationAirport,flight.originAirport,flight.firstOfficer,flight.captain,flight.status,flight.flightID))
        self.cur.execute("""UPDATE Plane SET Location = ? WHERE PlaneID = ?""",(flight.destinationAirport, flight.planeId))
        self.conn.commit()
        print("Flight completed and plane location updated.")
    except Exception as e:
        self.conn.rollback()
        print(e)


#Diplay code for flight details based on the row returned from the flight table
  def displayFlightSummary(self, flight):
       self.cur.execute("SELECT AirportName FROM Airport WHERE AirportID = ?", (flight[7],))
       origin = self.cur.fetchone()
       originName = origin[0] if origin else f"Airport {flight[7]}"
       self.cur.execute("SELECT AirportName FROM Airport WHERE AirportID = ?", (flight[6],))
       destination = self.cur.fetchone()
       destinationName = destination[0] if destination else f"Airport {flight[6]}"
       self.cur.execute("SELECT Name FROM Pilot WHERE PilotID = ?", (flight[9],))
       captain = self.cur.fetchone()
       captainName = captain[0] if captain else "None"
       self.cur.execute("SELECT Name FROM Pilot WHERE PilotID = ?", (flight[8],))
       firstOfficer = self.cur.fetchone()
       firstOfficerName = firstOfficer[0] if firstOfficer else "None"
       print(f"Flight ID: {flight[0]}")
       print(f"Plane ID: {flight[5]}")
       print(f"Origin: {originName}")
       print(f"Destination: {destinationName}")
       print(f"Departure: {flight[2]}")
       print(f"Arrival: {flight[1]}")
       print(f"Captain: {captainName}")
       print(f"First Officer: {firstOfficerName}")
       print(f"Status: {flight[10]}")
       print("-" * 30)


#Diplay code for flight details based on a flight object
  def displayFlightObject(self,flight):
    self.cur.execute("SELECT AirportName FROM Airport WHERE AirportID = ?", (flight.originAirport,))
    origin = self.cur.fetchone()
    originName = origin[0] if origin else f"Airport {flight.originAirport}"
    self.cur.execute("SELECT AirportName FROM Airport WHERE AirportID = ?", (flight.destinationAirport,))
    destination = self.cur.fetchone()
    destinationName = destination[0] if destination else f"Airport {flight.destinationAirport}"
    self.cur.execute("SELECT Name FROM Pilot WHERE PilotID = ?", (flight.captain,))
    captain = self.cur.fetchone()
    captainName = captain[0] if captain else "None"
    self.cur.execute("SELECT Name FROM Pilot WHERE PilotID = ?", (flight.firstOfficer,))
    firstOfficer = self.cur.fetchone()
    firstOfficerName = firstOfficer[0] if firstOfficer else "None"
    print("\nFlight Details")
    print("-" * 30)
    print(f"Flight ID: {flight.flightID}")
    print(f"Plane ID: {flight.planeId}")
    print(f"Origin: {originName}")
    print(f"Destination: {destinationName}")
    print(f"Departure: {flight.plannedDeparture}")
    print(f"Arrival: {flight.plannedArrival}")
    print(f"Captain: {captainName}")
    print(f"First Officer: {firstOfficerName}")
    print(f"Status: {flight.status}")
    print("-" * 30)


# Menu to assign Pilots using the Main Menu feature
  def assignPilot(self):
      flight = self.getFlight()
      if flight is None:
       return
      if flight.status != "Planned":
       print("Unable to edit flights that are not Planned Status")
       return
      while True:
       self.cur.execute("SELECT Name FROM Pilot WHERE PilotID = ?",(flight.captain,))
       capt = self.cur.fetchone()
       captName = capt[0] if capt else "None"
       self.cur.execute("SELECT Name FROM Pilot WHERE PilotID = ?",(flight.firstOfficer,))
       firstOff = self.cur.fetchone()
       firstOffName = firstOff[0] if firstOff else "None"
       print("\nFlight Details")
       print(f"1. Edit Captain: {flight.captain} {captName}")
       print(f"2. Edit First Officer: {flight.firstOfficer} {firstOffName}")
       print("3.Remove Captain")
       print("4.Remove First Officer")
       print("5.Save Changes and Return to Main Menu")
       print("6.Return")
       print("-" * 50)
       try:
        choice = int(input("Select an option: "))
        if 1<= choice <= 6:
          if choice == 1:
           result = flight.setCaptain(self)
           if result in ("back","cancel"):
             continue
          elif choice == 2:
           result = flight.setFirstOfficer(self)
           if result in ("back","cancel"):
            continue
          elif choice == 3:
           flight.captain = None
          elif choice == 4:
            flight.firstOfficer = None              
          elif choice == 5:
           self.updateFlight(flight)
           return
          elif choice == 6:
           return
        else:
          print("please choose a valid option.")
       except ValueError:
        print("Please enter a number.")
  

#Wizard function to control new flight and edit destination wizards
  def runWizard(self,steps,db):
    currentStep = 0
    while 0 <= currentStep < len(steps):
      result = steps[currentStep](db)
      if result == "back":
        if currentStep > 0:
          currentStep -=1
      elif result == "cancel":
        return "cancel"
      else:
        currentStep += 1
    return

#Function to edit the destination menu triggered from the main menu.
  def updateDestinationInformation(self):
    flight = self.getFlight()
    if flight is None:
      return
    if flight.status != "Planned":
      print("Only flights with a 'Planned' status can be edited.")
      return
    while True:
      self.cur.execute("SELECT AirportName FROM Airport WHERE AirportID = ?", (flight.destinationAirport,))
      destination = self.cur.fetchone()
      destinationName = destination[0] if destination else flight.destinationAirport
      try:
        self.displayFlightObject(flight)
        print("-" * 50)
        print(f"1. Destination Airport: {destinationName}")
        print("2. Save Changes and Return to Main Menu")
        print("-" * 50)
        choice = input("Select a field to edit (or B to return): ")
        if choice.upper() == "B":
          return
        try:
          choice = int(choice)
          if 1<= choice <= 2:
            if choice == 1:
              result = self.runWizard([flight.setDestinationCountry,flight.setDestinationAirport],self)
              if result != "cancel" and flight.plannedDeparture is not None:
               flight.setArrivalDateTime(self)
            elif choice == 2:
              self.updateFlight(flight)
              return
            else:
              print("please choose a valid option.")
        except ValueError:
          print("Please enter a number.")
      except Exception as e:
        print(e)



#function to search for a flight, and create a flight object in the system which can be worked on during edit menus.
  def getFlight(self):
    while True:
      flightID = input("Enter FlightID (C=Cancel): ")
      if flightID.upper() == "C":
        return
      try:
        flightID = int(flightID)
      except ValueError:
        print("Please enter a valid FlightID")
        continue
      self.cur.execute(self.sql_search_flight, (flightID,))
      result = self.cur.fetchone()
      if result is None:
        print("No Record, enter a valid FlightID.")
        continue
      elif result is not None:
        flight = Flight()
        flight.flightID = result[0]
        flight.plannedArrival = (datetime.datetime.fromisoformat(result[1]) if result[1] is not None else None)
        flight.plannedDeparture = (datetime.datetime.fromisoformat(result[2])if result[2] is not None else None)
        flight.actualArrival = (datetime.datetime.fromisoformat(result[3])if result[3] is not None else None)
        flight.actualDeparture = (datetime.datetime.fromisoformat(result[4])if result[4] is not None else None)
        flight.planeId = result[5]
        flight.destinationAirport = result[6]
        flight.originAirport = result[7]
        flight.firstOfficer = result[8]
        flight.captain = result[9]
        flight.status = result[10]
      return flight

  
# delete flight locates a flight record based on the flightID and removes the flight record only.

  def deleteFlight(self):
    flight = self.getFlight()
    if flight is None:
      return
    if flight.status != "Planned":
      print("Only flights with a 'Planned' status can be deleted.")
      return
    confirm = input(f"Delete Flight {flight.flightID}? (Y/N): ").upper()
    if confirm != "Y":
      return
    try:
      self.cur.execute("DELETE FROM Flight WHERE FlightID = ?", (flight.flightID,))
      self.conn.commit()
      if self.cur.rowcount > 0:
        print(f"{self.cur.rowcount} row(s) deleted.")
      else:
        print("Cannot find this record in the database.")

    except Exception as e:
      self.conn.rollback()
      print(e)

# New class for flight, used to create an editable flight object for users to make changes to prior to committing back to the database
class Flight:

  def __init__(self):
    self.flightID = None
    self.originAirport = None
    self.originCountry = None
    self.destinationAirport = None
    self.destinationCountry = None
    self.status = None
    self.captain = None
    self.firstOfficer = None
    self.planeId = None
    self.plannedArrival = None
    self.plannedDeparture = None
    self.actualArrival = None
    self.actualDeparture = None

# function for Selecting the Origin Country
  def setOriginCountry(self,db):
    while True:
      db.cur.execute("SELECT CountryCode, CountryName FROM Country")
      countries = db.cur.fetchall()
      for i, country in enumerate(countries, start = 1):
        print(f"{i}. {country[1]}" )
      print("\nB - Back")
      print("C - Cancel\n")
      choice = input("Enter the country the flight is flying from: ").upper()
      if choice == "B":
        return "back"
      if choice == "C":
        return "cancel"
      try:
        choice = int(choice)
        if 1<= choice <= len(countries):
          self.originCountry = countries[choice - 1][0]
          return
        print("please choose a valid option.")
      except ValueError:
        print("Please enter a number.")

# function for Assigning Origin Airport
  def setOriginAirport(self,db):
    while True:
      db.cur.execute("SELECT AirportID, AirportName, CountryCode FROM Airport WHERE CountryCode = ?",(self.originCountry,))
      airports = db.cur.fetchall()
      for i, airport in enumerate(airports, start = 1):
        print(f"{i}. {airport[1]}" )
      print("\nB - Back")
      print("C - Cancel\n")
      choice = input("Enter the airport the flight is flying from: ").upper()
      if choice == "B":
        return "back"
      if choice == "C":
        return "cancel"
      try:
        choice = int(choice)
        if 1<= choice <= len(airports):
          self.originAirport = airports[choice - 1][0]
          return
        print("please choose a valid option.")
      except ValueError:
        print("Please enter a number.")


# function for Selecting the Destination Country
  def setDestinationCountry(self,db):
    while True:
      db.cur.execute("SELECT CountryCode, CountryName FROM Country")
      countries = db.cur.fetchall()
      for i, country in enumerate(countries, start = 1):
        print(f"{i}. {country[1]}" )
      print("\nB - Back")
      print("C - Cancel\n")
      choice = input("Enter the country the flight is flying to: ").upper()
      if choice == "B":
        return "back"
      if choice == "C":
        return "cancel"
      try:
        choice = int(choice)
        if 1<= choice <= len(countries):
          self.destinationCountry = countries[choice - 1][0]
          return
        print("please choose a valid option.")
      except ValueError:
        print("Please enter a number.")

# function for Assigning the Destination Airport

  def setDestinationAirport(self,db):
    while True:
      db.cur.execute("SELECT AirportID, AirportName, CountryCode FROM Airport WHERE CountryCode = ? AND AirportID != ?",(self.destinationCountry, self.originAirport))
      airports = db.cur.fetchall()
      for i, airport in enumerate(airports, start = 1):
        print(f"{i}. {airport[1]}" )
      print("\nB - Back")
      print("C - Cancel\n")
      choice = input("Enter the airport the flight is flying to: ").upper()
      if choice == "B":
        return "back"
      if choice == "C":
        return "cancel"
      try:
        choice = int(choice)
        if 1<= choice <= len(airports):
          self.destinationAirport = airports[choice - 1][0]
          return
        print("please choose a valid option.")
      except ValueError:
        print("Please enter a number.")



# Function to select Departure Date Time - A flight cannot be scheduled in the past
  def setDepartureDateTime(self,db):
    while True:

      print("\nB - Back")
      print("C - Cancel\n")
      flightDate = input("Enter flight date (dd/MM/YYYY HH:MM): ")

      if flightDate.upper() == "B":
        return "back"
      if flightDate.upper() == "C":
        return "cancel"
      try:
        self.plannedDeparture = datetime.datetime.strptime(flightDate, "%d/%m/%Y %H:%M")
        if self.plannedDeparture < datetime.datetime.now():
          print("Departure time cannot be in the past.")
          continue
        self.setArrivalDateTime(db)
        return
      except ValueError:
        print("Please enter a valid date and time.")



# Autopopulate Arrival Date Time
  def setArrivalDateTime(self, db):
      db.cur.execute(DBOperations.sql_journey_time,(self.originAirport, self.destinationAirport))
      result = db.cur.fetchone()
      if self.status == "Departed":
        if result is None:
          print("No journey time found for this route.")
          return False
        traveltime = result[0]
        self.plannedArrival = self.actualDeparture + datetime.timedelta(minutes = traveltime)
      else:
        if result is None:
          print("No journey time found for this route.")
          return False
        traveltime = result[0]
        self.plannedArrival = self.plannedDeparture + datetime.timedelta(minutes = traveltime)



# Function to set Actual Departure Date Time
  def setActualDeparture(self,db):
    while True:
      print("\nB - Back")
      print("C - Cancel\n")
      flightDate = input("Enter actual departure date time (dd/MM/YYYY HH:MM): ")

      if flightDate.upper() == "B":
        return "back"
      if flightDate.upper() == "C":
        return "cancel"
      try:
        self.actualDeparture = datetime.datetime.strptime(flightDate, "%d/%m/%Y %H:%M")
        self.setAutoStatus("Departed")
        self.setArrivalDateTime(db)
        return
      except ValueError:
        print("Please enter a valid date and time.")



# Function to set Actual Arrival Date Time
  def setActualArrival(self):
    while True:
      print("\nB - Back")
      print("C - Cancel\n")
      flightDate = input("Enter actual arrival date time (dd/MM/YYYY HH:MM): ")
      if flightDate.upper() == "B":
        return "back"
      if flightDate.upper() == "C":
        return "cancel"
      try:
        self.actualArrival = datetime.datetime.strptime(flightDate, "%d/%m/%Y %H:%M")
        self.setAutoStatus("Landed")
        return
      except ValueError:
        print("Please enter a valid date and time.")



# Function to Select Plane 

  def setPlane(self,db):
    while True:
      currentFlightID = self.flightID if self.flightID is not None else -1
      db.cur.execute("SELECT PlaneID, TypeName, MaxPassengers FROM Plane JOIN PlaneType ON Plane.TypeID = PlaneType.TypeID WHERE Location = ? AND Plane.PlaneID NOT IN (SELECT PlaneID FROM Flight WHERE Status != 'Complete' AND FlightID != ?)", (self.originAirport, currentFlightID))
      planes = db.cur.fetchall()
      for i, plane in enumerate(planes, start = 1):
        print(f"{i}. {plane[1]} Passengers:{plane[2]}" )
      if len(planes) <= 0:
        input("No planes available at your location. Press Enter to go back: ")
        return "back"
      print("\nB - Back")
      print("C - Cancel\n")
      choice = input("Enter the plane you would like to take the Flight: ").upper()
  
      if choice == "B":
        return "back"
      if choice == "C":
        return "cancel"
      try:
        choice = int(choice)
        if 1 <= choice <= len(planes):
          self.planeId = planes[choice - 1][0]
          return
        print("please choose a valid option.")
      except ValueError:
        print("Please enter a number.")


# Function to Select The Captain 
  def setCaptain(self,db): 
    while True:
      currentFlightID = self.flightID if self.flightID is not None else -1
      firstOfficerToExclude = self.firstOfficer if self.firstOfficer is not None else -1
      db.cur.execute(DBOperations.sql_available_pilots, (firstOfficerToExclude, currentFlightID, self.plannedArrival, self.plannedDeparture, currentFlightID, self.plannedArrival, self.plannedDeparture))
      pilots = db.cur.fetchall()
      for i, pilot in enumerate(pilots, start = 1):
        print(f"{i}. {pilot[1]}")
      if len(pilots) <= 0:
       input("No pilots available. Press Enter to go back: ")
       return "back"
     
      print("\nB - Back")
      print("C - Cancel\n")
      print("S - Skip\n")
      choice = input("Enter the pilot to Captain the plane: ").upper()

      if choice == "B":
        return "back"
      if choice == "C":
        return "cancel"
      if choice == "S":
        return
      try:
        choice = int(choice)
        if 1<= choice <= len(pilots):
          self.captain = pilots[choice - 1][0]
          return
        print("please choose a valid option.")
      except ValueError:
        print("Please enter a number.")



# Function to Select The First Officer 
  def setFirstOfficer(self,db):  
    while True:
      currentFlightID = self.flightID if self.flightID is not None else -1
      captainToExclude = self.captain if self.captain is not None else -1
      db.cur.execute(DBOperations.sql_available_pilots, (captainToExclude, currentFlightID, self.plannedArrival, self.plannedDeparture, currentFlightID, self.plannedArrival, self.plannedDeparture))
      pilots = db.cur.fetchall()
      for i, pilot in enumerate(pilots, start = 1):
        print(f"{i}. {pilot[1]}")
      if len(pilots) <= 0:
       input("No pilots available. Press Enter to go back: ")
       return "back"

      print("\nB - Back")
      print("C - Cancel\n")
      print("S - Skip\n")
      choice = input("Enter the Pilot for First Officer: ").upper()

      if choice == "B":
        return "back"
      if choice == "C":
        return "cancel"
      if choice == "S":
        return
      try:
        choice = int(choice)
        if 1<= choice <= len(pilots):
          self.firstOfficer = pilots[choice - 1][0]
          return
        print("please choose a valid option.")
      except ValueError:
        print("Please enter a number.")



#Function for displaying the selected items and offer the user to submit or cancel or continue to edit the record.
  def confirmBooking(self,db):
    while True:
      db.displayFlightObject(self)
      print("\nB - Back")
      print("C - Cancel\n")
      print("S - Save\n")
      choice = input("Do you want to store the new Flight? ").upper()
  
      if choice == "B":
        return "back"
      if choice == "C":
        return "cancel"
      if choice == "S":
        return
      else:
        print("Please enter a valid option.")


#Boarding only manual trigger - All others could be triggered autonomously
  def setAutoStatus(self, status):
    if status not in ['Planned', 'Boarding','Departed','Landed', 'Complete'] :
      print("Status is not valid")
      return
    self.status = status



# Main Function where the main menu is managed
db_ops = DBOperations()

while True:
  print("\n Menu:")
  print("**********")
  print(" 1. Add a New Flight")
  print(" 2. View Flights by Criteria")
  print(" 3. Update Flight Information")
  print(" 4. Assign/Remove Pilot on Flight")
  print(" 5. View Pilot Flight")
  print(" 6. View/Update Destination Information")
  print(" 7. Delete Flight")
  print(" 8. Exit\n")
  try:
   __choose_menu = int(input("Enter your choice: "))
   if __choose_menu == 1:
    db_ops.addNewFlight()
   elif __choose_menu == 2:
    db_ops.viewFlightsByCriteria()
   elif __choose_menu == 3:
    db_ops.updateFlightInformation()
   elif __choose_menu == 4:
    db_ops.assignPilot()
   elif __choose_menu == 5:
    db_ops.getPilotFlight()
   elif __choose_menu == 6:
    db_ops.updateDestinationInformation()
   elif __choose_menu == 7:
    db_ops.deleteFlight()
   elif __choose_menu == 8:
    db_ops.conn.close()
    print("Application closed.")
    break
   else:
    print("Invalid Choice")
  except ValueError:
          print("Please enter a number.")