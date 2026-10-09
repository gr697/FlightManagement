import sqlite3
import datetime

# Define DBOperation class to manage all data into the database.
# Give a name of your choice to the database


class DBOperations:
  sql_create_pilot_table = '''CREATE TABLE IF NOT EXISTS Pilot(PilotID INTEGER PRIMARY KEY AUTOINCREMENT, Name VARCHAR(40) NOT NULL, DoB DATE NOT NULL, ContactNumber INTEGER NOT NULL)'''
  sql_create_plane_table = '''CREATE TABLE IF NOT EXISTS Plane(PlaneID INTEGER PRIMARY KEY AUTOINCREMENT, Location INTEGER NOT NULL, TypeID INTEGER NOT NULL, FOREIGN KEY (TypeID) REFERENCES PlaneType(TypeID), FOREIGN KEY (Location) REFERENCES Airport(AirportID))'''
  sql_create_planetype_table = '''CREATE TABLE IF NOT EXISTS PlaneType(TypeID INTEGER PRIMARY KEY AUTOINCREMENT, TypeName VARCHAR(200) NOT NULL, MaxPassengers INTEGER NOT NULL)'''
  sql_create_schedule_table = '''CREATE TABLE IF NOT EXISTS Schedule(FlightID INTEGER PRIMARY KEY AUTOINCREMENT, PlannedArrivalDateTime DATETIME, PlannedDepartureDateTime DATETIME, ActualArrivalDateTime DATETIME, ActualDepartureDateTime DATETIME, PlaneID INTEGER NOT NULL, ToAirportID INTEGER NOT NULL, FromAirportID INTEGER NOT NULL, FirstOfficer INTEGER NOT NULL, Captain INTEGER NOT NULL, Status TEXT NOT NULL CHECK (Status IN ('Planned', 'Delayed', 'Boarding', 'Departed', 'Landed')), FOREIGN KEY (PlaneID) REFERENCES Plane(PlaneID), FOREIGN KEY (ToAirportID) REFERENCES Airport(AirportID), FOREIGN KEY (FromAirportID) REFERENCES Airport(AirportID), FOREIGN KEY (FirstOfficer) REFERENCES Pilot(PilotID), FOREIGN KEY (Captain) REFERENCES Pilot(PilotID))'''
  sql_create_airport_table = '''CREATE TABLE IF NOT EXISTS Airport(AirportID INTEGER PRIMARY KEY AUTOINCREMENT, AirportName VARCHAR(200) NOT NULL, CountryCode VARCHAR(3) NOT NULL, FOREIGN KEY (CountryCode) REFERENCES Country(CountryCode))'''
  sql_create_country_table = '''CREATE TABLE IF NOT EXISTS Country(CountryCode CHAR(3) NOT NULL, CountryName VARCHAR(200) NOT NULL, Continent VARCHAR (200) NOT NULL, PRIMARY KEY (CountryCode))'''
  sql_create_journeytime_table = '''CREATE TABLE IF NOT EXISTS JourneyTime(OriginID INTEGER, DestinationID INTEGER, TotalTravelTimeMins INTEGER NOT NULL, PRIMARY KEY (OriginID, DestinationID), FOREIGN KEY (DestinationID) REFERENCES Airport(AirportID), FOREIGN KEY (OriginID) REFERENCES Airport(AirportID))'''
  sql_insert = ""
  sql_select_all = "select * from TableName"
  sql_search = "select * from TableName where FlightID = ?"
  sql_alter_data = ""
  sql_update_data = ""
  sql_delete_data = ""
  sql_drop_table = ""




  def __init__(self):
    try:
      self.conn = sqlite3.connect("FlightManagement.db")
      self.cur = self.conn.cursor()
      self.cur.execute(self.sql_create_pilot_table)
      self.cur.execute(self.sql_create_plane_table)
      self.cur.execute(self.sql_create_planetype_table)
      self.cur.execute(self.sql_create_schedule_table)
      self.cur.execute(self.sql_create_airport_table)
      self.cur.execute(self.sql_create_country_table)
      self.cur.execute(self.sql_create_journeytime_table)
      self.cur.execute("SELECT COUNT(*) FROM Country")
      count = self.cur.fetchone()[0]
      if count == 0:
        self.cur.executescript("INSERT INTO Country VALUES('GBR','United Kingdom','Europe');INSERT INTO Country VALUES('FRA','France','Europe');INSERT INTO Country VALUES('DEU','Germany','Europe'); INSERT INTO Country VALUES('ESP','Spain','Europe'); INSERT INTO Country VALUES('ITA','Italy','Europe'); INSERT INTO Country VALUES('USA','United States','North America'); INSERT INTO Country VALUES('CAN','Canada','North America'); INSERT INTO Country VALUES('MEX','Mexico','North America'); INSERT INTO Country VALUES('BRA','Brazil','South America'); INSERT INTO Country VALUES('ARG','Argentina','South America'); INSERT INTO Country VALUES('AUS','Australia','Oceania'); INSERT INTO Country VALUES('NZL','New Zealand','Oceania'); INSERT INTO Country VALUES('JPN','Japan','Asia'); INSERT INTO Country VALUES('CHN','China','Asia'); INSERT INTO Country VALUES('IND','India','Asia');")
      self.cur.execute("SELECT COUNT(*) FROM Airport")
      count = self.cur.fetchone()[0]
      if count == 0:
        self.cur.executescript("INSERT INTO Airport VALUES(1,'Manchester Airport','GBR'); INSERT INTO Airport VALUES(2,'Heathrow Airport','GBR'); INSERT INTO Airport VALUES(3,'Charles de Gaulle','FRA'); INSERT INTO Airport VALUES(4,'Frankfurt Airport','DEU'); INSERT INTO Airport VALUES(5,'Madrid Airport','ESP');INSERT INTO Airport VALUES(6,'Rome Fiumicino','ITA'); INSERT INTO Airport VALUES(7,'JFK International','USA');INSERT INTO Airport VALUES(8,'Toronto Pearson','CAN'); INSERT INTO Airport VALUES(9,'Mexico City Airport','MEX'); INSERT INTO Airport VALUES(10,'Sao Paulo Airport','BRA'); INSERT INTO Airport VALUES(11,'Buenos Aires Airport','ARG');INSERT INTO Airport VALUES(12,'Sydney Airport','AUS'); INSERT INTO Airport VALUES(13,'Auckland Airport','NZL'); INSERT INTO Airport VALUES(14,'Tokyo Haneda','JPN'); INSERT INTO Airport VALUES(15,'Delhi Airport','IND');")
      self.cur.execute("SELECT COUNT(*) FROM Plane")
      count = self.cur.fetchone()[0]
      if count == 0:
        self.cur.executescript("INSERT INTO Plane (Location,TypeID) VALUES(1,1);INSERT INTO Plane (Location,TypeID) VALUES(2,2);INSERT INTO Plane (Location,TypeID) VALUES(3,3);INSERT INTO Plane (Location,TypeID) VALUES(4,4);INSERT INTO Plane (Location,TypeID) VALUES(5,5);INSERT INTO Plane (Location,TypeID) VALUES(6,6);INSERT INTO Plane (Location,TypeID) VALUES(7,7);INSERT INTO Plane (Location,TypeID) VALUES(8,8);INSERT INTO Plane (Location,TypeID) VALUES(9,9);INSERT INTO Plane (Location,TypeID) VALUES(10,10);INSERT INTO Plane (Location,TypeID) VALUES(11,11);INSERT INTO Plane (Location,TypeID) VALUES(12,12);INSERT INTO Plane (Location,TypeID) VALUES(13,13);INSERT INTO Plane (Location,TypeID) VALUES(14,14);INSERT INTO Plane (Location,TypeID) VALUES(15,15);")
      count = self.cur.fetchone()[0]
      if count == 0:
        self.cur.executescript("INSERT INTO PlaneType VALUES(1,'Airbus A320',180);INSERT INTO PlaneType VALUES(2,'Airbus A321',220);INSERT INTO PlaneType VALUES(3,'Airbus A330',300);INSERT INTO PlaneType VALUES(4,'Airbus A350',350);INSERT INTO PlaneType VALUES(5,'Boeing 737-800',189);INSERT INTO PlaneType VALUES(6,'Boeing 737 MAX',210);INSERT INTO PlaneType VALUES(7,'Boeing 747',416);INSERT INTO PlaneType VALUES(8,'Boeing 757',239);INSERT INTO PlaneType VALUES(9,'Boeing 767',290);INSERT INTO PlaneType VALUES(10,'Boeing 777',396);INSERT INTO PlaneType VALUES(11,'Boeing 787',330);INSERT INTO PlaneType VALUES(12,'Embraer E190',114);INSERT INTO PlaneType VALUES(13,'ATR 72',78);INSERT INTO PlaneType VALUES(14,'Bombardier CRJ900',90);INSERT INTO PlaneType VALUES(15,'Airbus A220',145);")
      self.cur.execute("SELECT COUNT(*) FROM Pilot")
      count = self.cur.fetchone()[0]
      if count == 0:
        self.cur.executescript("INSERT INTO Pilot VALUES(1,'John Smith','1980-05-10',447700000001);INSERT INTO Pilot VALUES(2,'Alice Brown','1985-03-12',447700000002);INSERT INTO Pilot VALUES(3,'David Wilson','1978-07-21',447700000003);INSERT INTO Pilot VALUES(4,'Emma Jones','1987-11-02',447700000004);INSERT INTO Pilot VALUES(5,'Michael Taylor','1982-01-14',447700000005);INSERT INTO Pilot VALUES(6,'Sophia Evans','1990-06-30',447700000006);INSERT INTO Pilot VALUES(7,'Daniel White','1979-04-11',447700000007);INSERT INTO Pilot VALUES(8,'Olivia Hall','1988-09-19',447700000008);INSERT INTO Pilot VALUES(9,'James Walker','1981-08-22',447700000009);INSERT INTO Pilot VALUES(10,'Grace Young','1991-02-17',447700000010);INSERT INTO Pilot VALUES(11,'Benjamin King','1983-12-25',447700000011);INSERT INTO Pilot VALUES(12,'Mia Scott','1989-10-15',447700000012);INSERT INTO Pilot VALUES(13,'Ethan Green','1984-07-04',447700000013);INSERT INTO Pilot VALUES(14,'Chloe Baker','1992-01-09',447700000014);INSERT INTO Pilot VALUES(15,'Henry Adams','1986-05-28',447700000015);")
      self.cur.execute("SELECT COUNT(*) FROM Schedule")
      count = self.cur.fetchone()[0]
      if count == 0:
        self.cur.executescript("INSERT INTO Schedule VALUES(1,'2026-11-01 08:00','2026-11-01 06:00',NULL,NULL,1,2,1,2,1,'Planned');INSERT INTO Schedule VALUES(2,'2026-11-01 10:30','2026-11-01 08:00',NULL,NULL,2,3,2,4,3,'Planned');INSERT INTO Schedule VALUES(3,'2026-11-02 14:00','2026-11-02 11:00',NULL,NULL,3,4,3,6,5,'Boarding');INSERT INTO Schedule VALUES(4,'2026-11-02 18:00','2026-11-02 15:00',NULL,NULL,4,5,4,8,7,'Delayed');INSERT INTO Schedule VALUES(5,'2026-11-03 12:00','2026-11-03 09:00',NULL,NULL,5,6,5,10,9,'Planned');INSERT INTO Schedule VALUES(6,'2026-11-03 15:30','2026-11-03 12:00',NULL,NULL,6,7,6,12,11,'Departed');INSERT INTO Schedule VALUES(7,'2026-11-04 21:00','2026-11-04 18:00',NULL,NULL,7,8,7,14,13,'Planned');INSERT INTO Schedule VALUES(8,'2026-11-05 07:30','2026-11-05 05:00',NULL,NULL,8,9,8,1,15,'Landed');INSERT INTO Schedule VALUES(9,'2026-11-05 13:00','2026-11-05 10:30',NULL,NULL,9,10,9,3,2,'Planned');INSERT INTO Schedule VALUES(10,'2026-11-06 17:45','2026-11-06 14:15',NULL,NULL,10,11,10,5,4,'Departed');INSERT INTO Schedule VALUES(11,'2026-11-07 09:15','2026-11-07 06:45',NULL,NULL,11,12,11,7,6,'Boarding');INSERT INTO Schedule VALUES(12,'2026-11-07 20:00','2026-11-07 17:00',NULL,NULL,12,13,12,9,8,'Delayed');INSERT INTO Schedule VALUES(13,'2026-11-08 12:30','2026-11-08 09:30',NULL,NULL,13,14,13,11,10,'Planned');INSERT INTO Schedule VALUES(14,'2026-11-08 18:15','2026-11-08 15:15',NULL,NULL,14,15,14,13,12,'Departed');INSERT INTO Schedule VALUES(15,'2026-11-09 22:00','2026-11-09 18:30',NULL,NULL,15,1,15,15,14,'Planned');")
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
    finally:
      self.conn.close()


  def get_connection(self):
    self.conn = sqlite3.connect("FlightManagement.db")
    self.cur = self.conn.cursor()




  def addNewFlight(self):
    newFlight = Schedule()
    origincountry = ""
    destinationcountry = ""

# Wizard starting with origin country
    while True:
      self.cur.execute("SELECT CountryCode, Name FROM Country")
      countries = self.cur.fetchall()
      for i, country in enumerate(countries, start = 1):
        print(f"{i}. {country[1]}" )
      print("\nEnter B to return to the main menu. \n")
      choice = input("Enter the country the flight is flying from: ")
      if choice.upper() == "B":
        return
      try:
        choice = int(choice)
        if 1<= choice <= len(countries):
          origincountry = countries[choice - 1][0]
          break
        print("please choose a valid option.")
      except ValueError:
        print("Please enter a number.")

# Wizard Assigning Origin Airport
    while True:
      self.cur.execute("SELECT AirportID, AirportName, CountryCode, Name FROM Airport WHERE CountryCode = ?",(origincountry))
      airport = self.cur.fetchall()
      for i, airport in enumerate(airport, start = 1):
        print(f"{i}. {airport[1]}" )
      print("Enter B to return to the main menu. \n")
      choice = input("Enter the airport the flight is flying to: ")
      if choice.upper() == "B":
        return
      try:
        choice = int(choice)
        if 1<= choice <= len(countries):
          airportid = airport[choice - 1][0]
          newFlight.set_Flight_origin(newFlight,airportid[choice-1][0])
          break
        print("please choose a valid option.")
      except ValueError:
        print("Please enter a number.")
  
    while True:
# Wizard Destination country
      self.cur.execute("SELECT CountryCode, Name FROM Country")
      countries = self.cur.fetchall()
      for i, country in enumerate(countries, start = 1):
        print(f"{i}. {country[1]}" )
      print("\nEnter B to return to the main menu. \n")
      choice = input("Enter the country the flight is flying to: ")
      if choice.upper() == "B":
        return
      try:
        choice = int(choice)
        if 1<= choice <= len(countries):
          destinationcountry = countries[choice - 1][0]
          break
        print("please choose a valid option.")
      except ValueError:
        print("Please enter a number.")

# Wizard Assigning Destination Airport not including the orgin airport
    while True:
      self.cur.execute("SELECT AirportID, AirportName, CountryCode, Name FROM Airport WHERE CountryCode = ? AND AirportID != ?",(destinationcountry), (airportid))
      airport = self.cur.fetchall()
      for i, airport in enumerate(airport, start = 1):
        print(f"{i}. {airport[1]}" )
      print("Enter B to return to the main menu. \n")
      choice = input("Enter the airport the flight is flying to: ")
      if choice.upper() == "B":
        return
      try:
        choice = int(choice)
        if 1<= choice <= len(countries):
          airportid = airport[choice - 1][0]
          newFlight.set_flight_destination(newFlight,airportid[choice-1][0])
          break
        print("please choose a valid option.")
      except ValueError:
        print("Please enter a number.")

# Wizard Selecting Departure Date Time
    while True:
      print("Enter B to return to the main menu. \n")
      try:
        flight_date = input("Enter flight date (dd/MM/YYYY HH:MM): ")
        date_object = datetime.strptime(flight_date, "%d/%m/%Y %H:%M")
        break
      except ValueError:
        print("Please enter a valid date and time.")


# Wizard Selecting Plane - To simplify Ive gone with find planes that are at airports that havent been scheduled. 
    while True:
      self.cur.execute("SELECT PlaneID, TypeName, MaxPassengers, Name FROM Plane JOIN PlaneType ON Plane.TypeID = PlaneType.TypeID WHERE Location = ? AND PlaneID NOT IN (SELECT PlaneID FROM Schedule)", (self.flightorigin))
      plane = self.cur.fetchall()
      for i, plane in enumerate(plane, start = 1):
        print(f"{i}. {plane[1]} Passengers:{plane[2]}" )
      if len(plane) <= 0:
        restart = input("No planes avaliable at your location press any key to return to the main menu:  \n")
        return
      else:
        print("Enter B to return to the main menu. \n")
        choice = input("Enter the Plane: ")
      if choice.upper() == "B":
        return
      try:
        choice = int(choice)
        if 1<= choice <= len(plane):
          location = plane[choice - 1][0]
          break
        print("please choose a valid option.")
      except ValueError:
        print("Please enter a number.")


# Wizard Selecting The Captain - this could escalate to pilot location and rules to ensure adaquet rest is given preventing the pilot from being assigned to a flight
    while True:
      self.cur.execute("SELECT PilotID, Name, DoB FROM Pilot PilotID NOT IN (SELECT PilotID FROM Schedule WHERE (PlannedDepartureDateTime >= ? AND PlannedDepartureDateTime <= ?) OR (PlannedArrivalDateTime >= ? AND PlannedArrivalDateTime <= ?)", (self.planneddeparture),(self.plannedarrival),(self.planneddeparture),(self.plannedarrival))
      pilot = self.cur.fetchall()
      for i, pilot in enumerate(pilot, start = 1):
        print(f"{i}. {pilot[1]}")
      if len(pilot) <= 0:
        restart = input("No pilots available press any key to return to the main menu:  \n")
        return
      else:
        print("Enter B to return to the main menu. \n")
        choice = input("Enter the Pilot for Captain: ")
      if choice.upper() == "B":
        return
      try:
        choice = int(choice)
        if 1<= choice <= len(pilot):
          captain = pilot[choice - 1][0]
          break
        print("please choose a valid option.")
      except ValueError:
        print("Please enter a number.")


# Wizard Selecting The First Officer - this could escalate to pilot location and rules to ensure adaquet rest is given preventing the pilot from being assigned to a flight
    while True:
      self.cur.execute("SELECT PilotID, Name, DoB FROM Pilot PilotID NOT IN (SELECT PilotID FROM Schedule WHERE (PlannedDepartureDateTime >= ? AND PlannedDepartureDateTime <= ?) OR (PlannedArrivalDateTime >= ? AND PlannedArrivalDateTime <= ?)", (self.planneddeparture),(self.plannedarrival),(self.planneddeparture),(self.plannedarrival))
      pilot = self.cur.fetchall()
      for i, pilot in enumerate(pilot, start = 1):
        print(f"{i}. {pilot[1]}")
      if len(pilot) <= 0:
        restart = input("No pilots available press any key to return to the main menu:  \n")
        return
      else:
        print("Enter B to return to the main menu. \n")
        choice = input("Enter the Pilot for First Officer: ")
      if choice.upper() == "B":
        return
      try:
        choice = int(choice)
        if 1<= choice <= len(pilot):
          FirstOfficer = pilot[choice - 1][0]
          break
        print("please choose a valid option.")
      except ValueError:
        print("Please enter a number.")

#Write code for displaying the Shedule item created and offer the user to submit or cancel the record.

    



  def insert_data(self):
    try:
      self.get_connection()

      flight = Schedule()
      flight.set_flight_id(int(input("Enter FlightID: ")))

      self.cur.execute(self.sql_insert, tuple(str(flight).split("\n")))

      self.conn.commit()
      print("Inserted data successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def select_all(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_select_all)
      result = self.cur.fetchall()

      # think how you could develop this method to show the records

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def search_data(self):
    try:
      self.get_connection()
      flightID = int(input("Enter FlightNo: "))
      self.cur.execute(self.sql_search, tuple(str(flightID)))
      result = self.cur.fetchone()
      if type(result) == type(tuple()):
        for index, detail in enumerate(result):
          if index == 0:
            print("Flight ID: " + str(detail))
          elif index == 1:
            print("Flight Origin: " + detail)
          elif index == 2:
            print("Flight Destination: " + detail)
          else:
            print("Status: " + str(detail))
      else:
        print("No Record")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def update_data(self):
    try:
      self.get_connection()

      # Update statement

      if result.rowcount != 0:
        print(str(result.rowcount) + "Row(s) affected.")
      else:
        print("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()


# Define Delete_data method to delete data from the table. The user will need to input the flight id to delete the corrosponding record.

  def delete_data(self):
    try:
      self.get_connection()

      if result.rowcount != 0:
        print(str(result.rowcount) + "Row(s) affected.")
      else:
        print("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()


class Schedule:

  def __init__(self, FlightID, Status, Captain, FirstOfficer, FromAirport, ToAirport, PlaneID, PlannedArrivalDateTime, PlannedDepartureDateTime, ActualArrivalDateTime, ActualDepartureDateTime ):
    self.flightID = FlightID
    self.flightOrigin = FromAirport
    self.flightDestination = ToAirport
    self.status = Status
    self.captain = Captain
    self.firstofficer = FirstOfficer
    self.planid = PlaneID
    self.plannedarrival = PlannedArrivalDateTime
    self.planneddeparture = PlannedDepartureDateTime
    self.actualarrival = ActualArrivalDateTime
    self.actualdeparture = ActualDepartureDateTime


  def set_flight_id(self, flightID):
    self.flightID = flightID

  def set_flight_origin(self, flightOrigin):
    self.flightorigin = flightOrigin

  def set_flight_destination(self, flightDestination):
      self.flightdestination = flightDestination

      
  def set_departureDateTime(self, departureDateTime):
      self.planneddeparture = departureDateTime
      self.cur.execute('''SELECT TotalTravelTimeMins FROM JourneyTime WHERE OriginID = ? AND DestinationID = ?''',(self.flightorigin,self.flightdestination))
      traveltime = self.cur.fetchone()[0]
      self.plannedarrival = self.planneddeparture + datetime.timedelta(minutes = traveltime)


  def set_status(self, status):
    self.status = status

  def get_flight_id(self):
    return self.flightID

  def get_flight_origin(self):
    return self.flightOrigin

  def get_flight_destination(self):
    return self.flightDestination

  def get_status(self):
    return self.status

  def __str__(self):
    return str(
      self.flightID
    ) + "\n" + self.flightOrigin + "\n" + self.flightDestination + "\n" + str(
      self.status)




# The main function will parse arguments.
# These argument will be defined by the users on the console.
# The user will select a choice from the menu to interact with the database.
db_ops = DBOperations()


while True:
  print("\n Menu:")
  print("**********")
  print(" 1. Add a New Flight")
  print(" 2. View Flights by Criteria")
  print(" 3. Update Flight Information")
  print(" 4. Assign Pilot to Flight")
  print(" 5. View Pilot Schedule")
  print(" 6. View/Update Destination Information")
  print(" 7. Exit\n")

  __choose_menu = int(input("Enter your choice: "))
  if __choose_menu == 1:
    db_ops.addNewFlight()
  elif __choose_menu == 2:
    db_ops.insert_data()
  elif __choose_menu == 3:
    db_ops.select_all()
  elif __choose_menu == 4:
    db_ops.search_data()
  elif __choose_menu == 5:
    db_ops.update_data()
  elif __choose_menu == 6:
    db_ops.delete_data()
  elif __choose_menu == 7:
    exit(0)
  else:
    print("Invalid Choice")
