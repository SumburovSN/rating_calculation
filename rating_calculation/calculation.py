import csv
import argparse
from datetime import datetime
import os
from tabulate import tabulate


class RatingCalculation:
    def __init__(self):
        self.aggregated_data = {}
        self.calculated_data = []
        self.args = self.add_arguments()
        self.csv_files = self.args.files
        self.path_csv_files = self.args.path
        self.report_file = self.args.report

    @staticmethod
    def add_arguments():
        parser = argparse.ArgumentParser(description='Обработка csv файлов')
        parser.add_argument('-f', '--files', nargs='+', required=True, help='Список csv файлов для обработки')
        parser.add_argument('-p', '--path', default="data", help='Путь к csv файлам (default "./data")')
        parser.add_argument('-r', '--report', default="average-rating", help='provide report filename')
        arguments = parser.parse_args()
        return arguments

    @staticmethod
    def csv_available(file_csv):
        if not os.path.isfile(file_csv):
            print(f"FileNotFoundError: CSV файл не найден: {file_csv}")
            return False
        return True

    @staticmethod
    def column_available(file_csv):
        try:
            with open(file_csv, 'r', newline='') as file:
                reader = csv.DictReader(file)
                if reader.fieldnames is None:
                    print(f"ValueError: {file_csv} не содержит заголовка")
                    return False
                if 'brand' not in reader.fieldnames or 'rating' not in reader.fieldnames:
                    print(f"MissingColumnError: В заголовке {file_csv} отсутствуют требуемые колонки "
                          f"'brand' и/или 'rating'. ")
                    return False
        except Exception as exc:
            print(exc)
        return True

    def reading_csv(self, file_csv):
        with open(file_csv, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row['brand']:
                    print(f'Brand пустой в файле {file_csv} в строке {row}')
                    continue
                try:
                    rating = float(row['rating'])
                except ValueError:
                    print(f'Неверный формат числа {row["rating"]} в файле {file_csv} в строке {row}')
                    continue
                self.process_row(row['brand'], rating)

    def process_row(self, brand, rating):
        if brand in self.aggregated_data.keys():
            self.aggregated_data[brand].append(rating)
        else:
            self.aggregated_data.update({brand: [rating]})

    def build_report(self):
        for brand, rating_list in self.aggregated_data.items():
            ratings_sum = 0
            for rating in rating_list:
                ratings_sum += rating
            average_rating = ratings_sum / len(rating_list)
            self.calculated_data.append([brand, average_rating])
        self.calculated_data = sorted(self.calculated_data, key=lambda x: x[0])

    def print_report(self):
        with open(self.report_file, "w", encoding="utf-8") as file:
            file.write(f'Отчет по рейтингу брендов от {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} \n')
            file.write(tabulate(self.calculated_data, headers=('brand', 'rating'), tablefmt="grid", floatfmt=".2f"))

    def get_report(self):
        for file in self.csv_files:
            filename = os.path.join(self.path_csv_files, file)
            if not self.csv_available(filename):
                print("Отчет не создан из-за отсутствия файла данных")
                return
            elif not self.column_available(filename):
                print("Отчет не создан из-за некорректного формата данных")
                return
            else:
                self.reading_csv(filename)
        self.build_report()
        self.print_report()
        print(tabulate(self.calculated_data, headers=('brand', 'rating'), tablefmt="grid", floatfmt=".2f"))


if __name__ == '__main__':
    rate_run = RatingCalculation()

    rate_run.get_report()
    # для проверки
    print(rate_run.aggregated_data)
    # import sys
    #
    # print(sys.path)
