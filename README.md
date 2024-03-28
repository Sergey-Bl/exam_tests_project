<h1> Hey there! I'm Sergey 👋 </h1>
<h2> It are tests for exam TechMeSkills </h2>

<h3> 👨🏻‍💻 About Project </h3>

- 🔭 &nbsp; This project is a comprehensive testing suite designed for the 21vek online hypermarket. It includes both API
  and UI (User Interface) tests that ensure the website operates reliably and meets the expected performance benchmarks.
  The API testing component is focused on the backend services, validating the functionality, reliability, security, and
  performance of the web services. It checks the endpoints for correct responses, error handling, and adherence to the
  RESTful architecture principles.

<h3>🛠 Tech Stack</h3>

- 💻 &nbsp; Python | Pytest
- 🌐 &nbsp; Selenium WebDriver

<br>


</br>



<h3> 🤝🏻 Connect with Me if need</h3>

<p align="left">
&nbsp; <a href="mailto:blotskiy.sergey@gmail.com" target="_blank" rel="noopener noreferrer"><img src="https://img.icons8.com/plasticine/100/000000/gmail.png"  width="50" /></a>
</p>

⭐️ From [SergeyBl](https://github.com/Sergey-Bl)

# **Manual test run start:**

## **For start API tests:**

**1 command for run tests:** `pytest tests/tests_api/test_api.py --alluredir=logs`

**2 command to create report:** `allure generate tests/tests_api/logs -o reports --clean`

_Without report/allure_:`pytest tests/tests_api/test_api.py`

**Module tests runs:**

Smoke API - `pytest -m api_smoke tests/tests_api/test_api.py`

User API - `pytest -m api_user tests/tests_api/test_api.py`

## **For start UI tests:**

**1 command for run tests:** `pytest tests/tests_ui/tests_21vek.py --alluredir=logs`

**2 command to create report:** `allure generate tests/tests_api/logs -o reports --clean`

_Without report/allure:_
`pytest tests/tests_ui/tests_21vek.py`

Запуск тестов по браузерам
`pytest --headless=no --browser=chrome`
`pytest --headless=yes --browser=firefox`
headless меняем на yes/no в зависимости от нужности

# **FAST tests run:**

**API:** File for run API tests and collect allure report = **_run_api_tests.sh_** - `located /test_runners`

**UI:** File for run UI tests and collect allure report = **_run_ui_tests.sh_** - `located /test_runners`
