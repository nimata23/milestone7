# CS321-Milestone5
<h2>Deployment to Cloud</h2>

## Installing dependencies

In order to run this Flask app, activate the virtual environment of your choice, then run:

`
pip install -r requirements.txt
`

This will install all the requirements needed to run the Flask app.

In order to actually run the app, navigate to the base repository directory. Your current directory should contain main.py. Run the following:

`
flask --app main run
`

The command line will output the port on which the website is running.

# Report

### Abstract: 
This milestone involved developing a dynamic version of our Athletic Management System to the cloud.  We relied on our work from Milestone 4 (Flask website) as a base for adding new functional features from our backlog.  This included using biometric data (and updating our graphs and tables to reflect this), and deploying our app to the cloud.  Our plan was (in the form of issues) as follows:
* Host the app on the cloud
* Use real data in the data base
* Refactor the format of our HTML files 
* Add fields to database objects
* Aggregate our data
* Use real data in our graphs and tables
* Revamp our sign up functionality


### Sprint Backlog:
#### User stories (general):
<p> update this once milestone is completed </p>
<p>As a user a can create a new account using an email and password – Completed<br>
As a user of the website I can log in to the website with a username and password – Completed<br>
As a user of the website I can login to my assigned role –Completed<br>
As a user of the website, I can navigate back to my dashboard by clicking on the mule icon – Partially completed (works for moving between athlete detail pages and dashboard)</p>

#### Admin/Peak:
<p>As an Admin, I can edit the permissions of all other users. – Started but unfinished<br>
As an Admin, I can view the sports science data (sleep, nutrition, readiness) of athletes and teams – Completed<br>
As an Admin, I can upload csv with the sport science data of our athletes, or add users – Partially completed (admin can upload data through CSV, but the data does not go into the database at this time)<br>
As an Admin, I can delete users accounts without deleting the user’s data – not implemented</p>

#### Athlete:
<p>As an Athlete, I can view graphs detailing my most recent sports science data (sleep, nutrition, readiness). – Completed (using dummy data) <br>
As an Athlete, I can view a graph showing changes in my sports science data over time. – Completed (using dummy data)<br>
As an Athlete, I can change the range of time over which I view changes in my sports science data.--not implemented<br>
As an Athlete, I can download a csv file of my sports science data.--not implemented<br>
As an Athlete, I can view detail pages on different aspects of my sports science data (sleep, readiness, calories) – Partially completed (can view detail pages, need to add graphs)<br>
As an Athlete, I can view notes on my readiness to play, sleep, and nutrition.--Completed</p>

#### Coach
<p>As a Coach, I can view sports science data from athletes on my teams –Completed<br>
As a Coach, I can choose which of my teams I wish to view– not implemented<br>
As a Coach, I can navigate to an athlete’s individual page by clicking on their profile – Completed<br>
As a Coach, I can see graphs showing changes in sports science data over time (readiness, sleep, nutrition) –Partially completed (Have plots, but they wouldn’t load in detailed athlete pages)<br>
As a Coach, I can download csvs of my athlete’s sports science data? –not implemented</p>

### Results: 


### Burn Down Chart:


### Team Reflection: 


### Contribution List: 
* Calvin: 
* Ben: 
* Matt: 
* Hannah: 
* Milo: 
* Tamsin: 
* Nicole: 

### Extensions: 
We added a functional ReadMe file to our repository detailing the website.

### References: 
Naser Al Madi


## Uploading files

CSV files can be uploaded from the path `"/upload"`. An uploaded file will be automatically parsed and ingested into the database. In order for the file to be properly parsed and inserted, the following conventions must be followed:

- The filename must be in `{"user.csv", "nutrition.csv", "recovery.csv", "sleep.csv"}`. Uploaded files currently overwrite the previous csv of the same name; this should be changed in a later version.
- The csv file must contain the correct column labels.
