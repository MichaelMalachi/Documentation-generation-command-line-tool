# FileProcessor.py

import re
import os

class FileProcessor:
    """
    Класс для обработки файлов и извлечения информации из них.
    """

    def __init__(self, filter_expr=None):
        self.filter_expr = filter_expr

    def get_files_to_process(self, source_dir):
        files_to_process = []
        filter_pattern = re.compile(self.filter_expr) if self.filter_expr else None
        for root, _, files in os.walk(source_dir):
            for file in files:
                if filter_pattern and not filter_pattern.match(file):
                    continue
                files_to_process.append(os.path.join(root, file))
        return files_to_process

    def process_file(self, file_path):
        with open(file_path, 'r') as f:
            file_content = f.read()

        file_title = self._extract_info(file_content, r'/\*[\s\*]*File: (.+?)\*/', os.path.basename(file_path))
        file_description = self._extract_info(file_content, r'/\*[\s\*]*Description: (.+?)\*/',
                                              "Native tcp connection header.")

        references = self._extract_references(file_content)

        read_data = self._extract_read_data(file_content)

        return {
            'file_title': file_title,
            'file_description': file_description,
            'references': references,
            'read_data': read_data
        }

    def _extract_info(self, content, pattern, default):
        match = re.search(pattern, content)
        return match.group(1) if match else default

    def _extract_references(self, content):
        references = []
        matches = re.findall(r'#include\s*<(.+?)>', content)
        for match in matches:
            reference = match.split('/')[-1].split('.')[0]
            references.append('References to' + reference.replace('_', ' '))
        return references

    def _extract_read_data(self, content):
        matches = re.findall(r'/\*[\s\*]*@Function\s*-\s*(.+?)\s*@(.*?)\*/', content, re.DOTALL)
        return '\n'.join(['{} - {}'.format(match[0], match[1].strip()) for match in matches])
