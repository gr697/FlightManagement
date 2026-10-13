# FlightManagement
Assignment 1 Databases and cloud
Flight Management System

------------------------------------------------------------------------------------------
Overview

The Flight Management System is a Python console-based application that uses SQLite to manage flight scheduling and operational data. The system allows users to create, update, search and delete flight records while maintaining relationships between aircraft, airports, countries, pilots and journey times.

The application was designed as a minimum viable flight scheduling solution to demonstrate relational database design, SQL query development, object-oriented programming and the implementation of operational business rules.

Features
Flight Management
Create new flights using a wizard-based interface.
View flights using multiple search criteria.
Update existing flight information.
Delete planned flights.
Store planned and actual departure and arrival times.
Manage flight status throughout the flight lifecycle.
Pilot Management
Assign Captains and First Officers to flights.
Prevent pilots from being allocated to overlapping flights.
View flights assigned to a specific pilot.
Remove pilot assignments from planned flights.
Aircraft Management
Allocate available aircraft to flights.
Prevent aircraft from being allocated to multiple active flights.
Automatically update aircraft location when flights are completed.
Display aircraft type and passenger capacity information.
Route Management
Calculate planned arrival times automatically.
Retrieve journey durations based on origin and destination airports.
Prevent origin and destination airports from being identical.

------------------------------------------------------------------------------------------
Workflow Management

Flights pass through the following workflow statuses:

Plain Text
Planned → Boarding → Departed → Landed → Complete

-------------------------------------------------------------------------------------------

Different editing permissions are available depending on the flight status.

Database Structure

The database consists of the following entities:

Country

Airport

PlaneType

Plane

Pilot

JourneyTime
 
Flight

------------------------------------------------------------------------------------------

Key Business Rules

Aircraft Availability

Aircraft can only be assigned when:

Located at the selected origin airport.
Not assigned to another active flight.
Assigned flights have reached a Complete status.
Pilot Availability

Pilots cannot be assigned when:

Already scheduled on an overlapping flight.
Already assigned to the opposite role on the same flight.
Flight Deletion

Flights may only be deleted when:

Plain Text
Status = Planned

This prevents loss of historical operational records.

Automatic Arrival Calculation

Planned arrival times are automatically calculated using:

Plain Text
Origin Airport
Destination Airport
Journey Duration
Running the Application

Ensure Python 3 is installed.

------------------------------------------------------------------------------------------

Save the source code as:

Plain Text
main.py
Run the application:
Shell
python main.py
The SQLite database will automatically be created:
Plain Text
FlightManagement.db
------------------------------------------------------------------------------------------
Sample data for:

Countries
Airports
Plane Types
Planes
Pilots
Flights
Journey Times

will be automatically loaded on first execution.

------------------------------------------------------------------------------------------

Main Menu
Plain Text
1. Add a New Flight
2. View Flights by Criteria
3. Update Flight Information
4. Delete/Assign Pilot on Flight
5. View Pilot Flight
6. View/Update Destination Information
7. Delete Flight
8. Exit