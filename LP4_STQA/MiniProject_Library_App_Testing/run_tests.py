# STQA Mini Project - Test runner + Test Report generator
# Runs all tests, measures time, writes Test_Report.txt with pass/fail per test case
# and an acceptance decision based on the pass/fail criteria in the Test Plan.
# Run: python run_tests.py
import datetime
import time
import unittest

ACCEPTANCE_PASS_RATE = 95.0   # % of test cases that must pass (from Test Plan)


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append((test.id(), "PASS", ""))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.records.append((test.id(), "FAIL", str(err[1])))

    def addError(self, test, err):
        super().addError(test, err)
        self.records.append((test.id(), "ERROR", str(err[1])))


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover(".", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2, resultclass=RecordingResult)
    start = time.time()
    result = runner.run(suite)
    elapsed = time.time() - start

    total = result.testsRun
    passed = sum(1 for r in result.records if r[1] == "PASS")
    rate = 100 * passed / total if total else 0
    accepted = rate >= ACCEPTANCE_PASS_RATE and not result.errors

    lines = ["TEST SUMMARY REPORT - Library Management System",
             "=" * 84,
             f"Date            : {datetime.datetime.now():%Y-%m-%d %H:%M}",
             f"Total test cases: {total}",
             f"Passed          : {passed}",
             f"Failed          : {len(result.failures)}",
             f"Errors          : {len(result.errors)}",
             f"Pass rate       : {rate:.1f}%",
             f"Execution time  : {elapsed:.3f} s",
             "", f"{'Test case':<76}Status", "-" * 84]
    for tid, status, msg in result.records:
        name = tid.replace("test_library.", "")
        lines.append(f"{name:<76}{status}")
        if msg:
            lines.append(f"    -> {msg}")
    lines += ["", "ACCEPTANCE CRITERIA: pass rate >= 95% and no errors",
              f"DECISION: {'ACCEPTED - application is ready for release' if accepted else 'REJECTED - fix defects and re-test'}"]

    report = "\n".join(lines)
    with open("Test_Report.txt", "w") as f:
        f.write(report + "\n")
    print("\n" + report)
    print("\nSaved to Test_Report.txt")
