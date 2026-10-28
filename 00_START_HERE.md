# START HERE – BE Comp Sem 7 Practical Exam (SPPU 2019 Pattern)

**LP-III (410246):** DAA · ML · BT  **LP-IV (410247):** CSDF · STQA

## Folder map
```
Sem7_Practicals/
├── 00_START_HERE.md            <- this file
├── 00_SETUP/                   check_environment.py, requirements.txt
├── LP3_DAA/   A1..A5 + A6 mini project   (C++ and Python, sample outputs)
├── LP3_ML/    A1..A6 + A7 mini project   (executed notebooks + datasets + HTML copies)
├── LP3_BT/    A1..A6 + A7 mini project   (.sol contracts, guides, survey report, dApp)
├── LP4_CSDF/  A1..A6                     (Python programs, Wireshark capture, Snort rules)
├── LP4_STQA/  Mini project               (app, test plan, test cases, automated tests, report)
└── 99_Original_Code_Backup/              (your old code from the sem7 repo, for reference only)
```
Every subject folder has a **README.md** with the exact problem statements, run commands and **viva quick answers**.

## In the exam hall (first 5 minutes)
1. Copy the whole `Sem7_Practicals` folder to the Desktop. Running from the pendrive works but is slower.
2. Open a terminal / command prompt in that folder and run:
   ```
   python 00_SETUP/check_environment.py
   ```
   (Windows lab PCs may need `py` instead of `python`.)
3. If something is missing: `python -m pip install -r 00_SETUP/requirements.txt`
4. Open only the slip's assignment folder → run → show the output → explain from the README.

## Checklist – the day before
- [ ] Copy `Sem7_Practicals` to the pendrive. Open 2–3 files from the pendrive to confirm the copy works.
- [ ] Read the README of each subject (the viva section especially).
- [ ] Run at least one program per subject once yourself.
- [ ] **BT:** MetaMask installed in your browser, Sepolia test ETH in the wallet, and your 12-word recovery phrase written down safely (not on the pendrive).
- [ ] **ML:** skim each notebook's markdown and conclusion. Know the formulas (R2, RMSE, precision, recall).
- [ ] **CSDF A6:** know 5 Wireshark filters and how Follow HTTP Stream shows a plain-text password.
- [ ] **STQA:** practise the demo order in `LP4_STQA/MiniProject_Library_App_Testing/README.md`.
- [ ] Print (or keep handy) the BT survey report if your journal needs it.

## If something goes wrong
| Problem | Fix |
|---|---|
| `g++` not found | Run the Python version of the DAA program, or use onlinegdb.com |
| Jupyter not installed | `pip install notebook`, or use Google Colab, or show the `.html` copy of the executed notebook |
| `FileNotFoundError` for a CSV | Open the notebook **from its own folder** (CSV paths are relative) |
| TensorFlow missing (ML A3) | Nothing to do: the notebook auto-switches to the scikit-learn neural network |
| Pillow missing (CSDF A2) | The program automatically uses a text CAPTCHA, or `pip install pillow` |
| No internet for Remix (BT) | Show the `.sol` code + README steps, and explain the gas table |
| Slow PC for Uber Random Forest | Change `n_estimators=50` to `20` in that cell |
