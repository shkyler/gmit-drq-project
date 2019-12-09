# GMIT Data Representation Project - 2019
This repository contains all of the documentation for my project for the Data Representation module of the GMIT Data Analytics program. This README serves as the documentation for the project. The project is a simple room booking system that could be used by an educational institution to manage its rooms.

## Accessing the project

The best way to access the code for this project is to clone the repository from Github:

```
git clone https://github.com/shkyler/gmit-drq-project.git
```

The project is currently hosted live and can be viewed and tested by clicking <a href="http://shkyler.pythonanywhere.com/bookings.html">here</a>.

## Database Schema

The data for this project is stored and managed using a MySQL database. The database has two tables, one which maintains a register of the rooms, the other maintains a register of the bookings. The `rooms` table can be described as follows:

<img src="https://raw.githubusercontent.com/shkyler/gmit-drq-project/master/img/descRooms.png">

The `rooms` table can be created in MySQL with the following query:

```
CREATE TABLE `rooms` 
(
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `colour` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
)
```
The `bookings` table can be described as follows:

<img src="https://raw.githubusercontent.com/shkyler/gmit-drq-project/master/img/descBookings.png">

The `bookings` table can be created in MySQL with the following query:

```
CREATE TABLE `bookings` (
  `roomID` int(5) NOT NULL,
  `dateRequired` varchar(255) NOT NULL,
  `userName` varchar(255) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UC_Bookings` (`roomID`,`dateRequired`),
  CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`roomID`) REFERENCES `rooms` (`id`)
)
```
Note the UNIQUE KEY on roomID and dateRequired - MySQL will handle duplicate bookings and will not allow them. Also there is a FOREIGN KEY CONSTRAINT linking the `roomID` in the `bookings` table to the `id` of the `rooms` table.

## Overview of the project

1. The data is stored in a MySQL database.
1. The database queries are defined using the `bookingsDAO.py` database access object.
1. The `appserver.py` application server calls the queries and returns the results as JSON objects.
1. AJAX calls are made in the `bookings` and `roomviewer` html files and the results are displayed in nice tables in web browser.


## Instructions for running the project

1. Clone the repository.
1. Create a MySQL database called `bookings` with the 2 tables as described above.
1. Edit the `dbconfigtemplate.py` file adding your MySQL host, database, user and password information.
1. Create a virtual environment, and use `pip` to install the dependancies from the `requirements.txt` file.
1. Set `appserver.py` as the FLASK_APP and run flask.
1. Using a web browser access `http://127.0.0.1:5000/bookings.html` (assuming you are using the local host to serve the website)



