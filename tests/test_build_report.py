from rating_calculation.calculation import RatingCalculation


def test_build_report_basic():
    """Проверка корректного расчёта среднего рейтинга"""
    rc = RatingCalculation.__new__(RatingCalculation)
    rc.aggregated_data = {
        "apple": [4.5, 5.0],
        "samsung": [4.8],
        "xiaomi": [4.6, 4.4, 4.5]
    }
    rc.calculated_data = []

    rc.build_report()

    # Проверка рассчитанных средних значений
    expected = [
        ["apple", (4.5 + 5.0)/2],
        ["samsung", 4.8],
        ["xiaomi", (4.6 + 4.4 + 4.5)/3]
    ]

    # Так как метод сортирует по имени бренда
    expected_sorted = sorted(expected, key=lambda x: x[0])

    assert rc.calculated_data == expected_sorted


def test_build_report_empty():
    """Проверка метода при пустом aggregated_data"""
    rc = RatingCalculation.__new__(RatingCalculation)
    rc.aggregated_data = {}
    rc.calculated_data = []

    rc.build_report()

    assert rc.calculated_data == []
