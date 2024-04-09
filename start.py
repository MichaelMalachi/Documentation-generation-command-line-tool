import argparse
from FileProcessor import FileProcessor
from DocumentationGenerator import DocumentationGenerator


def main():
    parser = argparse.ArgumentParser(description='Generate human-readable documentation from source code.')
    parser.add_argument('--source', help='Source code directory', required=True)
    parser.add_argument('--output', help='Output directory', required=True)
    parser.add_argument('--profile', help='Select a profile of regular expressions')
    parser.add_argument('--show-help', action='store_true', help='Show this help message and exit')
    args = parser.parse_args()

    if args.show_help:
        parser.print_help()
        return

    # Фильтр задается напрямую в коде
    filter_expr = r".*\.h"

    file_processor = FileProcessor(filter_expr)
    files_to_process = file_processor.get_files_to_process(args.source)
    files_info = [file_processor.process_file(file_path) for file_path in files_to_process]

    doc_gen = DocumentationGenerator(args.output)
    doc_gen.generate_documentation(files_info)


if __name__ == "__main__":
    main()

