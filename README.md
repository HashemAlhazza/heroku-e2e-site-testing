Got it! Here's the full `README.md` file, properly formatted so you can copy and paste it directly:

```markdown
# HerokuApp UI Testing — Playwright & Selenium

This project demonstrates automated UI testing of the website [the-internet.herokuapp.com](https://the-internet.herokuapp.com) using two different Python frameworks: **Selenium** and **Playwright**. The purpose is to explore and compare both tools by dividing the testing responsibilities between them.

---

## 📁 Project Structure

```

.
├── Python\_Playwright/
│   ├── Features\_Gherkins/
│   │   └── herokuapp.feature         # Gherkin scenarios for Playwright BDD
│   ├── test\_two\_steps.py            # Step definitions for feature file
│   └── test\_two.py                  # Manual Playwright tests
│
├── Python\_Selenium/
│   └── test\_one.py                  # Selenium-based test cases

````

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

## 📦 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/herokuapp-ui-testing.git
   cd herokuapp-ui-testing
````

2. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies**

   For both frameworks:

   ```bash
   pip install -r requirements.txt
   ```

   *(Create a combined `requirements.txt` if needed with both Selenium and Playwright dependencies.)*

4. **Install Playwright browsers**

   ```bash
   playwright install
   ```

---

## 🧪 How to Run Tests

### ▶️ Playwright Tests

Run manually scripted Playwright tests:

```bash
cd Python_Playwright
pytest test_two.py
```

### ▶️ BDD Tests (Playwright + Gherkin)

```bash
cd Python_Playwright
pytest
```

Make sure the `.feature` file and `test_two_steps.py` are in the same module path.

### ▶️ Selenium Tests

```bash
cd Python_Selenium
pytest test_one.py
```

---

## 🤔 Why Use Both?

* 📌 To compare **ease of use**, **speed**, and **readability** between Selenium and Playwright.
* 📌 To explore **BDD** using Gherkin syntax for non-technical stakeholders.
* 📌 To practice real-world test automation with a variety of tools and design patterns.

---

## ✅ Current Status

* 🔄 Selenium tests: ✅ Completed for first half of features
* 🔄 Playwright tests: ✅ Completed for second half (manual + BDD)
* 🧪 Project is functional and ready for future enhancements

---

## 👨‍💻 Author

**Hashem Mohammed** — Embedded Systems & QA Engineer
[LinkedIn Profile](https://www.linkedin.com/in/hashem-al-hazzaa-032183183/)
