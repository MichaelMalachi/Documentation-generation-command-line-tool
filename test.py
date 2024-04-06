import os  # Импорт модуля для работы с операционной системой
import re  # Импорт модуля для работы с регулярными выражениями
import argparse  # Импорт модуля для разбора аргументов командной строки

class DocumentationGenerator:
    """
    Класс для генерации документации на основе исходного кода.
    """
    def __init__(self, source_dir, output_dir, filter_expr=None, profile=None):
        """
        Конструктор класса DocumentationGenerator.

        :param source_dir: Директория с исходным кодом.
        :param output_dir: Директория для сохранения сгенерированных файлов документации.
        :param filter_expr: Регулярное выражение для фильтрации файлов.
        :param profile: Профиль регулярных выражений.
        """
        # Инициализация параметров объекта
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.filter_expr = filter_expr
        self.profile = profile

    def generate_documentation(self):
        """
        Метод для генерации документации.

        Создает HTML-файлы документации на основе исходного кода.
        """
        # Список файлов, которые нужно обработать
        files_to_process = []
        # Если задано регулярное выражение для фильтрации файлов
        if self.filter_expr:
            # Компиляция регулярного выражения
            filter_pattern = re.compile(self.filter_expr)
            # Обход всех файлов в директории и её поддиректориях
            for root, _, files in os.walk(self.source_dir):
                for file in files:
                    # Проверка, соответствует ли имя файла регулярному выражению
                    if filter_pattern.match(file):
                        files_to_process.append(os.path.join(root, file))
        else:
            # Если регулярное выражение не задано, обработать все файлы в директории и её поддиректориях
            for root, _, files in os.walk(self.source_dir):
                files_to_process.extend([os.path.join(root, file) for file in files])

        # Создание документации для каждого файла
        for file_path in files_to_process:
            with open(file_path, 'r') as f:
                file_content = f.read()

            # Поиск заголовка файла
            file_title_match = re.search(r'/\*[\s\*]*File: (.+?)\*/', file_content)
            if file_title_match:
                file_title = file_title_match.group(1)
            else:
                file_title = os.path.basename(file_path)

            # Поиск описания файла
            file_description_match = re.search(r'/\*[\s\*]*Description: (.+?)\*/', file_content)
            if file_description_match:
                file_description = file_description_match.group(1)
            else:
                file_description = "No description available."

            # Поиск раздела "References"
            references_match = re.search(r'/\*[\s\*]*#include(.+?)\*/', file_content)
            if references_match:
                references = references_match.group(1)
            else:
                references = "No references available."

            # Поиск раздела "Read data from"
            read_data_match = re.search(r'/\*[\s\*]*@Param(.+?)\*/', file_content)
            if read_data_match:
                read_data = read_data_match.group(1)
            else:
                read_data = "No data param information available."

            # Генерация HTML-файла с информацией о файле
            output_filename = os.path.join(self.output_dir, os.path.splitext(os.path.basename(file_path))[0] + '.html')
            with open(output_filename, 'w') as output_file:
                output_file.write('<!DOCTYPE html>\n<html>\n<head>\n')
                output_file.write('<title>{}</title>\n</head>\n<body>\n'.format(file_title))
                output_file.write('<h1>{}</h1>\n'.format(file_title))
                output_file.write(
                    '<p class="source_note">Built from file \'{}\'</p>\n'.format(os.path.basename(file_path)))
                output_file.write('<p class="file_description">{}</p>\n'.format(file_description))
                output_file.write('<p class="references">References: {}</p>\n'.format(references))
                output_file.write('<p class="read_data">Read data from: {}</p>\n'.format(read_data))
                output_file.write('</body>\n</html>\n')

                print("Documentation generated for", file_path, "at", output_filename)


def main():
    """
    Точка входа в программу. Анализирует аргументы командной строки и запускает генерацию документации.
    """
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description='Generate human-readable documentation from source code.')
    parser.add_argument('--source', help='Source code directory', required=True)
    parser.add_argument('--output', help='Output directory', required=True)
    parser.add_argument('--filter', help='Regular expression filter to be applied on files listing')
    parser.add_argument('--profile', help='Select a profile of regular expressions')
    parser.add_argument('--show-help', action='store_true', help='Show this help message and exit')
    args = parser.parse_args()

    # Если указан аргумент --show-help, выводим справку и завершаем выполнение программы
    if args.show_help:
        parser.print_help()
        return

    # Создаем экземпляр DocumentationGenerator с переданными аргументами
    doc_gen = DocumentationGenerator(args.source, args.output, args.filter, args.profile)

    # Генерируем документацию
    doc_gen.generate_documentation()


if __name__ == "__main__":
    main()
