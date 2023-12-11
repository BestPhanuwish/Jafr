# How to run test

just type in the terminal command "bash run_test.sh"

# How does it works

when run the test using bash script
it will go throught every test inside tests/ directory
set the home user to each test directory
execute jafr.py with respective home directory
current home user will always be that test directory
current date will always be 01/08/23 for testing purpose

sometimes when testing, it will make changed to the file
which made testing more tedious since we need to reset the content of the file
I have come up with the solution to stored the original content of the file
to file named "tasks_origin.md" and "meetings_origin.md"
which every time when run test, it will reset the content by copy content
from the origin to current "task.md" and "meetings.md"

# What we are testing

There are 3 functionallity that had been test in this scaffold
1. Displaying reminders.
2. Completing tasks.
3. Adding new meetings.
Where each of the functionallity had been split into 3 different categories
- positive case (normal functionallity)
- negative case (alternate way of normal functionallity)
- edge case (weird input from user, not accorded to the requirement)
