# HerokuApp UI Testing — Playwright & Selenium

This project demonstrates automated UI testing of the website [the-internet.herokuapp.com](https://the-internet.herokuapp.com) using two different Python frameworks: **Selenium** and **Playwright**. The purpose is to explore and compare both tools by dividing the testing responsibilities between them.

---

## 🚀 What Is Being Tested?

The website under test is [`https://the-internet.herokuapp.com`](https://the-internet.herokuapp.com), a site designed for practicing automated UI testing scenarios.

To compare the two frameworks:

- ✅ **Selenium (Python_Selenium/)** is used to test the **first half** of the website features.
- ✅ **Playwright (Python_Playwright/)** is used to test the **second half**, with two approaches:
  - Traditional Playwright scripting (`test_two.py`)
  - BDD-style tests using `pytest-bdd` and `.feature` files (`herokuapp.feature` + `test_two_steps.py`)

---

## 🧪 Technologies Used

### 🕸️ Browsers & UI Automation
- **Selenium (Python)** — WebDriver-based automation
- **Playwright (Python)** — Modern automation tool with multi-browser support

### 📘 BDD (Behavior-Driven Development)
- **pytest-bdd** — Enables `.feature` files and step definitions for Playwright

---

### 🧪 How to Run Tests

This project is structured into two main directories: `Python_Playwright` and `Python_Selenium`. Each has its own set of tests that can be run independently using `pytest`.

> ℹ️ **Note:** All commands below should be executed from within each Framework foler root directory.

#### ▶️ Run Playwright Tests

1.  **Change to the Python_Playwright directory:**
    ```bash
    cd Python_Playwright
    ```
2.  **Run the tests:**
    -   To run the traditional scripted tests (`test_two.py`):
        ```powershell
        pytest test_two.py -v --headed
        ```
    -   To run the BDD-style tests (`.feature` file):
        ```powershell
        pytest test_two_steps.py -s -v --headed
        ```

#### ▶️ Run Selenium Tests

1.  **Change to the Selenium directory:**
    ```bash
    cd Python_Selenium
    ```
2.  **Run the tests:**
    ```powershell
    pytest test_one.py -v
    ```
    > ℹ️ **Note:** Selenium tests do not need the `--headed` flag, as the browser is always visible by default unless configured otherwise.