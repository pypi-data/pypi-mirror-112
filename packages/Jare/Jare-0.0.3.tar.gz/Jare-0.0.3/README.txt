Installing Jare


Since this is a python module, you have to have the module installed. 
Know since I do have a windows and not mac or linux it might be a bit different but 
mostly it is the same.

To install Jare, simply open Command Promt(For Mac or Linux it is different, 
you can google "how to install packages in mac/linux" if you have any of those) 
and then type:

pip install jare


Commands:


1.jare_run_list


This Command takes 3 values:

1.Input value (input(x))


2.Questions list (questions = ["Hello", "How are you doing"])


3. Answers List (answers = ["Hi", "I am fine, Thank You!"])


BEFORE YOU CODE:
MAKE SURE THAT THE INDEX OF THE QUESTION AND THE ANSWER LIST ARE THE SAME 
FOR EXAMPLE: IF YOU WANT THE BOT TO SAY Hi WHEN THE USER ASKE'S hello AND 
IF YOU WANT THE BOT TO SAY I am fine, Thank You! WHEN THE USER ASKE'S How are you doing
THEN THE INDEX OR THE STRINGS HAVE TO BE IN THE SAME ORDER


questions = ["Hello", "How are you doing"]


answers = ["Hi", "I am fine, Thank You!"]


Then it simple combines it in to a dictionary and then ask's the user for an input and 
then prints out the responses



2.jare_run_dictionary


This is very similar to the 1st Command. Simply it takes two values the input value
and the dictionary. Make sure that the dictionary is something like this:

dictionary = {"Hello":"Hi", "How are you":"I am fine thank you!"}



then ask's the user for an input and then prints out the responses
