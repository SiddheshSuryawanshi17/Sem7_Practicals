# STQA Mini Project – Library Management System Testing

In the 2019 pattern, STQA in LP-IV is a **mini project**. This folder covers every part of the problem statement:

| Requirement in syllabus | File |
|---|---|
| Small application | `library.py` (run: `python library.py`) |
| Test plan + features to be tested + bug taxonomy | `Test_Plan.md` |
| Test cases with test procedures | `Test_Cases.csv` (opens in Excel) |
| White-box + black-box, unit + integration testing with a tool | `test_library.py` (Python unittest) |
| UI black-box automation tool | `selenium_ui_test/selenium_login_test.py` + `login.html` |
| Test report with pass/fail criteria and acceptance decision | `python run_tests.py` → `Test_Report.txt` |

## Exam demo order (10 min)
1. `python library.py` → add a member, issue a book, return it → show the fine.
2. Open `Test_Plan.md` → explain features, approach (ECP, BVA, branch coverage) and bug taxonomy.
3. Open `Test_Cases.csv` in Excel.
4. `python run_tests.py` → 34 tests pass → report says **ACCEPTED**.
5. **Show a defect being caught:** in `library.py` change `if not (5 <= age <= 100)` to `if not (5 <= age < 100)` → run again → `test_age_100` FAILS → decision **REJECTED**. Undo the change.
6. (If Selenium + Chrome is available) `pip install selenium` → `python selenium_ui_test/selenium_login_test.py`. The browser opens and the 5 UI tests run automatically.

## If the examiner asks for Java / JUnit instead
The same tests in JUnit 5 look like this:
```java
@Test void fineIsCapped() { assertEquals(500, Library.calculateFine(1000)); }
@Test void negativeDaysThrows() { assertThrows(IllegalArgumentException.class, () -> Library.calculateFine(-1)); }
```
In Eclipse: right-click the project → *Build Path → Add Libraries → JUnit 5* → right-click the test class → *Run As → JUnit Test* (green bar = pass).
