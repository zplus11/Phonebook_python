# Phonebook_python
This is a basic phonebook program where you can store your contacts. The numbers and other info are stored locally in a json file.

We are at version 3. Ref `versions.md`.

The program allows you to
- [x] Add a contact with name, multiple phones, multiple emails, address, note,
- [x] Remove a contact,
- [x] Edit details of a contact,
- [x] Search for a contact's details,
- [x] Print the complete book to PDF format (requires `pdflatex`<sup>1</sup>).

1.  **See [MiKTeX](https://miktex.org/) for a `pdflatex` distribution.**

## How to use
To install the program, navigate to your desired directory and run `git clone https://github.com/zplus11/Phonebook_python.git` in the console. Then run `phonebook.py`. To use this program, you ONLY need that file apart from `pdflatex`.

## Screenshots

*(May not correspond to the latest commit...)*

- Showing the book. Type 1a to list details of each contact.
<img src="assets/1.png" alt="Turtle graphics" style="width: 100%">

- Showing detail of a contact.
<img src="assets/2.png" alt="Turtle graphics" style="width: 100%">

- Add a contact.
<img src="assets/3.png" alt="Turtle graphics" style="width: 100%">

- Remove a contact.
<img src="assets/4.png" alt="Turtle graphics" style="width: 100%">

- Edit a contact
<img src="assets/5.png" alt="Turtle graphics" style="width: 100%">

- Print the book to PDF
<img src="assets/p.png" alt="Turtle graphics" style="width: 100%">
<img src="assets/sp.png" alt="Turtle graphics" style="width: 100%">

## Versions

#### Version 0 [upto Version 1]
- Launch and minor changes

#### Version 1 [05 Sep, 2023]
- Colour support
- Added `admin` block for saving preferences in `phonebank.json`
- Misc: All numbers are within lists now

#### Version 2 [08 Dec, 2023]
- Added option to export book into pdf
- Fixed some minor bugs

#### Version 3 [13 June, 2024]
- Probably the last version
- Rewrote completely in a far better way

