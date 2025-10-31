from rating_calculation.calculation import RatingCalculation


def test_reading_csv_valid(tmp_path, capsys):
    """Проверка корректного чтения CSV"""
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text("brand,rating\napple,4.5\nsamsung,4.8\n")

    rc = RatingCalculation.__new__(RatingCalculation)  # не вызываем __init__
    rc.aggregated_data = {}
    rc.process_row = RatingCalculation.process_row.__get__(rc)  # привязываем метод к объекту

    rc.reading_csv(str(csv_file))

    assert rc.aggregated_data == {
        "apple": [4.5],
        "samsung": [4.8]
    }

    captured = capsys.readouterr()
    assert "Brand пустой" not in captured.out
    assert "Неверный формат числа" not in captured.out


def test_reading_csv_empty_brand(tmp_path, capsys):
    """Проверка строки с пустым brand"""
    csv_file = tmp_path / "empty_brand.csv"
    csv_file.write_text("brand,rating\n,4.5\napple,4.8\n")

    rc = RatingCalculation.__new__(RatingCalculation)
    rc.aggregated_data = {}
    rc.process_row = RatingCalculation.process_row.__get__(rc)

    rc.reading_csv(str(csv_file))

    captured = capsys.readouterr()

    assert "Brand пустой" in captured.out
    assert rc.aggregated_data == {"apple": [4.8]}


def test_reading_csv_invalid_rating(tmp_path, capsys):
    """⚠️ Проверка строки с неверным рейтингом"""
    csv_file = tmp_path / "invalid_rating.csv"
    csv_file.write_text("brand,rating\napple,abc\nsamsung,4.9\n")

    rc = RatingCalculation.__new__(RatingCalculation)
    rc.aggregated_data = {}
    rc.process_row = RatingCalculation.process_row.__get__(rc)

    rc.reading_csv(str(csv_file))

    captured = capsys.readouterr()

    assert "Неверный формат числа" in captured.out
    assert rc.aggregated_data == {"samsung": [4.9]}
