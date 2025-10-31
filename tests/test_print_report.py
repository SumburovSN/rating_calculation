import os
# from datetime import datetime
# from tabulate import tabulate
from rating_calculation.calculation import RatingCalculation

def test_print_report_creates_file(tmp_path):
    # Создаём объект без __init__
    rc = RatingCalculation.__new__(RatingCalculation)
    rc.calculated_data = [
        ["apple", 4.75],
        ["samsung", 4.8]
    ]
    rc.report_file = tmp_path / "report.txt"

    # Вызов метода
    rc.print_report()

    # Проверяем, что файл создан
    assert os.path.isfile(rc.report_file)

    # Проверяем содержимое
    content = rc.report_file.read_text(encoding="utf-8")

    # Заголовок с датой должен присутствовать
    assert "Отчет по рейтингу брендов от" in content

    # Данные из calculated_data должны присутствовать
    assert "apple" in content
    assert "4.75" in content
    assert "samsung" in content
    assert "4.80" in content  # tabulate округляет floatfmt=".2f"
