# Phonebook_python
This is a basic phonebook program where you can store your friends' phone numbers. The numbers and other info are stored locally in a json file. ANSI 8-16 colour codes are used to beautify the output. These codes are supported by most consoles.

We are at version 2. Ref `versions.md`.

The program allows you to
- [x] Add a friend,
- [x] Add many friends in bulk,
- [x] Add multiple numbers for a friend, 
- [x] Remove a friend,
- [x] Edit number of a friend,
- [x] Search for a friend's details,
- [x] Reset your numbers (and create a backup file) or restore from an existing backup file,
- [x] Add or edit notes for an existing friend.
- [x] Change colour themes of the book.
- [x] Extract the complete book in pdf format (requires `pdflatex`).
- [ ] Change language for the program.

## How to use
To install the program, navigate to your desired directory and run `git clone https://github.com/zplus11/Phonebook_python.git` in the console. Or simply download `phonebook.py` file manually and run it from there.

⚠️ **To run the program, you need to have Python, `pdflatex`, and `Levenshtein`, `json` modules installed. Install Python from [here](https://www.python.org/downloads/) and the modules using `pip install <name>` command. See [MiKTeX](https://miktex.org/) for `pdflatex` distribution.**

