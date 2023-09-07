import sqlite3

class Database():
    def __init__(self, dbname) -> None:
        self.dbname = dbname
        self.connection = sqlite3.connect(self.dbname)
        self.cursor = self.connection.cursor()
        # 2 tables: first one is guests: guests have a name, age, and group, andd also 
        # an id that is automatically generated (auto increment, primary key)
        # second table is tables: tables have an id, a current occupancy, and an array of integers (foreign keys)
        # that represent the guests at the table
        self.cursor.execute("CREATE TABLE IF NOT EXISTS guests (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, groupname TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tables (id INTEGER PRIMARY KEY AUTOINCREMENT, groupname TEXT, occupancy INTEGER, guests TEXT)")
        self.connection.commit()

    def add_guest(self, guestarray) -> None:
        # insert if not already present
        self.cursor.execute("SELECT * FROM guests WHERE name=? AND age=? AND groupname=?", (guestarray[0], guestarray[1], guestarray[2]))
        if len(self.cursor.fetchall()) == 0:
            self.cursor.execute("INSERT INTO guests (name, age, groupname) VALUES (?, ?, ?)", (guestarray[0], guestarray[1], guestarray[2]))
            self.connection.commit()

    def new_table(self, first_guest):
        self.cursor.execute("INSERT INTO tables (groupname, occupancy, guests) VALUES (?, ?, ?)", (first_guest[3], 1, "".join(first_guest[0])))
        self.connection.commit()
    
    def get_tables_by_group(self, groupname):
        self.cursor.execute("SELECT * FROM tables WHERE groupname=?", (groupname,))
        return self.cursor.fetchall()
    
    def add_guest_to_table(self, table_id, guest_id):
        self.cursor.execute("SELECT * FROM tables WHERE id=?", (table_id,))
        table = self.cursor.fetchall()[0]
        guests = table[3].split(",")
        guests.append(str(guest_id))
        self.cursor.execute("UPDATE tables SET occupancy=?, guests=? WHERE id=?", (table[2] + 1, ",".join(guests), table_id))
        self.connection.commit()

    def get_guests(self):
        self.cursor.execute("SELECT * FROM guests")
        return self.cursor.fetchall()
