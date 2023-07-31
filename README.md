# Project_1
This is code sample for my MLH fellowship application.
Instructions to run the server
1. cd into the current folder
2. run "python -m venv env"
3. run "env\Scripts\activate.bat" if in Windows, else run "source env/bin/activate".
4. run "pip install -r requirements.txt"
5. run "python Code/main.py"

Also if you wish to use a new database , you can delete the database provided , and just run again the main.py and database would be created. But , you need to make sure that you explicitly insert two rows into the role  table which are:
(1,'admin','can create ,update and delete events and venues')
(2,'user','can book events and venues')
The last value in both the rows defines the description of the role 
You can insert the rows using db , or using any database application.

You can just simply add data in the existing database as well

P.S. - You may not like the user-interface , as I was focusing more on the backend.
