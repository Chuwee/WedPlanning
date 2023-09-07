class Parser():
    def __init__(self, filename) -> None:
        self.filename = filename
        self.file = open(self.filename, "r")
        self.lines = self.file.readlines()
        self.current_line = 0
        self.file.close()

    ''' File format: 
    Example:
    
    #
    Name: John Doe
    Age: 20
    Group: Friends
    #
    Name: Jane Doe
    Age: 20
    Group: Family
    #
    ...'''
    def next_guest(self) -> list:
        if self.lines[self.current_line] != "#\n":
            return None
        self.current_line += 1
        if self.current_line >= len(self.lines):
            return None
        guest = []
        for i in range(3):
            guest.append(self.lines[self.current_line].split(": ")[1].strip())
            self.current_line += 1
        return guest