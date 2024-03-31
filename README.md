<h1> Hey there! I'm Sergey 👋 </h1>
<h2> It are tests for exam TechMeSkills </h2>

<h3> 👨🏻‍💻 About Project </h3>

- 🔭 &nbsp; This project is a comprehensive testing suite designed for the 21vek online hypermarket. It includes both API
  and UI (User Interface) tests that ensure the website operates reliably and meets the expected performance benchmarks.
  The API testing component is focused on the backend services, validating the functionality, reliability, security, and
  performance of the web services. It checks the endpoints for correct responses, error handling, and adherence to the
  RESTful architecture principles.

<h3>🛠 Tech Stack</h3>

- 💻 &nbsp; **Python** | Основной язык программирования, используемый для написания тестов.
- 🧪 &nbsp; **Pytest** | Фреймворк для модульного и функционального тестирования, обеспечивающий удобные механизмы
  ассертов и фикстур.
- 🌐 &nbsp; **Selenium WebDriver** | Инструмент для автоматизации действий веб-браузера, используемый в UI тестировании.
- 📊 &nbsp; **Allure Framework** | Инструмент для визуализации результатов тестирования, предоставляющий подробные
  отчеты.
- 📁 &nbsp; **Git** | Система контроля версий для отслеживания изменений в коде тестов и совместной работы.

<h3> 🤝🏻 Connect with Me if need</h3>

<p align="left">
&nbsp; <a href="mailto:blotskiy.sergey@gmail.com" target="_blank" rel="noopener noreferrer"><img src="https://img.icons8.com/plasticine/100/000000/gmail.png"  width="50" /></a>
</p>

⭐️ From [SergeyBl](https://github.com/Sergey-Bl)

## Установка и настройка

### Установка Python

Перед тем, как приступить к работе, убедитесь, что на вашем компьютере установлен Python версии 3.6 или выше. Вы можете
скачать Python с официального сайта: [python.org](https://www.python.org/).

### Установка зависимостей

Перед началом тестов установите все необходимые зависимости из файла `requirements.txt` с помощью следующей команды,
выполняемой в корне проекта:
`pip install -r requirements.txt`

# **Manual test run start:**

## **For start API tests:**

**Сommand for run tests:** `pytest tests/tests_api/test_api.py`

**Module tests runs:**

Smoke API - `pytest -m api_smoke tests/tests_api/test_api.py`

User API - `pytest -m api_user tests/tests_api/test_api.py`

## **For start UI tests:**

**Сommand for run tests:** `pytest tests/tests_ui/tests_21vek.py`

Запуск тестов по браузерам

`pytest --headless=no --browser=chrome`

`pytest --headless=yes --browser=firefox`

headless меняем на yes/no в зависимости от нужности

----

#### **После запуска тестов и когда они прошли можно сгенерировать репорт командой `allure serve allure_logs`**

----

# **FAST tests run:**

**API:** File for run API tests and collect allure report = **_run_api_tests.sh_** - `located /test_runners`

**UI:** File for run UI tests and collect allure report = **_run_ui_tests.sh_** - `located /test_runners`


----
## **Notes:**
- В коде есть создание логов запусков апи и юай тестов
- Есть создание скриншотов после каждого удачного или неудачного теста с логами
- В коде заложена отчистка логов и скринов перед запуском тестов
- Код автоматически генерит так же allure репорт 
- На юай тесты и на апи тесты разбиты свои conftest с своими параметрами