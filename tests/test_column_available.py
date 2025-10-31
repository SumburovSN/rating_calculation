from rating_calculation.calculation import RatingCalculation


def test_column_available_valid_csv(tmp_path, capsys):
    """Файл с корректными колонками"""
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text("name,brand,price,rating\nitem,BrandA,10,4.5\n")
    result = RatingCalculation.column_available(str(csv_file))

    assert result is True
    captured = capsys.readouterr()
    assert "ValueError" not in captured.out
    assert "MissingColumnError" not in captured.out


def test_column_available_no_header(tmp_path, capsys):
    """Файл без заголовка (DictReader не находит fieldnames)"""
    csv_file = tmp_path / "no_header.csv"
    # Симулируем отсутствие заголовка
    csv_file.write_text("")
    result = RatingCalculation.column_available(str(csv_file))

    assert result is False
    captured = capsys.readouterr()
    assert "не содержит заголовка" in captured.out


def test_column_available_missing_columns(tmp_path, capsys):
    """Файл без нужных колонок 'brand' и 'rating'"""
    csv_file = tmp_path / "missing_cols.csv"
    csv_file.write_text("name,price\nitem,100\n")
    result = RatingCalculation.column_available(str(csv_file))

    assert result is False
    captured = capsys.readouterr()
    assert "MissingColumnError" in captured.out
