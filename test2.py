import os
import re
import argparse
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class DocumentationGenerator:
    def __init__(self, source_dir, output_dir, filter_expr=None, profile=None):
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.filter_expr = filter_expr
        self.profile = profile

    def generate_documentation(self):
        files_to_process = []
        if self.filter_expr:
            filter_pattern = re.compile(self.filter_expr)
            for root, _, files in os.walk(self.source_dir):
                for file in files:
                    if filter_pattern.match(file):
                        files_to_process.append(os.path.join(root, file))
        else:
            for root, _, files in os.walk(self.source_dir):
                files_to_process.extend([os.path.join(root, file) for file in files])

        for file_path in files_to_process:
            with open(file_path, 'r') as f:
                file_content = f.read()

            file_title_match = re.search(r'/\*[\s\*]*File: (.+?)\*/', file_content)
            if file_title_match:
                file_title = file_title_match.group(1)
            else:
                file_title = os.path.basename(file_path)

            file_description_match = re.search(r'/\*[\s\*]*Description: (.+?)\*/', file_content)
            if file_description_match:
                file_description = file_description_match.group(1)
            else:
                file_description = "No description available."

            output_filename = os.path.join(self.output_dir, os.path.splitext(os.path.basename(file_path))[0] + '.html')
            with open(output_filename, 'w') as output_file:
                output_file.write('<!DOCTYPE html>\n<html>\n<head>\n')
                output_file.write('<title>{}</title>\n</head>\n<body>\n'.format(file_title))
                output_file.write('<h1>{}</h1>\n'.format(file_title))
                output_file.write(
                    '<p class="source_note">Built from file \'{}\'</p>\n'.format(os.path.basename(file_path)))
                output_file.write('<p class="file_description">{}</p>\n'.format(file_description))
                output_file.write('</body>\n</html>\n')

                print("Documentation generated for", file_path, "at", output_filename)


def generate_docs():
    source_dir = source_dir_entry.get()
    output_dir = output_dir_entry.get()
    filter_expr = filter_entry.get()
    profile = profile_entry.get()

    if not source_dir or not output_dir:
        messagebox.showerror("Error", "Source directory and output directory are required.")
        return

    doc_gen = DocumentationGenerator(source_dir, output_dir, filter_expr, profile)
    doc_gen.generate_documentation()
    messagebox.showinfo("Success", "Documentation generated successfully.")


def browse_source_dir():
    source_dir = filedialog.askdirectory()
    if source_dir:
        source_dir_entry.delete(0, tk.END)
        source_dir_entry.insert(0, source_dir)


def browse_output_dir():
    output_dir = filedialog.askdirectory()
    if output_dir:
        output_dir_entry.delete(0, tk.END)
        output_dir_entry.insert(0, output_dir)


# Создаем графический интерфейс
root = tk.Tk()
root.title("Documentation Generator")

# Поля для ввода
tk.Label(root, text="Source Directory:").grid(row=0, column=0)
source_dir_entry = tk.Entry(root, width=50)
source_dir_entry.grid(row=0, column=1)
tk.Button(root, text="Browse", command=browse_source_dir).grid(row=0, column=2)

tk.Label(root, text="Output Directory:").grid(row=1, column=0)
output_dir_entry = tk.Entry(root, width=50)
output_dir_entry.grid(row=1, column=1)
tk.Button(root, text="Browse", command=browse_output_dir).grid(row=1, column=2)

tk.Label(root, text="Filter Expression:").grid(row=2, column=0)
filter_entry = tk.Entry(root, width=50)
filter_entry.grid(row=2, column=1)

tk.Label(root, text="Profile:").grid(row=3, column=0)
profile_entry = tk.Entry(root, width=50)
profile_entry.grid(row=3, column=1)

# Кнопка для запуска генерации документации
tk.Button(root, text="Generate Documentation", command=generate_docs).grid(row=4, column=1)

root.mainloop()
