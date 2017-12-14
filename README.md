# SI 507 F17 - Final Project

###this readme serves as a description and report of work done in my final project:

## Part1: Introduction

This final project aims to collect unversity rankings (top-100 national unversities) and other information from a website(US News Unversity Ranking Website), store them into a databse called si507_final_ywangdr, and visualize them on an interactive map.

## Part2: Steps to run the code
*0. this project uses python3.5, but any python3 verion should be fines.
*1. Clone the repo into a local directory. You should be able to see requirements.txt in that repo, which would be used later in 3.
*2. create a virtual environment (could be anywhere)
*3. install the virtual environment dependancies: pip install requirements.txt
*4. activate the virtual environment, and navigate to the repo
*5. all the credentials are stored in config.py, however, most of the keys are already filled for you, 
the only thing you need to do is that you need to make sure there exists a Postgres database on your lcal machine,
 and it should named exactly "postgres", with the user being "postgres" (usually this database was automatically created for you when you installed Postgres)
Now you need to copy the corresponding password of the database to db_password variable in config.py
Later the program will first connect to this database, and then create a new database called si507_final_ywangdr, then connect to the new database to do operations
*6. Do this if in step 5 you don't have a database called postgre, otherwise skip this step. You need to create a database yourself, then update db_name, db_user and db_password in config.py
*7. Now things have been set up, you could start running SI507F17_finalproject_tests.py first to check if everything works fine. In your virtual environment, type in: python /path/to/SI507F17_finalproject_tests.py
*8. All 15 test cases should pass.
*9. Now you could start running SI507F17_finalproject.py
*10. similar to 7, type in: python /path/to/SI507F17_finalproject_tests.py
*11. the code may run for a while (maybe a minute or two, or even longer). After it finishes, your web browser should be opened and you should be directed to a webpage on which shows the final visualization of the 100 unversities on map, move your mouse over the dots and you should be able to see the metadata of a unversity

