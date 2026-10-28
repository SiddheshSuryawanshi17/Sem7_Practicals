# STQA Mini Project - Application Under Test (AUT)
# Library Management System: add books, register members, issue / return books, fine calculation.
# Run the app:   python library.py
from datetime import date, timedelta

MAX_BOOKS_PER_MEMBER = 3
LOAN_DAYS = 14
FINE_PER_DAY = 5      # Rs per late day
MAX_FINE = 500


class LibraryError(Exception):
    pass


class Book:
    def __init__(self, isbn, title, author, copies=1):
        if not isbn or len(isbn) != 13 or not isbn.isdigit():
            raise LibraryError("ISBN must be exactly 13 digits")
        if not title.strip():
            raise LibraryError("Title cannot be empty")
        if copies < 1:
            raise LibraryError("Copies must be at least 1")
        self.isbn, self.title, self.author = isbn, title.strip(), author.strip()
        self.total = self.available = copies


class Member:
    def __init__(self, member_id, name, age):
        if not (member_id.startswith("M") and member_id[1:].isdigit() and len(member_id) == 5):
            raise LibraryError("Member ID must be like M1234")
        if not name.strip():
            raise LibraryError("Name cannot be empty")
        if not (5 <= age <= 100):
            raise LibraryError("Age must be between 5 and 100")
        self.member_id, self.name, self.age = member_id, name.strip(), age
        self.borrowed = {}   # isbn -> issue date


def calculate_fine(days_late):
    """Fine rules: 0 if returned on time, Rs 5/day late, capped at Rs 500."""
    if days_late < 0:
        raise LibraryError("Days late cannot be negative")
    if days_late == 0:
        return 0
    return min(days_late * FINE_PER_DAY, MAX_FINE)


class Library:
    def __init__(self):
        self.books, self.members = {}, {}

    def add_book(self, book):
        if book.isbn in self.books:
            self.books[book.isbn].total += book.total
            self.books[book.isbn].available += book.total
        else:
            self.books[book.isbn] = book

    def register_member(self, member):
        if member.member_id in self.members:
            raise LibraryError("Member already registered")
        self.members[member.member_id] = member

    def search(self, keyword):
        k = keyword.lower()
        return [b for b in self.books.values() if k in b.title.lower() or k in b.author.lower()]

    def issue_book(self, member_id, isbn, on=None):
        on = on or date.today()
        member = self.members.get(member_id)
        book = self.books.get(isbn)
        if member is None:
            raise LibraryError("Member not found")
        if book is None:
            raise LibraryError("Book not found")
        if book.available == 0:
            raise LibraryError("No copies available")
        if isbn in member.borrowed:
            raise LibraryError("Member already has this book")
        if len(member.borrowed) >= MAX_BOOKS_PER_MEMBER:
            raise LibraryError("Borrow limit reached")
        book.available -= 1
        member.borrowed[isbn] = on
        return on + timedelta(days=LOAN_DAYS)          # due date

    def return_book(self, member_id, isbn, on=None):
        on = on or date.today()
        member = self.members.get(member_id)
        if member is None or isbn not in member.borrowed:
            raise LibraryError("This book was not issued to this member")
        issued = member.borrowed.pop(isbn)
        self.books[isbn].available += 1
        days_late = max(0, (on - issued).days - LOAN_DAYS)
        return calculate_fine(days_late)


def main():
    lib = Library()
    lib.add_book(Book("9780131103627", "The C Programming Language", "Kernighan", 2))
    lib.add_book(Book("9780262033848", "Introduction to Algorithms", "Cormen", 1))
    menu = "\n1.Add book 2.Register member 3.Search 4.Issue 5.Return 6.List books 0.Exit\nChoice: "
    while True:
        try:
            ch = input(menu).strip()
            if ch == "1":
                lib.add_book(Book(input("ISBN (13 digits): "), input("Title: "), input("Author: "), int(input("Copies: "))))
                print("Book added")
            elif ch == "2":
                lib.register_member(Member(input("Member ID (M1234): "), input("Name: "), int(input("Age: "))))
                print("Member registered")
            elif ch == "3":
                for b in lib.search(input("Keyword: ")):
                    print(f"{b.isbn} | {b.title} | {b.author} | available {b.available}/{b.total}")
            elif ch == "4":
                print("Issued. Due date:", lib.issue_book(input("Member ID: "), input("ISBN: ")))
            elif ch == "5":
                print("Returned. Fine: Rs", lib.return_book(input("Member ID: "), input("ISBN: ")))
            elif ch == "6":
                for b in lib.books.values():
                    print(f"{b.isbn} | {b.title} | {b.author} | available {b.available}/{b.total}")
            elif ch == "0":
                break
        except (LibraryError, ValueError) as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
