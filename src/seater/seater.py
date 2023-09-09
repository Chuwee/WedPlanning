from database.database import Database as d

class Seater():
    def __init__(self, max_seats, min_seats, database: d):
        self.max_seats = max_seats
        self.database = database
        self.min_seats = min_seats

    def first_seat(self, guest_array):
        # First, check if there are any tables that are not full and 
        # has the name of this guys group
        tables = self.database.get_tables_by_group(guest_array[3])
        # Add him into the first non full table
        # If there are no non full tables, create a new table and add him there
        for table in tables:
            if table[2] < self.max_seats:
                print("Adding guest " + str(guest_array[1]) + " to table " + str(table[0]))
                self.database.add_guest_to_table(table[0], guest_array[0])
                return
        self.database.new_table(guest_array)
    
    def check_seats(self, guest_array):
        tables = self.database.get_tables()
        not_good_tables = []
        for table in tables:
            if table[2] < self.min_seats:
                not_good_tables.append(table)
        # Good tables are tables without the not good tables
        good_tables = []
        for table in tables:
            if table not in not_good_tables:
                good_tables.append(table)
        return (tables, not_good_tables, good_tables)

    def run(self):
        guests = self.database.get_guests()
        for guest in guests:
            self.first_seat(guest)
        (tables, not_good_tables, good_tables) = self.check_seats(guests)
        if len(not_good_tables) > 0:
            print("There are tables with less than " + str(self.min_seats) + " people!")
        
