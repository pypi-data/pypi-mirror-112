##**SM - Module for Python programing language >= 3.6:**

##**CopyRight by Pascal Vallaster | all rights reserved**

###**Please report any errors to <pascalvallaster@gmail.com>**

###General Stuff:

####def quit()
 - Exits the current (main-)thread

####def clear()
 - Clears the terminal

####def sleep(sec)
 - Sleeps a certain time= sec: int

```
from sm import sleep
some_function_and_stuff()
sleep(5)
print("This program waited for 5 secounds")
```

####def check_input_int()
 - Checks if the entry from the user was an integer 


###Math Stuff:

####def fracture(
- Calculates a fracture; param p(bool) if for printing the result => True/False;
 - If division-zero error is raised it

####def check_int(nZ)
 - Checks if the param nZ is an int; param p(bool) if for printing the number => True/False;
 - Returns a bool

####def N(nZ)
 - Checks if param nZ is a natural number; param p(bool) if for printing the number => True/False;
 - Returns a bool

####def Nu(nZ)
 - Checks if param nZ is part of the uneven numbers; param p(bool) if for printing the number => True/False;
 - Returns a bool

####def Ne(nZ)
 - Checks if param nZ is part of even numbers; param p(bool) if for printing the result => True/False;
 - Returns a bool

####def P(nZ)
 - Checks if param nZ is part of the prime numbers; param p(bool) if for printing the result => True/False;
 - Returns a bool


###Hacking Stuff (aircrack-ng):

####def attack(bssid, interf)
 - Attacks the wifi with the given bssid and interf; can only be used with the program aircrack-ng or similar
one that accepts the same commands;
######--legal-disclaimer--
 - **Only use this function for good purposes - I am
not responsible for any damage that could happen if the function was executed!**


###DB Stuff:

####class IncorrectEntry(Exception)
 - Exception class in case the entry from some params is invalid; is raised by def check_vars()
```
from sm import dbworker
class db(dbworker):
    def __init__(self):
        super(db, self).__init__()
        
instance = db()
instance.INSERT(table:"table1", column:"column1")

-Execute Python-Script-
...
Incorrect entry for variable: value
Got 'NONE' instead  # Because 'value' must have a value, but it hasn't one => ERROR
    
```

####class dbworker

    => def INSERT()
    => def SELECT_ELEMETs()
    => def SELECT_ALL()
    => def  DELETE()
    => def UPDATE()
    => def getLastEntry()

 - See doc from dbworker itself, and the single functions in class dbworker._< function >_(); 
 - It's recommended to close the connection to the db before closing down the application => dbworker.close()


###XML Stuff:

####class XMLworker

    => def overwrite()
    => insert_element

 - See doc from XMLworker itself, and the single functions in class XMLworker._< function >_();


###JSON Stuff:

####class JSONworker

    => def write()

 - See doc from XMLworker itself, and the single functions in class JSONworker._< function >_();


####Mail Stuff:
- No doc


###Log Stuff:

####class logMaker
 - writes a log in a file with function writeLog()


###Color Stuff:

####class colors

    => RED = Fore.RED
    => BLUE = Fore.BLUE
    => CYAN = Fore.CYAN
    => WHITE = Fore.WHITE
    => BLACK = Fore.BLACK
    => GREEN = Fore.GREEN
    => YELLOW = Fore.YELLOW
    => MAGENTA = Fore.MAGENTA

    => RESET = Fore.RESET
    => BRIGHT = Style.BRIGHT
    => NORMAL = Style.NORMAL

 - See doc from package colorama itself


####Animations:

####def point_animation()
 - To animate three points "..." (loading symbol)

####def stick_animation()
 - To animate a rotating stick  (loading symbol)


###Copy-Paste Code:

- No Doc


###Main Stuff:

####main()

 - For handling the sys args if module is started with these