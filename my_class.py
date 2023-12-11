from datetime import datetime

"""
This class use date time Object implementation, to learn more about date time:
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
"""

class Meeting:
    def __init__(self, description, time) -> None:
        self.description = description
        self.time = datetime.strptime(time, "%H:%M %d/%m/%y")
        
    # this method had optional parameter to customise the message
    def printf(self, start_with, print_with_date=None) -> str:
        if print_with_date:
            print(start_with + self.description, "on", self.time.strftime("%d/%m/%y"), "at", self.time.strftime("%H:%M"))
        else:
            print(start_with + self.description, "at", self.time.strftime("%H:%M"))
            
        
class Task:
    def __init__(self, line_index, description, time, status) -> None:
        self.index = line_index
        self.description = description
        self.time = datetime.strptime(time, "%d/%m/%y")
        if status == "complete":
            self.completed = True
        elif status == "not complete":
            self.completed = False
    
    # this method had optional parameter to customise the message
    def printf(self, start_with, print_with_date=None) -> None:
        if print_with_date:
            print(start_with + self.description, "by", self.time.strftime("%d/%m/%y"))
        else:
            print(start_with + self.description)
            
class User:
    def __init__(self, username, user_id, home_dir) -> None:
        self.username = username
        self.user_id = user_id
        self.home_dir = home_dir