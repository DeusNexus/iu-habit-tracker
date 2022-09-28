# IU INTERNATIONAL UNIVERSITY OF APPLIED SCIENCES
## Habit Tracker for Object Oriented and Functional Programming with Python (DLBDSOOFPP01)
A python habit tracker command-line application that uses `questionary` for a better UX and `SQLite` as database.

## Purpose
The habit tracker provides users with a simple easy tool that can be run on any platform that has access to python 3.
For compatibility reasons and keeping the appliciation lightweight the choice was made to serve it within the command-line interface which is even available on operating systems that do not have a graphical user interface.

Users can easily track their habits by creating or logging in to their own user-profile and then proceed to create, manage and view their habits in an organized and accessible manner. In this way it is easy to keep track of personal progress with the use of analytics that show habit streaks, best performing and worst performing, and more.

# Development Planning - UML Schemas
## Class Diagram
![Alt text](Images/UML.jpg?raw=true "UML Class Diagram")
### Updates
28 September 2022: Removed functionality for email push notifications, for the scope of the project it would require daemon process to keep running in background to check if certain dates are already met and then send the push notifications. This however is no longer supported and can be considered removed.
## Flow Diagram
![Alt text](Images/Flow-Diagram.jpg?raw=true "UML Flow Diagram")

# How To Get Started
## Dependencies
Python 3.7+
## Installation Instruction
## Run The Application
Use docker? Or use python __main__.py?

# User interface
## Welcome Screen
After the application is started from the command-line the welcome screen will greet the user with total amount of registered users, datetime and general title screen.
Options will be given of what the user can do next, which include creating a new user if someone doesn't yet have an account or logging in to one of the already registered users using the correct password.
### Create User
The new user will be asked to provide a unique username and password for his account. Optionally an email account can be registered where push notification will be send to if a deadline is about to expire or has failed. 
(NOTE TO SELF, THIS REQUIRES SOME DAEMON PROCESS TO RUN..)
### Login Existing User
Choosing one of the registered users will ask you to provide the password. One can try again if it was wrong or choose to exit.
## User Screen
After successfull authentication the (new) user will be brought to the user screen which displays the current amount of active and inactive habits for the user, the next earliest deadline for all active habits and a wide variety of options including; View, Create, Edit, Delete, Export/Import, Reset, Credits and Logout & Exit.
### View
In the view screen one can display all habits, individual habits or filter by certain criteria for more specific grouping/matching.
### Create
Creating habits is easily done in the create screen. The user selects whether a regular or dynamic habit has to be created and step-wise is asked to provide mandatory information and/or can optionally add other features if desired.
### Edit
In case one wants to change features of a Habit like title, description, interval, etc. then this can be done in the edit screen. A habit is simply selected from a list of all active and inactive habits and then the feature to be changed is selected and a new value is provided by the user.
### Delete
The delete screen offers functionality to remove a habit by selecting it from the list. After selecting the habit it will be permanently deleted from the user account.
### Export/Import
One can also choose to export the user account and this will generate a JSON file containing the user data. The data can be imported again on another device using the Habit Tracker application and choosing import. Now the user has to select the JSON file, which ideally is located in the same folder as the Habit Tracker and also provide the user password to decrypt the account. The account will then be added to the local user accounts and can be logged in to with all history of habits and checkins.
### Reset
The option to completely or partially reset the user account is possible. Complete reset will do a clean slate wipe and leave nothing behind. Partial reset will clean everything and then load example data into the user account.
### Credits
Feeling interested in who created the Habit Tracker application? See the credits and enjoy.
### Logout & Exit
The application will terminate and provide you with a goodbye message after selecting this option from the user screen menu.

# Disclaimer
The developed application is licensed under the GNU General Public License.