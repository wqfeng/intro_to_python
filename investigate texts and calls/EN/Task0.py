"""
Intro to Python Project 1, Task 0

Complete each task in the file for that task. Submit the whole folder
as a zip file or GitHub repo. 
Full submission instructions are available on the Project Preparation page.
"""


"""
Read file into texts and calls. 
It's ok if you don't understand how to read files
You will learn more about reading files in future lesson
"""
import csv
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)


"""
TASK 0: 
what is the first record of texts and what is the last record of calls
Print messages: 
"First record of texts, <incoming number> texts <answering number> at time <time>"
"Last record of calls, <incoming number> calls <answering number> at time <time>, lasting <during> seconds"
"""
first_record_of_texts = texts[0]
last_record_of_calls = calls[-1]

print("First record of texts, {} texts {} at time {}".format(
    first_record_of_texts[0],
    first_record_of_texts[1],
    first_record_of_texts[2]
))

print("Last record of calls, {} calls {} at time {}, lasting {} seconds".format(
    last_record_of_calls[0],
    last_record_of_calls[1],
    last_record_of_calls[2],
    last_record_of_calls[3]
))

