from database.database import Database as d

class Seater():
    def __init__(self, max_seats, database: d):
        self.max_seats = max_seats
        self.database = database

    def seat(self, guest_array):
        # First, check if there are any tables that are not full and 
        # has the name of this guys group
        tables = self.database.get_tables_by_group(guest_array[2])
        # Add him into the first non full table
        # If there are no non full tables, create a new table and add him there
        for table in tables:
            if table[2] < self.max_seats:
                self.database.add_guest_to_table(table[0], guest_array[0])
                return
        self.database.new_table(guest_array[2], guest_array[0])

    def run(self):
        guests = self.database.get_guests()
        for guest in guests:
            self.seat(guest)
