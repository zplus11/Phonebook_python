from time import sleep
import json
import os
import Levenshtein

def find_closest_match(search_query, contacts):
    closest_match = None
    min_distance = float('inf')
    for contact in contacts:
        distance = Levenshtein.distance(search_query, contact)
        if distance < min_distance:
            min_distance = distance
            closest_match = contact
    return closest_match

st = "\033[0;36m"
st2 = "\033[0;46;30m"
ed = "\033[0m"

if os.path.exists("phonebank.json"):
    n11 = "n11" # no use
else:
    empty_book = {}
    string = json.dumps(empty_book, indent=4)
    with open("phonebank.json", "w") as file:
        file.write(string)
    file.close()


print(st2 + " <<-----------------| PHONEBOOK PROGRAM |----------------->> " + ed)
print(st + "Welcome to the program. You can keep your phone numbers here. They will be locally stored (in a newly made json file) and you can access them each time you open this file." + ed)
print("You have the following options.\n- Enter 1 to see the phonebook.\n- Enter 2 to add a new friend.\n- Enter 2b to add many friends in bulk.\n- Enter 3 to remove a friend.\n- Enter 4 to edit number of a friend.\n- Enter 5 to see details of an existing friend.\n- Enter 0 to enter dev mode.\n- Enter X to close the menu.")
ch = input("Enter your choice: ")
while ch.lower() != "x":
    if ch == "1":
        with open("phonebank.json", "r") as file:
            phone_dict = json.load(file)
        if len(phone_dict) == 0:
            print(st2 + "No friends?" + ed)
        else:
            max_length = max(len(str(key)) for key in phone_dict.keys()) + 5
            print(st2 + "NAME" + " " * (max_length - 4) + "PHONE NUMBER" + ed)
            for key in sorted(list(phone_dict)):
                name = str(key) + " " * (max_length - len(str(key)))
                if isinstance(phone_dict[key], list):
                    number = ", ".join(phone_dict[key])
                else:
                    number = phone_dict[key]
                print(st + name + " " + str(number) + ed)
    elif ch == "2":
        newfriend_name = input("Enter the name of your new friend: ").title()
        with open("phonebank.json", "r") as file:
            phone_dict = json.load(file)
        if newfriend_name in phone_dict:
            print(st2 + "They are already present in the book." + ed)
        else:
            newfriend_number_in = input("Enter their number/s (separate by comma if more than one): ")
            if "," in newfriend_number_in:
                newfriend_number = [element.strip() for element in newfriend_number_in.split(",")]
                newfriends_string = ", ".join(newfriend_number)
            else:
                newfriend_number = newfriend_number_in
                newfriends_string = newfriend_number_in
            phone_dict[newfriend_name] = newfriend_number
            with open("phonebank.json", "w") as file:
                json.dump(phone_dict, file)
            print(st2 + f"Okay, {newfriend_name} is added to the book with number/s {newfriends_string}." + ed)
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
                    friend_name = input("Enter their name: ").title()
                    friend_number_in = input("Enter their number/s: ")
                    if "," in friend_number_in:
                        friend_number = [element.strip() for element in friend_number_in.split(",")]
                    else:
                        friend_number = friend_number_in
                    phone_dict[friend_name] = friend_number
                    friend_names.append(friend_name)
                    names_string = ", ".join(friend_names)
                    with open("phonebank.json", "w") as file:
                        json.dump(phone_dict, file)
                print(st2 + f"{names_string} have been added to the phonebook!" + ed)
            else:
                print(st2 + "Very great bud, the 0 (zero) friends you wanted added have been added to the phonebook." + ed)
        else:
            print(st2 + f"Invalid number. Search for a course on Natural Numbers." + ed)
    elif ch == "3":
        toremove_name = input("Enter the name of the friend you want to remove: ").title()
        if toremove_name in phone_dict:
            del phone_dict[toremove_name]
            with open("phonebank.json", "w") as file:
                json.dump(phone_dict, file)
            print(st2 + f"Okay, {toremove_name} has been removed from the book." + ed)
        else:
            print(st2 + "They are not present in the dictionary. Check for spelling errors." + ed)
    elif ch == "4":
        edit_friend = input("Enter the name of friend to edit their number: ").title()
        with open("phonebank.json", "r") as file:
            phone_dict = json.load(file)
        if edit_friend in phone_dict:
            old_number = phone_dict[edit_friend]
            if isinstance(old_number, list):
                oldnumbers_string = ", ".join(old_number)
            else:
                oldnumbers_string = old_number
            new_number_in = input("Enter their new number/s (separate by comma if more than one): ")
            if "," in new_number_in:
                new_number = [element.strip() for element in new_number_in.split(",")]
                newnumbers_string = ", ".join(new_number)
            else:
                new_number = new_number_in
                newnumbers_string = new_number_in
            phone_dict[edit_friend] = new_number
            with open("phonebank.json", "w") as file:
                json.dump(phone_dict, file)
            print(st2 + f"Okay, the number/s of {edit_friend} has been changed FROM {oldnumbers_string} TO {newnumbers_string}." + ed)
        else:
            print(st2 + "They are not present in the dictionary. Check for spelling errors." + ed)
    elif ch == "5":
        with open("phonebank.json", "r") as file:
            phone_dict = json.load(file)
        search_name = input("Enter the name of the friend you want to search: ").title()
        search_result = find_closest_match(search_name, phone_dict)
        search_number = phone_dict[search_name]
        if isinstance(search_number, list):
            searchnumbers_string = ", ".join(search_number)
        else:
            searchnumbers_string = search_number
        print(st2 + f"I found {search_result} in the phonebook." + ed + st + f"\nThis is {search_result}.\nFound number/s: {searchnumbers_string}." + ed)
        print(f"To Copy // {search_result}: {searchnumbers_string}")
    elif ch == "0":
        print("Welcome to dev mode. Here you can reset the phonebook and back your data up in a backup file (It will be saved in the working directory with name ""phonebank_backup.json"". Furthermore, you can also restore an already existing data.")
        print("- Enter ""RESET"" (case sensitive) to reset all of the data right now.\n- Enter ""RESTORE"" to restore the data from an existing backup file.")
        dch = input()
        if dch == "RESET":
            with open("phonebank.json", "r") as file:
                phone_dict = json.load(file)
            with open("phonebank_backup.json", "w") as file:
                json.dump(phone_dict, file)
            with open("phonebank.json", "w") as file:
                json.dump({}, file)
            print(st2 + "All data has been reset and backup file has been created/updated. Find it in the directory of this program file." + ed)
        elif dch == "RESTORE":
            print(st + "The file must be a json file in dictionary format otherwise I don't know what will happen." + ed)
            filepath = input("Enter the file name with extension (or path if it's not in the working directory): ")
            if os.path.exists(f"{filepath}"):
                with open(filepath, "r") as file:
                    phonebank_backup_dict = json.load(file)
                with open("phonebank.json", "r") as file:
                    phonebank_existing = json.load(file)
                updated_existing = {}
                for item in phonebank_existing:
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
                print(st2 + "The file does not exist. Troubleshooting: Confirm path; Remember to include file extension in name; Path dummy example: ""D:\My Files\contacts_backup.json""" + ed)
        else:
            print(st2 + "Invalid choice. Can you read?" + ed)
    else:
        print(st2 + "Invalid choice. Refer to the guide." + ed)
    print("---------------------------X--------------X---------------------------")
    print("Task completed. Want to do another task? Same guide applies. 1) See book, 2) Add friend, 2b) Add friends in bulk, 3) Remove friend, 4) Edit friend, 5) Search friend, 0) Dev mode, X) End interaction.") 
    ch = input("Enter your next choice: ")
    print()
print(st2 + "You have opted to close the phonebook. Bye!" + ed)
sleep(2)
