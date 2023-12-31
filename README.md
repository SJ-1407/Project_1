## Setup

1.Clone the repository:

    git clone -b master https://github.com/SJ-1407/Project_1.git  
    cd Project_1 
   
2.Create and activate a virtual environment:  

     python -m venv any_name     
     .\any_name\Scripts\activate   
  
3. Install dependencies:   
      First go to the directory Project_1
      cd path to Project_1
     then  install the requirements using the command

       pip install -r reqs.txt


5.  Run the app:    

        python app.py
    Or if you are using any code editor then simply run the app.py file

7. Make sure to change the database url present in database.py, if you want to add new users , events and venues from the begining or you can use the database provided , and add some users to experience the site.

8. It might be possible that for few attempts you may get a blank home page , that may be due to flask has not connected to the database yet , run the app.py file few times and it will get fixed. This would happen only in the case if you are using the existing database.

#The home page of web app will be available at http://127.0.0.1:5000.   

