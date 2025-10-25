Репозиторий с тестами для проверки загрузки файлов различных форматов, размеров и границ допустимых параметров. Включает позитивные тесты, негативные тесты, а также тесты для проверки граничных значений.

Структура репозитория

test_file_upload/
├── assets/                       # Тестовые файлы
│   
├── __init__.py
├── .gitignore
├── conftest.py                    # Общие фикстуры для тестов
├── README.md
├── test_file_upload_boundaries.py # Тесты граничных значений (размер файла, лимиты)
├── test_file_upload_formats.py    # Тесты разных форматов файлов
└── test_file_upload_negative.py   # Негативные тесты

Установка:

1. Клонируйте репозиторий:
git clone https://github.com/ваш_логин/test_file_upload.git
cd test_file_upload

2. Создайте виртуальное окружение (рекомендуется):
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

3. Установите необходимые библиотеки:
pip install requests pytest

4. Настройка
В каждом тестовом файле (test_file_upload_formats.py, test_file_upload_negative.py, test_file_upload_boundaries.py) замените BASE_URL на URL вашего сервера/эндпоинта загрузки файлов:
BASE_URL = "http://example.com/upload"

5. Запуск тестов

Запуск всех тестов:
pytest test_file_upload/

6. Запуск с подробным выводом:
pytest -v test_file_upload/

7. апуск конкретного тестового файла, например тестов форматов:
pytest test_file_upload/test_file_upload_formats.py -v

Типы тестов

1. test_file_upload_formats.py - загрузка тестовых файлов (image, audio, video, document) разных форматов.
2. test_file_upload_negative.py - негативные проверки
3. test_fiel_upload_boundaries - проверки на граничное значение 10 мб (если меняется, можно поменять в тесте)
