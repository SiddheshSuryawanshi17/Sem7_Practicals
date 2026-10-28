# LP-IV : Software Testing and Quality Assurance (STQA)

For the 2019 pattern, the STQA lab is a **mini project**. Everything is in `MiniProject_Library_App_Testing/`; read its README for the 10-minute demo order.

Quick run (no installs needed):
```bash
cd MiniProject_Library_App_Testing
python library.py        # the application
python run_tests.py      # 34 unit + integration + black-box tests -> Test_Report.txt (ACCEPTED)
```

## Viva quick answers
- **Verification** ("are we building the product right?": reviews, inspections, static) vs **Validation** ("are we building the right product?": testing, dynamic).
- **Error → Fault/Defect/Bug → Failure.** A human error introduces a defect in the code, which causes a failure at run time.
- **Black-box** (no code knowledge): ECP, BVA, decision table, state transition, cause-effect graph. **White-box** (code knowledge): statement, branch, path coverage, cyclomatic complexity, data-flow. **Grey-box** = both.
- **Cyclomatic complexity** V(G) = E − N + 2P = number of decisions + 1 = number of independent paths.
- **BVA:** test min−1, min, min+1, max−1, max, max+1. **ECP:** one value from each valid/invalid class.
- **Levels:** Unit → Integration (top-down with stubs, bottom-up with drivers, big-bang, sandwich) → System → Acceptance (alpha at the developer site, beta at the customer site).
- **Types:** functional, regression, smoke (build OK?), sanity (fix OK?), performance (load, stress), security, usability, compatibility.
- **STLC:** requirement analysis → test planning → test case design → environment setup → execution → closure.
- **Bug life cycle:** New → Assigned → Open → Fixed → Retest → Verified → Closed (or Reopened / Rejected / Deferred / Duplicate).
- **Severity** (impact on the system, set by the tester) vs **Priority** (urgency to fix, set by the manager/business). Example: logo misspelt on the home page = low severity, high priority.
- **Test plan (IEEE 829):** identifier, introduction, test items, features to be tested / not tested, approach, pass/fail criteria, suspension/resumption criteria, deliverables, environment, responsibilities, schedule, risks, approvals.
- **Bug taxonomy:** a classification of the kinds of bugs (requirement, functional, boundary, data, integration, UI, performance, security…) used to design tests that target each kind.
- **Tools:** Selenium (web UI automation: WebDriver, IDE, Grid), JUnit/TestNG/pytest/unittest (unit), JMeter/LoadRunner (performance), Postman (API), Jira/Bugzilla (defect tracking), Appium (mobile).
- **Selenium locators:** id, name, className, tagName, linkText, partialLinkText, cssSelector, xpath.
- **Quality:** ISO 9126 / ISO 25010 characteristics (functionality, reliability, usability, efficiency, maintainability, portability). **CMMI** levels 1–5. **Six Sigma** = 3.4 defects per million. **QA** (process, preventive) vs **QC** (product, detective).
