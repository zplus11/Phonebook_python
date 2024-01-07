from time import sleep
import json
import os
import Levenshtein
import subprocess
from datetime import datetime

def find_closest_match(search_query, contacts):
    closest_match = None
    min_distance = float('inf')
    for contact in contacts:
        distance = Levenshtein.distance(search_query, contact)
        if distance < min_distance:
            min_distance = distance
            closest_match = contact
    return closest_match

def clean_for_tex(string):
                cleaned = ""
                for i in string:
                    if i in r"&%$#_{}~^\ ": cleaned += fr"\{i}"
                    else: cleaned += i
                return cleaned
    
if not os.path.exists("phonebank.json"):
    empty = {"admin": {"theme": "6", "language": "english"}}
    with open("phonebank.json", "w") as file:
        json.dump(empty, file)
    file.close()

with open("phonebank.json", "r") as file:
    phone_dict = json.load(file)
  
with open("phonebank.json", "r") as file:
    phone_dict = json.load(file)
theme = phone_dict["admin"]["theme"]
st = f"\033[0;3{theme}m"
st2 = f"\033[0;4{theme};30m"
ed = "\033[0m"

colours = {"blue": "6", "green": "2", "purple": "5", "red": "1", "white": "7", "yellow": "3"}

print(st2 + " <<-----------------| PHONEBOOK PROGRAM |----------------->> " + ed)
print(st + "Welcome to the program. You can keep your phone numbers here. They will be locally stored (in a newly made json file) and you can access them each time you open this file." + ed)
print("You have the following options.\n- Enter 1 to see the phonebook.\n- Enter 2 to add a new friend.\n- Enter 2b to add many friends in bulk.\n- Enter 3 to remove a friend.\n- Enter 4 to edit number of a friend.\n- Enter 4b to edit note of a friend.\n- Enter 5 to see details of an existing friend.\n- Enter p to generate a pdf of all phone numbers.\n- Enter + to change your settings.\n- Enter 0 to enter dev mode.\n- Enter X to close the menu.")
ch = input("Enter your choice: ")
while ch.lower().strip() != "x":
    if ch == "1":
        with open("phonebank.json", "r") as file:
            phone_dict = json.load(file)
        if len(phone_dict) == 1:
            print(st2 + "No friends?" + ed)
        else:
            max_length1 = max(len(str(key)) for key in phone_dict.keys()) + 5
            max_length2 = max(sum(len(number) for number in phone_dict[key][0]) + 2*len(phone_dict[key][0]) for key in phone_dict if key != "admin") + 3
            print(st2 + "NAME" + " " * (max_length1 - 3) + "PHONE NUMBER" + " " * (max_length2 - 11) + "NOTE" + ed)
            for key in sorted(list(phone_dict)):
                if key.lower().strip() != "admin":
                    name = str(key) + " " * (max_length1 - len(str(key)))
                    number_string = ", ".join(phone_dict[key][0])
                    number = number_string + " " * (max_length2 - len(number_string))
                    print(st + name + " " + str(number) + " " + phone_dict[key][1] + ed)
    elif ch == "2":
        newfriend_name = input("Enter the name of your new friend: ").title().strip()
        with open("phonebank.json", "r") as file:
            phone_dict = json.load(file)
        if newfriend_name in phone_dict:
            print(st2 + "They are already present in the book." + ed)
        elif newfriend_name.lower().strip() == "admin":
            print(st2 + "Sorry, that name is reserved." + ed)
        else:
            newfriend_number_in = input("Enter their number/s (separate by comma if more than one): ")
            newfriend_number = [element.strip() for element in newfriend_number_in.split(",")]
            newfriends_string = ", ".join(newfriend_number)
            newfriend_note = input("Enter any note for them if applicable (otherwise enter na or just enter): ")
            if newfriend_note.lower() in ["na", "n.a.", "n/a"] or len(newfriend_note) == 0:
                newfriend_note = "None"
            phone_dict[newfriend_name] = [newfriend_number, newfriend_note]
            with open("phonebank.json", "w") as file:
                json.dump(phone_dict, file)
            print(st2 + f"Okay, {newfriend_name} is added to the book with number/s {newfriends_string} and note {newfriend_note}." + ed)
    elif ch == "2b":
        print("Here you can add many friends to the phonebook at bulk. First letter of each name will automatically be capitalised, rest small-cased.")
        with open("phonebank.json", "r") as file:
            phone_dict = json.load(file)
        n = input("Enter the number of friends you wish to input: ")
        if n.isdigit():
            if int(n) > 0:
                print("If the friend has more than one number, then separate their numbers by a comma (,)")
                friend_names = []
                for i in range(int(n)):
                    print(st + "Friend", str(i+1) + ed)
                    friend_name = input("Enter their name: ").title().strip()
                    if friend_name in phone_dict:
                        print(st + f"They are already present in the book. Moving forward." + ed)
                    elif friend_name.lower().strip() == "admin":
                        print(st2 + "Sorry, that name is reserved." + ed)
                    else:
                        newfriend_number_in = input("Enter their number/s: ")
                        newfriend_note = input("Enter any note for them if applicable (otherwise enter na or just enter): ")
                        newfriend_number = [element.strip() for element in newfriend_number_in.split(",")]
                        newfriends_string = ", ".join(newfriend_number)
                        phone_dict[friend_name] = [newfriend_number, newfriend_note]
                        friend_names.append(friend_name)
                        names_string = ", ".join(friend_names)
                with open("phonebank.json", "w") as file:
                    json.dump(phone_dict, file)
                print(st2 + f"The following people have been added to the phonebook!" + ed)
                if len(friend_names) == 0:
                    print(st + "None." + ed)
                for friend in friend_names:
                    numbers_string = ", ".join(phone_dict[friend][0])
                    print(st + f"{friend} [{phone_dict[friend][1]}]: {numbers_string}" + ed)
            else:
                print(st2 + "Very great bud, the 0 (zero) friends you wanted added have been added to the phonebook." + ed)
        else:
            print(st2 + f"Invalid number. Search for a course on Natural Numbers." + ed)
    elif ch == "3":
        toremove_name = input("Enter the name of the friend you want to remove: ").title().strip()
        if toremove_name in phone_dict and toremove_name.lower() != "admin":
            del phone_dict[toremove_name]
            with open("phonebank.json", "w") as file:
                json.dump(phone_dict, file)
            print(st2 + f"Okay, {toremove_name} has been removed from the book." + ed)
        else:
            print(st2 + "They are not present in the dictionary. Check for spelling errors." + ed)
    elif ch == "4":
        edit_friend = input("Enter the name of friend to edit their number: ").title().strip()
        with open("phonebank.json", "r") as file:
            phone_dict = json.load(file)
        if edit_friend in phone_dict and edit_friend.lower() != "admin":
            old_number = phone_dict[edit_friend][0]
            oldnumbers_string = ", ".join(old_number)
            new_number_in = input("Enter their new number/s (separate by comma if more than one): ")
            new_number = [element.strip() for element in new_number_in.split(",")]
            newnumbers_string = ", ".join(new_number)
            phone_dict[edit_friend][0] = new_number
            with open("phonebank.json", "w") as file:
                json.dump(phone_dict, file)
            print(st2 + f"Okay, the number/s of {edit_friend} has been changed FROM {oldnumbers_string} TO {newnumbers_string}." + ed)
        else:
            print(st2 + "They are not present in the dictionary. Check for spelling errors." + ed)
    elif ch == "4b":
        edit_friend = input("Enter the name of friend to edit their note: ").title().strip()
        with open("phonebank.json", "r") as file:
            phone_dict = json.load(file)
        if edit_friend in phone_dict and edit_friend.lower() != "admin":
            old_note = phone_dict[edit_friend][1]
            new_note = input("Enter a new note for them if applicable (otherwise enter na or just enter): ")
            if new_note.lower() in ["na", "n.a.", "n/a"] or len(new_note) == 0:
                new_note = "None"
            phone_dict[edit_friend][1] = new_note
            with open("phonebank.json", "w") as file:
                json.dump(phone_dict, file)
            print(st2 + f"Okay, the note for {edit_friend} has been changed from {old_note} to {new_note}." + ed)
        else:
            print(st2 + "They are not present in the dictionary. Check for spelling errors." + ed)
    elif ch == "5":
        with open("phonebank.json", "r") as file:
            phone_dict = json.load(file)
        search_name = input("Enter the name of the friend you want to search: ").title().strip()
        search_result = find_closest_match(search_name, phone_dict)
        search_number = phone_dict[search_result][0]
        search_note = phone_dict[search_result][1]
        searchnumbers_string = ", ".join(search_number)
        print(st2 + f"I found {search_result} in the phonebook." + ed + st + f"\nThis is {search_result}.\nFound number/s: {searchnumbers_string}\nFound note: {search_note}." + ed)
        print(f"To Copy // {search_result} [{search_note}]: {searchnumbers_string}")
    elif ch == "0":
        print("Welcome to dev mode. Here you can reset the phonebook and back your data up in a backup file (It will be saved in the working directory with name ""phonebank_backup.json"". Furthermore, you can also restore an already existing data.")
        print("- Enter ""RESET"" (case sensitive) to reset all of the data right now.\n- Enter ""RESTORE"" to restore the data from an existing backup file.")
        dch = input()
        if dch == "RESET":
            with open("phonebank.json", "r") as file:
                phone_dict = json.load(file)
            admin = phone_dict["admin"]
            with open("phonebank_backup.json", "w") as file:
                json.dump(phone_dict, file)
            with open("phonebank.json", "w") as file:
                json.dump({"admin": admin}, file)
            print(st2 + "All data has been reset and backup file has been created/updated. Find it in the directory of this program file." + ed)
        elif dch == "RESTORE":
            print(st + "The file must be a json file in dictionary format otherwise I don't know what will happen." + ed)
            filepath = input("Enter the file name with extension (or path if it's not in the working directory): ")
            if os.path.exists(f"{filepath}"):
                with open(filepath, "r") as file:
                    phonebank_backup_dict = json.load(file)
                with open("phonebank.json", "r") as file:
                    phonebank_existing = json.load(file)
                updated_existing = {"admin": {"theme": "6", "language": "english"}}
                for item in [i for i in phonebank_existing if i != "admin"]:
                    updated_existing[item.title()] = phonebank_existing[item]
                updated_existing.update(phonebank_backup_dict)
                if len(phonebank_backup_dict) == 0:
                    print(st2 + "Backup file is empty." + ed)
                else:
                    print("Do you wish to restore the following friends? y/n")
                    print(', '.join(str(key) for key in phonebank_backup_dict))
                    rch = input()
                    if rch.lower() in ["y", "yes", "1"]:
                        with open("phonebank.json", "w") as file:
                            json.dump(updated_existing, file)
                        file.close()
                        print(st2 + "Data has been retrieved from the backup file. Press 1 to see your book." + ed)
                    else:
                        print(st2 + "Data restoring cancelled." + ed)
            else:
                print(st2 + "The file does not exist. Troubleshooting: Confirm path; Remember to include file extension in name; Path dummy example: 'D:\\My Files\\contacts_backup.json'" + ed)
        else:
            print(st2 + "Invalid choice. Can you read?" + ed)
    elif ch == "+":
        print(st + "Welcome to settings! Here you can customise the book according to your preferences. You have the following options:" + ed)
        print("- Enter 1 to change theme\n- Type 'back' to go back")
        sch = input("Enter your settings choice: ").lower().strip()
        if sch == "1":
            print("You have the following theme options:")
            for colour in colours:
                print(f"\033[0;3{colours[colour]}m This is {colour}. \033[0m \033[0;4{colours[colour]};30m With {colour} background. \033[0m")
            theme_choice = input("Enter the colour name of theme you want: ").lower().strip()
            if theme_choice in colours:
                theme = colours[theme_choice]
                st = f"\033[0;3{theme}m"
                st2 = f"\033[0;4{theme};30m"
                with open("phonebank.json", "r") as file:
                    phone_dict = json.load(file)
                phone_dict["admin"]["theme"] = theme
                with open("phonebank.json", "w") as file:
                    json.dump(phone_dict, file)
                print(st2 + "Confirmed. The theme is changed. Hope you like it!" + ed)
            else:
                print(st2 + "Invalid choice. Your theme stands unchanged." + ed)
        else:
            print(st2 + "Invalid choice." + ed)
    elif ch == "p":
        for col in colours:
            if colours[col] == theme:
                my_col = col
        datetimestamp = str(datetime.now())
        with open("phonebank.json", "r") as file:
            phone_dict = json.load(file)
        tex_source = r"\documentclass[12pt,a4paper]{article}\usepackage{xcolor,geometry,hyperref}\geometry{margin=2cm}\newcounter{contact}\newcommand{\contact}[3]{\stepcounter{contact}\texttt{\thecontact.} {\bfseries#1} {\itshape(#3)}. \texttt{#2} \\ }\begin{document}\noindent"
        tex_source += f"\\colorbox{{{my_col}}}"
        tex_source += r"{{\Huge\bfseries MY PHONEBOOK}}\hfill{\bfseries Phonebook\_Python\footnote{\href{https://github.com/zplus11/Phonebook_python}{Github repository.}}}\hfill\\[\baselineskip]"
        for friend in sorted([i for i in phone_dict if i.lower() != "admin"]):
            name = clean_for_tex(friend)
            numbers = clean_for_tex(", ".join(phone_dict[friend][0]))
            note = clean_for_tex(phone_dict[friend][1])
            tex_source += fr"\contact{{{name}}}{{{numbers}}}{{{note}}}"
        tex_source += r"\end{document}"
        try:
            with open("mybook.tex", "w") as tex:
                tex.write(tex_source)
            subprocess.run(["pdflatex", "mybook.tex"])
            os.remove("mybook.aux")
            os.remove("mybook.log")
            os.remove("mybook.tex")
            os.remove("mybook.out")
            print(st2 + "Your phone numbers have been printed on mybook.pdf file!" + ed)
        except Exception as e:
            print("Error:", e)
    elif ch == "raw":
        with open("phonebank.json", "r") as file:
            phone_dict = json.load(file)
        print(f"This is phonebank.json")
        print(phone_dict)
    else:
        print(st2 + "Invalid choice. Refer to the guide." + ed)
    print("---------------------------X--------------X---------------------------")
    print("Task completed. Want to do another task? Same guide applies. 1) See book, 2) Add friend, 2b) Add friends in bulk, 3) Remove friend, 4) Edit number of friend, 4b) Edit note of friend, 5) Search friend, p) Make pdf of phone numbers, +) Change settings, 0) Dev mode, X) End interaction.") 
    ch = input("Enter your next choice: ").lower().strip()
    print()
print(st2 + "You have opted to close the phonebook. Bye!" + ed)
sleep(2)
