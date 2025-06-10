# Тестирование: Delivery (Api и UI)

Проект содержит автоматизированные тесты для API и пользовательского интерфейса (UI) Деливери.

## Структура проекта
DIPLOM
1) API_test
  * pages/api_client
  * test_broccoli_salad_search.py
  * test_kontora_search.py
  * test_no_results_fallback.py
  * test_nonsense_search.py
  * test_pyaterochka_search.py
2) UI_test
  * pages/market_page.py
  * test_click_burgers.py
  * test_search_blyudo.py
  * test_search_market.py
  * test_search_tovar.py
  * test_sushi_button.py
3) .gitignore
4) requirements.txt # Зависимости
5) README.md # Документация`

## Запуск тестов

**Предварительно:**
- Установите браузер Chrome
- запускать тесты через интерфейс / через терминал

### Запуск через терминал
#### 1. UI-тесты

   `cd C:\Users\evill\OneDrive\Рабочий стол\DIPLOM` - перейти в директорию UI_test
   `python -m pytest UI_test/` - для запуска тестов
   
#### 2. API-тесты

   `cd C:\Users\evill\OneDrive\Рабочий стол\DIPLOM` - перейти в директорию API_test
   `python -m pytest API_test/` - для запуска тестов
   
#### 3. Все тесты
   `cd C:\Users\evill\OneDrive\Рабочий стол\DIPLOM` перейти в директорию DIPLOM 
   `python -m pytest --alluredir allure-result` - для запуска тестов

  В директории с тестами появится папка allure-result. Там сохранятся отчеты о тестах.
  
#### Введите команду ниже — сгенерируется отчет о тестах:
    `allure serve allure-result`
Отчет откроется на локальном сервере в окне вашего браузера.
Overview — раздел с общей информацией: сколько всего тестов запустили, процент успешных тестов, доля успешных и неуспешных тестов.

## Ссылка на финальный ручной проект:
https://ae90.yonote.ru/share/ed577c4d-10ea-4f4b-81f8-6d5782cec290