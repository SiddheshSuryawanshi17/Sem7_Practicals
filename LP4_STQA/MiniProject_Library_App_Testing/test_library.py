# STQA Mini Project - Automated tests (Python unittest, no install needed)
#   * White-box unit tests  : cover every branch of calculate_fine / validation code
#   * Black-box tests       : Equivalence Class Partitioning (ECP) + Boundary Value Analysis (BVA)
#   * Integration tests     : Library + Book + Member working together (issue -> return -> fine)
# Run: python -m unittest -v test_library.py      (or: python run_tests.py for a full report)
import unittest
from datetime import date, timedelta

from library import Book, Library, LibraryError, Member, calculate_fine, MAX_BOOKS_PER_MEMBER


# ------------------------------------------------------------------ White-box (unit)
class TC01_WhiteBox_CalculateFine(unittest.TestCase):
    """Branch coverage of calculate_fine(): 4 paths."""

    def test_path1_negative_days_raises(self):
        with self.assertRaises(LibraryError):
            calculate_fine(-1)

    def test_path2_zero_days_no_fine(self):
        self.assertEqual(calculate_fine(0), 0)

    def test_path3_fine_below_cap(self):
        self.assertEqual(calculate_fine(10), 50)

    def test_path4_fine_capped(self):
        self.assertEqual(calculate_fine(1000), 500)


class TC02_WhiteBox_BookValidation(unittest.TestCase):
    def test_valid_book(self):
        b = Book("9780131103627", "C Lang", "K&R", 2)
        self.assertEqual((b.total, b.available), (2, 2))

    def test_isbn_not_digits(self):
        self.assertRaises(LibraryError, Book, "97801311036AB", "T", "A")

    def test_empty_title(self):
        self.assertRaises(LibraryError, Book, "9780131103627", "   ", "A")

    def test_zero_copies(self):
        self.assertRaises(LibraryError, Book, "9780131103627", "T", "A", 0)


# ------------------------------------------------------------------ Black-box (ECP + BVA)
class TC03_BlackBox_ISBN_BVA(unittest.TestCase):
    """ISBN length valid class = 13. Boundaries: 12, 13, 14."""

    def test_length_12_invalid(self):
        self.assertRaises(LibraryError, Book, "978013110362", "T", "A")

    def test_length_13_valid(self):
        self.assertEqual(Book("9780131103627", "T", "A").isbn, "9780131103627")

    def test_length_14_invalid(self):
        self.assertRaises(LibraryError, Book, "97801311036271", "T", "A")


class TC04_BlackBox_MemberAge_BVA(unittest.TestCase):
    """Valid age 5..100 -> test 4, 5, 6, 99, 100, 101."""

    def check(self, age, valid):
        if valid:
            self.assertEqual(Member("M0001", "Riya", age).age, age)
        else:
            self.assertRaises(LibraryError, Member, "M0001", "Riya", age)

    def test_age_4(self): self.check(4, False)
    def test_age_5(self): self.check(5, True)
    def test_age_6(self): self.check(6, True)
    def test_age_99(self): self.check(99, True)
    def test_age_100(self): self.check(100, True)
    def test_age_101(self): self.check(101, False)


class TC05_BlackBox_MemberID_ECP(unittest.TestCase):
    """Classes: valid 'M'+4 digits | wrong prefix | non-digit | wrong length."""

    def test_valid_id(self):
        self.assertEqual(Member("M1234", "A", 20).member_id, "M1234")

    def test_wrong_prefix(self):
        self.assertRaises(LibraryError, Member, "X1234", "A", 20)

    def test_non_digit(self):
        self.assertRaises(LibraryError, Member, "M12A4", "A", 20)

    def test_wrong_length(self):
        self.assertRaises(LibraryError, Member, "M123", "A", 20)


class TC06_BlackBox_Fine_BVA(unittest.TestCase):
    """Cap reached at 100 days (100*5 = 500). Boundaries: 99, 100, 101."""

    def test_99_days(self): self.assertEqual(calculate_fine(99), 495)
    def test_100_days(self): self.assertEqual(calculate_fine(100), 500)
    def test_101_days(self): self.assertEqual(calculate_fine(101), 500)
    def test_1_day(self): self.assertEqual(calculate_fine(1), 5)


# ------------------------------------------------------------------ Integration
class TC07_Integration_IssueReturn(unittest.TestCase):
    def setUp(self):
        self.lib = Library()
        self.lib.add_book(Book("9780131103627", "The C Programming Language", "Kernighan", 1))
        self.lib.add_book(Book("9780262033848", "Introduction to Algorithms", "Cormen", 5))
        self.lib.register_member(Member("M0001", "Siddhesh", 21))
        self.lib.register_member(Member("M0002", "Amit", 22))
        self.today = date(2025, 10, 1)

    def test_issue_returns_due_date_and_reduces_stock(self):
        due = self.lib.issue_book("M0001", "9780131103627", self.today)
        self.assertEqual(due, self.today + timedelta(days=14))
        self.assertEqual(self.lib.books["9780131103627"].available, 0)

    def test_issue_when_no_copies(self):
        self.lib.issue_book("M0001", "9780131103627", self.today)
        with self.assertRaisesRegex(LibraryError, "No copies"):
            self.lib.issue_book("M0002", "9780131103627", self.today)

    def test_return_on_time_no_fine(self):
        self.lib.issue_book("M0001", "9780131103627", self.today)
        fine = self.lib.return_book("M0001", "9780131103627", self.today + timedelta(days=14))
        self.assertEqual(fine, 0)
        self.assertEqual(self.lib.books["9780131103627"].available, 1)

    def test_return_late_fine(self):
        self.lib.issue_book("M0001", "9780131103627", self.today)
        fine = self.lib.return_book("M0001", "9780131103627", self.today + timedelta(days=20))
        self.assertEqual(fine, 30)   # 6 days late * 5

    def test_borrow_limit(self):
        for i in range(MAX_BOOKS_PER_MEMBER):
            isbn = f"978000000000{i}"
            self.lib.add_book(Book(isbn, f"Book {i}", "X"))
            self.lib.issue_book("M0002", isbn, self.today)
        with self.assertRaisesRegex(LibraryError, "limit"):
            self.lib.issue_book("M0002", "9780262033848", self.today)

    def test_duplicate_member(self):
        self.assertRaises(LibraryError, self.lib.register_member, Member("M0001", "Dup", 30))

    def test_return_not_issued(self):
        self.assertRaises(LibraryError, self.lib.return_book, "M0001", "9780262033848")

    def test_search_case_insensitive(self):
        self.assertEqual(len(self.lib.search("algorithms")), 1)
        self.assertEqual(len(self.lib.search("KERNIGHAN")), 1)

    def test_add_same_isbn_increases_copies(self):
        self.lib.add_book(Book("9780262033848", "Introduction to Algorithms", "Cormen", 2))
        self.assertEqual(self.lib.books["9780262033848"].total, 7)


if __name__ == "__main__":
    unittest.main(verbosity=2)
