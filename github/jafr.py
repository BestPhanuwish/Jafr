import os
import sys
import json
from datetime import datetime, timedelta
import re
from typing import List

from my_class import Task
from my_class import Meeting
from my_class import User

# constant
instruction = """What would you like to do?
1. Complete tasks
2. Add a new meeting.
3. Share a task.
4. Share a meeting.
5. Change Jafr's master directory.
6. Exit"""

# check if able to transform string into date time object accorded to format
def is_valid_date(date_str, format) -> bool:
    try:
        datetime.strptime(date_str, format)
        return True
    except Exception:
        return False

# check if description is empty, contains only white space, or had word "Scheduled:" in it
def is_valid_meeting_description(meeting_str) -> bool:
    if len(meeting_str) == 0 or meeting_str.isspace() or "Scheduled:" in meeting_str.split():
        return False
    return True

# check list of ids and see if all of them are match the existed id
def is_valid_set_of_ids(other_users: List[User], userIds: List[str]) -> bool:
    if len(userIds) == 0:
        return False
    for id in userIds:
        isLegitId = False
        for user in other_users:
            if id == user.user_id:
                isLegitId = True
                break
        if not isLegitId:
            return False
    return True

# This function is useful for testing with specific time
def get_datetime_now() -> datetime:
    # if user provide second argument, then we use that as a current date
    if len(sys.argv) == 3 and is_valid_date(sys.argv[2], "%d/%m/%y"):
        return datetime.strptime(sys.argv[2], "%d/%m/%y")
    else:
        return datetime.now()

def is_today(time: datetime) -> bool:
    # Compare between today's date and the parameter
    return get_datetime_now().date() == time.date()

def is_upcoming_days(time: datetime, upcoming_day: int) -> bool:
    # Get the current date
    current_date = get_datetime_now().date()

    # Calculate the date range from tomorrow to the next three days
    tomorrow = current_date + timedelta(days=1)
    three_days_later = current_date + timedelta(days=upcoming_day)
    
    # return whether if time is within the date range
    return tomorrow <= time.date() <= three_days_later

def get_user_setting_file_name() -> str:
    # Normally this should be home directory, but this is just a simulation so it's inside current directory
    if os.path.exists(os.path.expanduser("~") + "/.jafr/user-settings.json"):
        return os.path.expanduser("~") + "/.jafr/user-settings.json"
    else:
        return os.path.expanduser(".") + "/.jafr/user-settings.json"

def get_user_by_id(id, other_users) -> User:
    for user in other_users:
        if user.user_id == id:
            return user

def print_reminder(tasks: List[Task], meetings: List[Meeting]):
    # print tasks that due today
    print("Just a friendly reminder! You have these tasks to finish today.")
    for task in tasks:
        if (is_today(task.time) and not task.completed):
            task.printf(start_with="- ")
    print()
            
    # print tasks that due in upcoming 3 days
    print("These tasks need to be finished in the next three days!")
    for task in tasks:
        if (is_upcoming_days(task.time, 3) and not task.completed):
            task.printf(start_with="- ", print_with_date=True)
    print()
    
    # print meeting that happening today
    print("You have the following meetings today!")
    for meeting in meetings:
        if (is_today(meeting.time)):
            meeting.printf(start_with="- ")
    print()
      
    # print meeting that will happen in upcoming 7 days
    print("You have the following meetings scheduled over the next week!")
    for meeting in meetings:
        if (is_upcoming_days(meeting.time, 7)):
            meeting.printf(start_with="- ", print_with_date=True)
    print()

def complete_task_in_file(task: Task, setting_data: dict):
    # update the task file by complete specific task
    try:
        # open file for read and write format
        fileName = setting_data["master"] + "/tasks.md"
        fTasks = open(fileName, "r+")
        
        # read all the contents from the file
        texts = fTasks.readlines()
        
        # get the line that's match the line index of current task
        prev_text = texts[task.index]
        
        # change from not complete to complete 
        # might be an edge case where task description contains "not complete" word (too lazy to handle it)
        texts[task.index] = re.sub("not complete", "complete", prev_text)
        
        # write new modified texts to file and close
        fTasks.seek(0)
        fTasks.writelines(texts)
        fTasks.truncate() # apperently need this function to prevent bug
        
        fTasks.close()
        
    except FileNotFoundError:
        sys.stderr.write("Missing tasks.md or meetings.md file.\n")
        return

def add_meeting_in_file(new_meeting: Meeting, setting_data: dict):
    # add meeting to file
    try:
        # open file for append format
        fileName = setting_data["master"] + "/meetings.md"
        fMeetings = open(fileName, "a")
        
        # add new content in the file
        fMeetings.write("\n")
        fMeetings.write("##### added by you\n")
        fMeetings.write(f"- {new_meeting.description} Scheduled: " + new_meeting.time.strftime("%H:%M %d/%m/%y") + "\n")
        
        fMeetings.close()
        
    except FileNotFoundError:
        sys.stderr.write("Missing tasks.md or meetings.md file.\n")
        return
    
def share_task(task: Task, path: str, setting_data: dict):
    # add meeting to file
    try:
        # open file for append format
        fileName = setting_data["master"] + "/tasks.md"
        fTasks = open(fileName, "r")
        fTasksOther = open(path + "/tasks.md", "a")
        
        # add new content in the file
        fTasksOther.write("\n")
        fTasksOther.write(f"##### shared by {os.environ['USER']}\n")
        fTasksOther.write(fTasks.readlines()[task.index])
        
        fTasks.close()
        fTasksOther.close()
        
    except FileNotFoundError:
        sys.stderr.write("Missing tasks.md or meetings.md file.\n")
        return

def share_meeting(meeting: Meeting, path: str):
    # add meeting to file
    try:
        # open file for append format
        fMeetingsOther = open(path + "/meetings.md", "a")
        
        # add new content in the file
        fMeetingsOther.write("\n")
        fMeetingsOther.write(f"##### shared by {os.environ['USER']}\n")
        fMeetingsOther.write(f"- {meeting.description} Scheduled: " + meeting.time.strftime("%H:%M %d/%m/%y") + "\n")
        
        fMeetingsOther.close()
        
    except FileNotFoundError:
        sys.stderr.write("Missing tasks.md or meetings.md file.\n")
        return


def main():
    
    # declare global variable
    
    tasks = [] # type -> List<Task>
    meetings = [] # type -> List<Meeting>
    other_users = [] # type -> List<User>
    setting_data = {} # json data of master directory which contains tasks and meetings
    
    # get the master directory
    try:
        # get master directory from json
        fileName = get_user_setting_file_name()
        fSetting = open(fileName, "r")
        setting_data = json.load(fSetting)
        fSetting.close()
        
        # edge case if we can't get directory from json
        master_file = os.path.expanduser(setting_data["master"])
        if master_file == None or not os.path.exists(master_file):
            raise FileNotFoundError()
    except FileNotFoundError:
        sys.stderr.write("Jafr's chosen master directory does not exist.\n")
        return
    
    # read the content in tasks file and store it in the list
    try:
        fileName = setting_data["master"] + "/tasks.md"
        fTasks = open(fileName, "r")
        
        for index, line in enumerate(fTasks):
            # remove the indentation
            line = re.sub(r"^\s*-", "-", line)
            
            # if it start with "- "", contains word "Due:" and "complete" then we considerate it
            if re.search(r"^-\s.*Due:.*complete", line):
                
                # split between 2 parts [description, time&status]
                splited = line.strip().split(" Due: ")
                
                # split again between time and status [time, status]
                splitedAgain = splited[1].split(" ", 1)
                
                # edge case when time or status is not in the right format, we skip it
                if (not is_valid_date(splitedAgain[0], "%d/%m/%y") or (splitedAgain[1] != "complete" and splitedAgain[1] != "not complete")):
                    continue
                
                # add new task that just read from the file to list of task object
                tasks.append(Task(
                    line_index = index, # get file line index (useful for modify file in the future)
                    description = splited[0][2:], # get the description
                    time = splitedAgain[0], # get the date
                    status = splitedAgain[1] # get the status
                ))
                
        fTasks.close()
        
    except FileNotFoundError:
        sys.stderr.write("Missing tasks.md or meetings.md file.\n")
        return
    
    # read the content in meetings file and store it in the list
    try:
        fileName = setting_data["master"] + "/meetings.md"
        fMeetings = open(fileName, "r")
        
        for line in fMeetings:
            # remove the indentation
            line = re.sub(r"^\s*-", "-", line)
            
            # if it start with "- "" and contains word "Scheduled:"" then we considerate it
            if re.search(r"^-\s.*Scheduled:.*", line):
                
                # split between 2 parts [description, time]
                splited = line.strip().split(" Scheduled: ")
                
                # edge case when date and time is not in the right format, we skip it
                if (not is_valid_date(splited[1], "%H:%M %d/%m/%y")):
                    continue
                
                # add new meeting that just read from the file to list of meeting object
                meetings.append(Meeting(
                    description = splited[0][2:], # get the description
                    time = splited[1], # get the time and date
                ))
        
        fMeetings.close()     
                
    except FileNotFoundError:
        sys.stderr.write("Missing tasks.md or meetings.md file.\n")
        return
    
    # read and translate data from passwd to raw data
    try:
        fPasswd = open(sys.argv[1], "r")
        
        for line in fPasswd:
            # split each info by ":"
            infos_str = line.strip().split(":")
            
            # if user is not your own then store it in the list
            if os.environ['USER'] != infos_str[0]:
                # add new user to the list with nescessary info
                other_users.append(User(
                    username = infos_str[0],
                    user_id = infos_str[2],
                    home_dir = infos_str[5]
                ))
        
        fPasswd.close()     
                
    except FileNotFoundError:
        sys.stderr.write("Missing passwd file.\n")
        return
    
    # greet the user
    print_reminder(tasks, meetings)
    print(instruction)
    
    # loop ask user question until they quit
    quit = False
    while not quit:

        answer = input()
        
        match answer:
            
            case "1": ## Complete tasks
                # if every tasks are complete then exit the function
                allTaskAreComplete = True
                for task in tasks:
                    if not task.completed:
                        allTaskAreComplete = False
                        break
                if allTaskAreComplete:
                    print("No tasks to complete!")
                    print(instruction)
                    continue
                
                # ask for task to complete
                print("Which task(s) would you like to mark as completed?")
                taskDict = {} # will need this to translate task num now to real task index in list
                taskNum = 0
                for index, task in enumerate(tasks):
                    if (not task.completed):
                        taskNum += 1
                        taskDict[taskNum] = index
                        task.printf(start_with=f"{taskNum}. ", print_with_date=True)
                
                # keep asking until get the correct input
                targetTasks = None
                isValid = False
                while not isValid:
                    targetTasks = input().split()
                    
                    # loop check if all target task number are valid
                    isValid = True
                    for targetTask in targetTasks:
                        if not targetTask.isdigit() or int(targetTask) > taskNum or int(targetTask) <= 0:
                            isValid = False
                            print(f"Please pick a sequence of number between 1-{taskNum}")
                            break
                
                # mark task to complete and update it to file
                for targetTask in targetTasks:
                    targetTask = int(targetTask)
                    taskIndex = taskDict[targetTask]
                    tasks[taskIndex].completed = True
                    complete_task_in_file(tasks[taskIndex], setting_data)
                
                print("Marked as complete.")
                print(instruction)
                
            case "2": ## Add a new meeting
                # keep asking for meething description until valid
                meetingDescription = None
                while True:
                    print("Please enter a meeting description:")
                    meetingDescription = input()
                    if is_valid_meeting_description(meetingDescription):
                        break
                
                # keep asking for meething date until valid
                meetingDate = None
                while True:
                    print("Please enter a date:")
                    meetingDate = input()
                    if is_valid_date(meetingDate, "%d/%m/%y"):
                        break
                    
                # keep asking for meeting time until valid
                meetingTime = None
                while True:
                    print("Please enter a time:")
                    meetingTime = input()
                    if is_valid_date(meetingTime, "%H:%M"):
                        break
                    
                print(f"Ok, I have added {meetingDescription} on {meetingDate} at {meetingTime}.")
                
                # add meething detail
                newMeeting = Meeting(
                    description = meetingDescription,
                    time = meetingTime + " " + meetingDate,
                )
                meetings.append(newMeeting)
                add_meeting_in_file(newMeeting, setting_data)
                
                # ask if user need to share meeting ask until valid answer
                isShare = input("Would you like to share this meeting? [y/n]: ")
                if isShare == "y":
                    # show available users to share
                    print("Who would you like to share with?")
                    for user in other_users:
                        print(f"{user.user_id} {user.username}")
                    
                    # keep asking for user ids to share until valid
                    userToShare = []
                    while True:
                        userIdsStr = input()
                        userIds = userIdsStr.split()
                        
                        if is_valid_set_of_ids(other_users, userIds):
                            userToShare = userIds
                            break
                        else:
                            print("Please enter all the valid sequence of user ids")
                        
                    # share the meeting to other users file
                    for userId in userToShare:
                        # get the directory where it store task.md
                        user = get_user_by_id(userId, other_users)
                        fileName = user.home_dir + "/.jafr/user-settings.json"
                        fSetting = open(fileName, "r")
                        path = json.load(fSetting)["master"]
                        fSetting.close()
                        
                        # update meeting into that user
                        share_meeting(newMeeting, path)
                    
                    print("Meeting shared.")
                
                print(instruction)
                
            case "3": ## Share a task
                # show available task
                print("Which task would you like to share?")
                for index, task in enumerate(tasks):
                    task.printf(start_with=f"{index+1}. ", print_with_date=True)
                
                # keep asking for task number until valid
                taskNum = None
                while True:
                    taskNum = input()
                    if taskNum.isdigit() and int(taskNum) > 0 and int(taskNum) <= len(tasks):
                        taskNum = int(taskNum)
                        break
                    print(f"Please enter the available task, between number 1-{len(tasks)}")
                    
                # show available users to share
                print("Who would you like to share with?")
                for user in other_users:
                    print(f"{user.user_id} {user.username}")
                
                # keep asking for user ids to share until valid
                userToShare = []
                while True:
                    userIdsStr = input()
                    userIds = userIdsStr.split()
                    
                    if is_valid_set_of_ids(other_users, userIds):
                        userToShare = userIds
                        break
                    else:
                        print("Please enter all the valid sequence of user ids")
                    
                # share the task to other users file
                for userId in userToShare:
                    # get the directory where it store task.md
                    user = get_user_by_id(userId, other_users)
                    fileName = user.home_dir + "/.jafr/user-settings.json"
                    fSetting = open(fileName, "r")
                    path = json.load(fSetting)["master"]
                    fSetting.close()
                    
                    # update task into that user
                    share_task(tasks[taskNum-1], path, setting_data)
                
                print("Task shared.")
                print(instruction)
                
            case "4": ## Share a meeting
                # show available meeting
                print("Which meeting would you like to share?")
                for index, meeting in enumerate(meetings):
                    meeting.printf(start_with=f"{index+1}. ", print_with_date=True)
                
                # keep asking for meeting number until valid
                meetingNum = None
                while True:
                    meetingNum = input()
                    if meetingNum.isdigit() and int(meetingNum) > 0 and int(meetingNum) <= len(meetings):
                        meetingNum = int(meetingNum)
                        break
                    print(f"Please enter the available meeting, between number 1-{len(meetings)}")
                    
                # show available users to share
                print("Who would you like to share with?")
                for user in other_users:
                    print(f"{user.user_id} {user.username}")
                
                # keep asking for user ids to share until valid
                userToShare = []
                while True:
                    userIdsStr = input()
                    userIds = userIdsStr.split()
                    
                    if is_valid_set_of_ids(other_users, userIds):
                        userToShare = userIds
                        break
                    else:
                        print("Please enter all the valid sequence of user ids")
                    
                # share the meeting to other users file
                for userId in userToShare:
                    # get the directory where it store task.md
                    user = get_user_by_id(userId, other_users)
                    fileName = user.home_dir + "/.jafr/user-settings.json"
                    fSetting = open(fileName, "r")
                    path = json.load(fSetting)["master"]
                    fSetting.close()
                    
                    # update meeting into that user
                    share_meeting(meetings[meetingNum-1], path)
                
                print("Meeting shared.")
                print(instruction)
                
            case "5": ## Change Jafr's master directory
                # ask for directory change
                print("Which directory would you like Jafr to use?")
                while True:
                    pathTarget = input()
                    # ask until path exist
                    if os.path.exists(pathTarget):
                        break
                    else:
                        print("path does not exist, try again")
                
                # store new path to json
                try:
                    # get master directory from json
                    fileName = get_user_setting_file_name()
                    fSetting = open(fileName, "w")
                    setting_data["master"] = pathTarget
                    json.dump(setting_data, fSetting)
                    fSetting.close()
                except FileNotFoundError:
                    sys.stderr.write("Jafr's chosen master directory does not exist.\n")
                    return
                print(f"Master directory changed to {pathTarget}.")
                print(instruction)
                
            case "6": ## Exit
                quit = True
                
            case _: ## if nothing is match
                print("Please pick number between 1-6")
    
    pass

if __name__ == '__main__':
    main()
