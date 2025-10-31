import pytest
from rating_calculation.calculation import RatingCalculation


@pytest.mark.parametrize(
    "initial_data, brand_to_add, rating_to_add, expected_data",
    [
        ({}, "apple", 4.8, {"apple": [4.8]}),                           # Новый бренд
        ({"apple": [4.8]}, "apple", 4.9, {"apple": [4.8, 4.9]}),       # Добавление к существующему бренду
        ({}, "samsung", 4.7, {"samsung": [4.7]}),                      # Новый бренд другой
        ({"apple": [4.8]}, "xiaomi", 4.5, {"apple": [4.8], "xiaomi": [4.5]}), # Несколько брендов
    ]
)
def test_process_row_param(initial_data, brand_to_add, rating_to_add, expected_data):
    rc = RatingCalculation.__new__(RatingCalculation)
    rc.aggregated_data = initial_data.copy()  # создаём копию, чтобы не мутировать параметр

    rc.process_row(brand_to_add, rating_to_add)

    assert rc.aggregated_data == expected_data
