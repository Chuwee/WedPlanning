''' Wedding Planner 

    Project description: takes a wedding invitation list and creates a seating chart, 
    a list of guests, and a list of tables.
'''

# Imports
import random
import sqlite3
from wed_database.wed_database import Wed_Database as Database
from file_parser.file_parser import Parser
from seater.seater import Seater
from chatter.chatter import Chatter
from whisperer.whisperer import Whisperer

DB_NAME = "database.db"

# Functions
def init_db(database, parser : Parser) -> None:
    while True:
        guest = parser.next_guest()
        if guest == None:
            break
        database.add_guest(guest)


def main():
    print("Welcome to the Wedding Planner!")
    print("Please enter the name of the file containing the guest list.")
    filename = input("Filename: ")
    print("Great, checking...")
    # # Check if file exists
    try:
        #whisperer = Whisperer(filename)
        parser = Parser(filename)
    except FileNotFoundError:
        print("File not found. Please try again.")
        return
    print("File found!")
    db = Database(DB_NAME)

    #whisperer.run_whisper()

    # Parse file
    init_db(db, parser)
    #agent = Chatter(db)
    seater = Seater(5, 4, db)
    #print(agent.run_conversation())
    seater.run()


main()