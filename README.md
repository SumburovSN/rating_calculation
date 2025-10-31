API для процессинга csv-файлов с данными (колонками) о брендах('brand') и рейтингах ('rating')

Логика: в rating_calculation/calculations.py

Запуск API: \rating-calculation> python main.py -f products1.csv products2.csv

Запуск тестов: rating-calculation> python -m pytest -v (для добавления корня проекта в sys.path)