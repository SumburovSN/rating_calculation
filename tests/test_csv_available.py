from rating_calculation.calculation import RatingCalculation


def test_csv_available_file_not_found(tmp_path):
    # путь к несуществующему файлу
    missing = tmp_path / "no_such_file.csv"
    # вызываем staticmethod без создания экземпляра (чтобы не триггерить argparse)
    assert RatingCalculation.csv_available(str(missing)) is False


def test_csv_available_file_exists(tmp_path):
    # создаём файл
    p = tmp_path / "exists.csv"
    p.write_text("name,brand,price,rating\nitem,Brand,10,4.5\n")
    assert RatingCalculation.csv_available(str(p)) is True


def test_csv_available_directory_instead_of_file(tmp_path):
    d = tmp_path / "a_dir"
    d.mkdir()
    # если передан путь к каталогу, os.path.isfile вернёт False
    assert RatingCalculation.csv_available(str(d)) is False
