# Jafr (Just A Friendly Reminder)

## Description

Just A Friendly Reminder is a start up Unix program written in Python which use to remind and manage task or meeting of the day between different user in the computer.
> Jafr is designed to run whenever a user opens their terminal at the beginning of their day. Users can choose to view reminders that are relevant to the current day, or make changes. Changes can include sharing reminders with other users. -- USYD

## About

Just A Friendly Reminder is a start up Unix program written in Python which mimic a Unix filesystem with multiple users and they all can share task or meeting. The program ideal is to run every time you start the Unix terminal and will display all the current task and meeting that you had and you able to edit them. However, this is just a simulation on how thats works.

This program is dedicated for educational purpose only. Since this is only a part for university project at USYD - INFO1112 Computing 1B OS and Network Platforms given by the task:
> In this assignment, you'll be creating a basic application called "Jafr" (short for "Just a friendly reminder"). This application helps multiple users manage their tasks and meetings on a Unix-like OS (a popular choice of OS in industry where developers might share a computer system or host web applications).
> Jafr is Unix-friendly. This means that
> Users interact with Jafr by typing commands in a command-line interface.
> Jafr assumes that all the tasks and meetings are stored in text files that are otherwise managed by users of the shared system. Users simply edit these files themselves when they want to make changes outside of Jafr.
> You will implement Jafr in Python and write a simple start up script in Bash. You will then write I/O end to end tests for Jafr.

Only student at USYD can see the [scaffold](https://github.sydney.edu.au/ppal4396/2023-INFO1112-A1/blob/main/JustAFriendlyReminder.md)

## Features

Jafr had mandetory features such as:
1. Display the task and meeting of the day
2. Mark the task as finished
3. Add new meeting that will appear on other user as well
4. Able to share task or meeting
5. Able to change the master directory
6. Able to exit the program

## How to run

Once you had install all the git repo you can run the program by type
"bash .bashrc"
on the terminal to start the program

Normally, .bashrc file will be inside home directory
It will run every time Unix start the program
Since this is a simulation so it's better to just run "bash .bashrc" here

## How to test

This repo also came with the testing suite
Please see "test_readme.md" for more information

## Note for tester or user (how to use)

(Before program start)
You are free to add, edit, or delete task and meeting in "tasks.md" and "meetings.md"
task format would be: "- task name Due: dd/mm/yy [complete/not complete]"
meeting format would be: "- meeting name Scheduled: mm:hh dd/mm/yy"
If you're confused you can see the template given by the repo
Note that wrong format tasks and meetings will be ignore in the program

(During the program)
You are able to put sequence of number to complete the task
(eg. 1 2 3 is allowed)

The correct date format is "dd/mm/yy"
The correct time format is "hh:mm" 
if you put the incorrect format it will repromt again

## Contributor

USYD: https://www.sydney.edu.au/

## Credit

Programmer: Best Phanuwish