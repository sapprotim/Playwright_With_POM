# HPB Dashboard Test Automation

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Framework-Playwright-green.svg)](https://playwright.dev/python/)
[![Pytest](https://img.shields.io/badge/Tested%20With-Pytest-orange.svg)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-Internal--Use-lightgrey.svg)]()

End-to-end test automation framework for the **Health Promotion Board (HPB) Dashboard**, covering clinical/lifestyle score calculations, nudges/alerts, and dashboard logic across multiple user roles — built with Python, Playwright, and Pytest.

---

## Purpose

This suite contains **210+ automated test cases** verifying all essential workflows and data logic on the HPB Dashboard. It is actively maintained and expanded alongside new feature development.

### User Roles Under Test

| Role            | Description                             |
|-----------------|-----------------------------------------|
| ORG Admin       | HPB Admin — system-level access         |
| Facility Admin  | Fullerton Health — facility manager     |
| Department Admin| Clinic Admin — clinic access level      |
| STM             | Doctor — service-level functionality    |

---

## Technology Stack

| Component       | Tool / Framework     |
|-----------------|----------------------|
| Language        | Python 3.x           |
| Automation      | Playwright (Python)  |
| Test Runner     | Pytest               |
| Reporting       | pytest-html          |
| Data Source     | Excel via `pandas`   |

---

## Project Structure

```
├── pages/                  # Page Object Model classes
│   ├── patient_logs/       # Patient log interactions (FBG, HbA1c, lipids, etc.)
│   ├── records/            # Records & document upload pages
│   └── user_basic_info/    # User profile, trends, wellness score
├── tests/                  # Test suites per role
│   ├── test_HPB_Admin.py
│   ├── test_fullerton_health.py
│   ├── test_Clinic.py
│   └── test_doctor.py
├── conftest.py             # Shared fixtures & screenshot hooks
├── data.py                 # Data loader (reads from data.xlsx)
├── config.py               # Credentials config (NOT committed — see below)
├── data.xlsx               # Test data workbook (NOT committed — see below)
└── requirements.txt        # Python dependencies
```

---

## Security — Credentials & Test Data

**`config.py` and `data.xlsx` are excluded from version control** (listed in `.gitignore`) because they contain login credentials and personally identifiable test data.

To set up locally, create `config.py` in the project root:

```python
# config.py — do NOT commit this file
BASE_URL  = "https://<your-environment-url>/#/login"
USERNAME  = "<your-test-account-email>"
PASSWORD  = "<your-test-account-password>"
```

Also obtain `data.xlsx` from the team and place it in the project root. It must contain three sheets: **Login**, **Search**, and **Link** with the expected column layout (see `data.py` for row/column indices).

---

## Installation

### Prerequisites

- Python 3.8+
- pip

### Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install manually:

```bash
pip install pytest==8.3.3
pip install pluggy==1.5.0
pip install pytest-faker==33.0.0
pip install pytest-base-url==2.1.0
pip install pytest-html==4.1.1
pip install pytest-metadata==3.1.1
pip install pytest-playwright==0.7.0
pip install pandas openpyxl
```

### Install Playwright browsers

```bash
playwright install
```

---

## Running Tests

```bash
# All tests — headless, with HTML report
pytest . --html=report.html --self-contained-html

# All tests — headed (visible browser)
pytest . --headed --html=report.html --self-contained-html

# Single test module
pytest tests/test_doctor.py
pytest tests/test_Clinic.py
pytest tests/test_fullerton_health.py
pytest tests/test_HPB_Admin.py

# Single test case by name
pytest -k test_roleDoc_trends_generate_wellness_plan

# Re-run only previously failed tests
pytest --last-failed --html=failed_report.html --self-contained-html
```

---

## Reporting

After a test run, open the generated HTML report:

```bash
# Windows
start report.html

# macOS / Linux
open report.html
```

Screenshots are automatically captured for each test (pass and fail) and embedded in the HTML report.

---

## Contributing

1. Branch from `main` for new features or fixes.
2. Follow the Page Object Model pattern — keep all locator/interaction logic inside `pages/`.
3. Keep test data in `data.xlsx`; never hardcode credentials in test files.
4. Run the full suite before submitting a PR.
