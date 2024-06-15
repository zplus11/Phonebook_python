import json
import justify
import os


def l60(content, width = 60):
    lines = []
    words = content.split(" ")
    while words:
        line = words[0]
        words.pop(0)
        while len(line) < width and words:
            popped = words.pop(0)
            if len(popped) > width:
                words.insert(0, popped[0: width] + "-")
                words.insert(1, popped[width: ])
                break
            if len(popped) < width - len(line):
                line += " " + popped
            else:
                words.insert(0, popped)
                break
        if line: lines.append(line)
    return lines

class Contact:

    def __init__(self, name: str, phone: list[str], email: list[str], address: str, note: str):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.note = note

    def __repr__(self):
        return self.name + " - " + self.note

    def __str__(self):
        return self.name.upper() + "\n" \
               + "Phone.     " + ("\n" + (" "*11)).join(self.phone) + "\n" \
               + "Email.     " + ("\n" + (" "*11)).join(self.email) + "\n" \
               + "Address.   " + ("\n" + (" "*11)).join(l60(self.address)) + "\n" \
               + "Note.      " + ("\n" + (" "*11)).join(l60(self.note))

class Book:

    def __init__(self, data):
        self.data = data
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        if not os.path.exists(data):
            with open(data, "w") as file:
                json.dump({"contacts": []}, file)
        with open(data, "r") as file:
            self.contacts = [Contact(x[0], x[1], x[2], x[3], x[4]) for x in json.load(file)["contacts"]]

    def __len__(self):
        return len(self.contacts)
    
    def __repr__(self):
        return "Book("+str(len(self))+")"

    def __iter__(self):
        for person in self.contacts:
            yield person

    def __str__(self):
        return "\n".join([str(i+1) + "\t" + repr(person) for i, person in enumerate(self)]) or "No Friends?"

    def add(self):
        self.contacts.append(
            Contact(
                input("Enter the name: ").title(),
                [x.strip() for x in input("Enter the phone numbers (comma separated): ").split(",")],
                [x.strip() for x in input("Enter the phone emails (comma separated): ").split(",")],
                input("Enter the address: ") or "NA",
                input("Enter note if any, else press return: ") or "NA"
            )
        )
        return f"Successfully added to the contacts."

    def remove(self, removename):
        for p in self:
            if p.name == removename:
                self.contacts.remove(p)
                return f"{p.name} was removed from the book."
        return f"No contact named {removename} found in the book."

    def edit(self, editname):
        this = None
        for some in self:
            if some.name == editname:
                this = some
        if this is not None:
            change = input("What to edit: name/phone/email/address/note: ")
            to = input("Enter the replacement: ")
            match change:
                case "name":
                    this.name = to.title()
                case "phone":
                    this.phone = [x.strip() for x in to.split(",")]
                case "email":
                    this.email = [x.strip() for x in to.split(",")]
                case "address":
                    this.address = to or "NA"
                case "note":
                    this.note = to or "NA"
                case _:
                    return f"Invalid change demanded."
            return f"The required changes are made."
        else:
            return f"No contact named {editname} found in the book." 

    def show(self, findname):
        for p in self:
            if p.name == findname: return str(p)
        return f"No contact named {findname} found in the book."

    def pprint(self, response):
        l = 100
        print("-"*l)
        for line in response.split("\n"):
            print("|  " + line + " "*(l-6 - len(line)) + "  |")
        print("-"*l)

    def menu(self):
        print("You have the following options:")
        print("1   Print the complete book")
        print("2   Show details of a contact")
        print("3   Add a contact")
        print("4   Remove a contact")
        print("5   Edit a contact")
        print("p   Print the book to PDF (requires pdflatex)")
        print("x   Close the book (ALWAYS use this to log out)")
        print("Type the character corresponding to your choice and hit enter.")

    def invalid(self):
        return "Invalid choice."

    def pdf(self):
        with open("Book.tex", "w") as file:
            file.write(
                "\\documentclass{article}\\usepackage[margin=1in]{geometry}\\newcommand\\contact[5]{\\vskip10pt{\\bf\\MakeUppercase{#1}}\\par\\vskip4pt" \
                "\\parbox[t]{.2\\linewidth}{{\\bf Phone.}} \\parbox[t]{.7\\linewidth}{#2} \\par\\vskip5pt" \
                "\\parbox[t]{.2\\linewidth}{{\\bf Email.}} \\parbox[t]{.7\\linewidth}{#3} \\par\\vskip5pt" \
                "\\parbox[t]{.2\\linewidth}{{\\bf Address.}} \\parbox[t]{.7\\linewidth}{#4} \\par\\vskip5pt" \
                "\\parbox[t]{.2\\linewidth}{{\\bf Note.}} \\parbox[t]{.7\\linewidth}{#5}}\\usepackage[utf8]{inputenc}\\begin{document}"
            )
            for p in self:
                file.write("\\contact{" \
                           + "}{".join([p.name, ", ".join(p.phone), ", ".join(p.email), self.clean(p.address), self.clean(p.note)]) \
                           + "}"
                )
            file.write("\\end{document}")
        import subprocess
        try:
            subprocess.run(["pdflatex", "Book.tex"])
            os.remove("Book.aux")
            os.remove("Book.log")
            os.remove("Book.tex")
            return "Contacts are printed to Book.pdf"
        except Exception as e:
            return "\n".join(l60("Error printing: " + str(e)))

    def clean(self, string):
        cleaned = ""
        for i in string:
            if i in r"&%$#_{}~\^": cleaned += fr"\{i}"
            else: cleaned += i
        return cleaned

    def quit(self):
        to_export = [(person.name, person.phone, person.email, person.address, person.note) for person in self.contacts]
        with open(self.data, "w") as file:
            json.dump({"contacts": to_export}, file)
        
    
book = Book("book.json")
book.pprint(" "*34+"WELCOME TO YOUR PHONEBOOK!")
book.menu()
choice = input().lower().strip()
while choice != "x":
    if choice == "1":
        print(book)
    elif choice == "1a":
        for p in book:
            book.pprint(book.show(p.name))
    elif choice == "2":
        toshow = input("Enter name of the contact: ")
        book.pprint(book.show(toshow))
        del toshow
    elif choice == "3":
        book.pprint(book.add())
    elif choice == "4":
        toremove = input("Enter name of the contact: ")
        book.pprint(book.remove(toremove))
        del toremove
    elif choice == "5":
        toedit = input("Enter name of the contact: ")
        book.pprint(book.edit(toedit))
        del toedit
    elif choice == "p":
        book.pprint(book.pdf())
    elif choice == "x":
        break
    else:
        book.pprint(book.invalid())
    print()
    book.menu()
    choice = input().lower().strip()
book.quit()
