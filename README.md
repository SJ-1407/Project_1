# Project_1
This is code sample for my MLH fellowship application.

Instructions to arrange the files in corresponding folders
1. Create a  folder named "__pycache__"
    1. Move the following files inside __pycache__:
    2. config.cpython-311.pyc
    3. controllers.cpython-311.pyc
    4. database.cpython-311.pyc
    5.  models.cpython-311.pyc

2. Create a  folder named  "application"
    1. Move the  __pycache__ folder inside application folder
    2.  Move the following files inside application:
    3.  config.py
    4.  controllers.py
    5.  database.py
    6.   models.py

3. Create a  floder named "instance"
   1. Move the file db.sqlite3 inside instance

4. Create a folder named "templates"
   1.  Move all the filed with ".html" extension inside templates 
       
 After creating the folders and moving all files as per the instructions follow the below instructions.   
 You can look at the screenshot images for reference.

Instructions to run the server
1. cd into the current folder
2. run "python -m venv env"
3. run "env\Scripts\activate.bat" if in Windows, else run "source env/bin/activate".
4. run "pip install -r requirements.txt"
5. run "python Code/main.py"

Also if you wish to use a new database , you can delete the database provided , and just run again the main.py and database would be created. But , you need to make sure that you explicitly insert two rows into the role  table which are:
1. (1,'admin','can create ,update and delete events and venues')
2. (2,'user','can book events and venues')
The last value in both the rows defines the description of the role 
You can insert the rows using db , or using any database application.

You can just simply add data in the existing database as well

P.S. - You may not like the user-interface , as I was focusing more on the backend.
