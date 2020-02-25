## eventSignUpRestApp
a simple event app built in python/rest

## Project package dependencies
- Python: 3.8
- djangorestframework: 3.11.0
- django: 3.0.3
- djangorestframework-api-key: 1.4.1
- These dependencies are in the project pipfile/piplock files and can be installed using pipenv, details below.
- [pipfile](https://github.com/abeeshp/eventSignUpRestApp/blob/master/Pipfile)
- [pipfile.lock](https://github.com/abeeshp/eventSignUpRestApp/blob/master/Pipfile.lock)
- The project has [requirements.txt](https://github.com/abeeshp/eventSignUpRestApp/blob/master/requirements.txt) to use with pip

### Dependency Management
The proejct dependencies are managed using [pipenv](https://realpython.com/pipenv-guide/), read this to know more.

#### To install pipenv
- pip install pipenv or  on mac, brew install pipenv

##### Basic pipenv commands
- pipenv install - this uses the pipfile/piplock file to install the required packages.
- pipenv shell - spawns a shell in a virtual environment to isolate the development/run of this app

### Running the app/local server
- mkdir eventApp, cd eventApp
- git clone https://github.com/abeeshp/eventSignUpRestApp .
- pipenv install - this uses the pipfile/piplock file to install the required packages.
- pipenv shell - spawns a shell in a virtual environment to isolate the development/run of this app
- cd event_manager
- python manage.py runserver

If everything is good, then you,ll see something as below

------------------------------------------------------------  
(gitevent) bash-3.2$ python manage.py runserver  
Watching for file changes with StatReloader  
Performing system checks...  

System check identified no issues (0 silenced).  
February 24, 2020 - 18:30:49  
Django version 3.0.3, using settings 'event_manager.settings'  
Starting development server at http://127.0.0.1:8000/  
Quit the server with CONTROL-C.  

------------------------------------------------------------  

## Running tests
- follow steps under Running the app/local server, cd event_manager
- python manage.py test 

## Event Signups
- goto http://localhost:8000/eventsList/ to list the evets
- click Signup to goto the signup page to register for the event using emailId.


## Api endpoints
- The app uses fixed ApiKeys for managing events/signups
- Replace "**************" with the actual apiKey

### To get all the events
- GET http://127.0.0.1:8000/api/events/  "Authorization: Api-Key *********************"

### To get all signUps for an event
- event_id is the eventsUniqueID
- GET http://127.0.0.1:8000/api/registrationDetails/?event_id=event_id  "Authorization: Api-Key *********************"

### To sign up for the event
- event_id is the eventsUniqueID
- POST http://127.0.0.1:8000/api/registrations/ email=user5@maildom.com event=16 name=testuser2 " "Authorization: Api-Key *********************"

### To remove a signup from the event
- DELETE http://127.0.0.1:8000/api/registrations/signUp_id/  "Authorization: Api-Key *********************"

### To remove the Event
-  DELETE http://127.0.0.1:8000/api/events/event_id/  "Authorization: Api-Key *********************"

### To get all signupgs
- GET http://127.0.0.1:8000/api/registrations/ "Authorization: Api-Key *********************"


### settings/details
- the email details are in .settings 
- FROM_MAIL_ID,TO_MAIL_ID change this if needed.
- Change the password in the .settings to actual password
- the project already comes with pre-scheduled events with sqllite db.
- you can usee a lightweight [dbbrowser](https://sqlitebrowser.org/) to check the  details at backend.
- the uniqueId for both events/registrations is autocreated by the restframework models.
- uses gmail smtp to send mails, change this if you want to use something else.

