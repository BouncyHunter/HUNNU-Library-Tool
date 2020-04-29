# HUNNU-Library-Tool
See who booked the seat already, book seats straight, and book seats automatically on your own server. Your own cookies required.

## autobook.py
Comes with a list of scheduled book request. Append yours to the list, a timer which triggers every 0.5 second will create a thread that book as you wish for each item in the list. Once succeed, the request will be removed from the list.
Read the source code to learn more and help me improve it.

In this program I imitated a simple command line with only few commands:

  book [seat NO] [date] [start time] [end time]
    Add a book request to the list. Note that start time and end time contain an integer [0, 1439], representing the minutes of a day.
  
  ls
    Print the list.
    
  del [index]
    Remove the book request of inputted index.
    
## hunnuCrawlMulti2_1.py
Crawl all the seats and who booked those seats of what time. Will create a "index.out" file and write it down at current folder.
Note that default date is 2020-04-24 and can be modified via source code only.

## request_main.py
In this program I imitated a simple command line with only few commands. Just type "help" for more info. Totally useless.

## tkinter_test.py
An application by tkinter for newbies. Note that start time and end time contain an integer [0, 1439], representing the minutes of a day.
"Liked Seats" works familiar with autobook.py, but has no multi-thread support, which means this book seats slowlier when having multiple
items in the list.
