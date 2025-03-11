client instructions
===================
commands list:
-------------
- register(url): register a new user, it will ask you to type in a username, email, password
- login(url): login with a user and password, by default the client uses the BASE_URL which is hard coded into the file for convenience, but if login is given a valid URL as an argument, it will try to log in to that instead.
- logout: logs out from the using the BASE_URL, since the base url is a global variable itll save what url you are using, weather a new one via the login arguments or the default one.
- list: list all the modules in the db
- view: view all the professors and their ratings in the db 
- average (professor_code, module_code): get a professors average rating in a certain module.
- rate (professor_code, module_code, year, semester, rating): submit a professor rating
- help: prints out all valid commands
- exit: exits the programme 

===========================================================
python anywhere domain: https://fy21sta.pythonanywhere.com/
===========================================================

--------
API info
--------
admin account: user: admin, password:123
most if not all the acounts also have a password that is 123

--------------------------
requirements to run client
--------------------------

please run pip install -r requirements.txt
which can be found in the main project dir