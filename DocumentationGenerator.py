
import os


class DocumentationGenerator:
    """
    Класс для генерации документации на основе информации о файлах.
    """

    def __init__(self, output_dir):
        self.output_dir = output_dir

    def generate_documentation(self, files_info):
        for file_info in files_info:
            output_filename = os.path.join(self.output_dir, file_info['file_title'] + '.html')
            with open(output_filename, 'w') as output_file:
                self._write_html_header(output_file, file_info['file_title'])
                self._write_file_content(output_file, file_info)
                self._write_references(output_file, file_info['references'])
                self._write_read_data(output_file, file_info['read_data'])
            print("Documentation generated for", file_info['file_title'], "at", output_filename)

    def _write_html_header(self, output_file, title):
        output_file.write('<!DOCTYPE html>\n<html>\n<head>\n')
        output_file.write('<title>{}</title>\n</head>\n<body>\n'.format(title))
        output_file.write('<h1>{}</h1>\n'.format(title))

    def _write_file_content(self, output_file, file_info):
        output_file.write('<p class="source_note">Built from file \'{}\'</p>\n'.format(file_info['file_title']))
        output_file.write('<p class="file_description">{}</p>\n'.format(file_info['file_description']))

    def _write_references(self, output_file, references):
        if references:
            output_file.write('<p class="references">References:</p>\n<ul>\n')
            for reference in references:
                output_file.write('<li>{}</li>\n'.format(reference))
            output_file.write('</ul>\n')

    def _write_read_data(self, output_file, read_data):
        output_file.write('<p class="read_data">Read data from:</p>\n<ul>\n')
        for line in read_data.split('\n'):
            output_file.write('<li>{}</li>\n'.format(line.strip()))
        output_file.write('</ul>\n')
