import os
import configparser
from datetime import datetime
import shutil
import sys


class FileManager:
    # конструктор считывает файл конфигурации и инициализирует рабочую директорию
    def __init__(self, config_file="settings.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        working_directory = self.config.get("FileManager", "working_directory")
        if not os.path.exists(working_directory):
            print(f"Ошибка: рабочий каталог '{working_directory}' не существует.")
            exit(1)

        self.working_directory = working_directory
        self.current_directory = self.working_directory

    # функция отображает список файлов и директорий в текущей директории
    def list_files(self):
        print("Файлы и директории в текущей директории:")
        print(f"{'Имя':<25} {'Размер':<10} {'Изменено'}")
        for item in os.listdir(self.current_directory):
            item_path = os.path.join(self.current_directory, item)
            size = os.path.getsize(item_path) if os.path.isfile(item_path) else "-"
            modified_time = datetime.fromtimestamp(os.path.getmtime(item_path)).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{item:<25} {size:<10} {modified_time}")

    # функция выводит сообщение об ошибке
    def print_error(self, message):
        print(f" Ошибка: {message} ")

    # функция валидирует путь, проверяя, что он находится в пределах рабочей директории
    def validate_path(self, path):
        full_path = os.path.join(self.current_directory, path)
        return os.path.abspath(full_path).startswith(os.path.abspath(self.working_directory))

    # функция выводит список доступных команд
    def show_help(self):
        print("Доступные команды:")
        print(f"{'create_dir <directory_name>':40} - Создать директорию")
        print(f"{'delete_dir <directory_name>':40} - Удалить директорию")
        print(f"{'cd <directory_name>':40} - Перейти в директорию")
        print(f"{'create_file <file_name>':40} - Создать файл")
        print(f"{'write_to_file <file_name>':40} - Записать в файл")
        print(f"{'read_file <file_name>':40} - Прочитать файл")
        print(f"{'delete_file <file_name>':40} - Удалить файл")
        print(f"{'copy_file <source> <destination>':40} - Копировать файл")
        print(f"{'move_file <source> <destination>':40} - Переместить файл")
        print(f"{'rename_file <source> <new_name>':40} - Переименовать файл")
        print(f"{'exit':40} - Выйти")

    # функция очищает экран консоли
    def clear_screen(self):
        if os.name == 'nt':  # для Windows
            os.system('cls')
        else:  # для UNIX-систем
            os.system('clear')

    # функция возвращает относительный путь от рабочей директории до заданного пути
    def get_relative_path(self, path):
        relative_path = os.path.relpath(path, self.working_directory)
        return relative_path if relative_path.startswith(os.sep) else os.sep + relative_path

    # функция создает директорию
    def create_dir(self, directory_name):
        full_path = os.path.join(self.current_directory, directory_name)
        if not self.validate_path(directory_name):
            self.print_error("Файл находится не в рабочей папке.")
        elif os.path.exists(full_path):
            self.print_error("Директория уже существует.")
        else:
            os.mkdir(full_path)
            print("Директория успешно создана.")

    # функция удаляет директорию
    def delete_dir(self, directory_name):
        full_path = os.path.join(self.current_directory, directory_name)
        if not self.validate_path(directory_name):
            self.print_error("Файл находится не в рабочей папке.")
        elif not os.path.exists(full_path):
            self.print_error("Директория не существует.")
        elif not os.path.isdir(full_path):
            self.print_error("Указан не директория.")
        else:
            shutil.rmtree(full_path)
            print("Директория успешно удалена вместе с ее содержимым.")

    # функция переходит в другую директорию
    def cd(self, directory_name):
        full_path = os.path.join(self.current_directory, directory_name)
        if not self.validate_path(directory_name):
            self.print_error("Файл находится не в рабочей папке.")
        elif not os.path.exists(full_path):
            self.print_error("Директория не существует.")
        elif not os.path.isdir(full_path):
            self.print_error("Указана не директория.")
        else:
            self.current_directory = full_path

    # функция создает файл
    def create_file(self, file_name):
        full_path = os.path.join(self.current_directory, file_name)
        if not self.validate_path(file_name):
            self.print_error("Файл находится не в рабочей папке.")
        elif os.path.exists(full_path):
            self.print_error("Файл уже существует.")
        else:
            open(full_path, 'a', encoding='utf-8').close()
            print("Файл успешно создан.")

    # функция удаляет файл
    def delete_file(self, file_name):
        full_path = os.path.join(self.current_directory, file_name)
        if not self.validate_path(file_name):
            self.print_error("Файл находится не в рабочей папке.")
        elif not os.path.exists(full_path):
            self.print_error("Файл не существует.")
        elif os.path.isdir(full_path):
            self.print_error("Указан не файл.")
        else:
            os.remove(full_path)
            print("Файл удален.")

    # функция записывает данные в файл
    def write_to_file(self, file_name):
        full_path = os.path.join(self.current_directory, file_name)
        if not self.validate_path(file_name):
            self.print_error("Файл находится не в рабочей папке.")
        elif not os.path.exists(full_path):
            self.print_error("Файл не существует. Создайте файл перед записью.")
        elif os.path.isdir(full_path):
            self.print_error("Указан не файл.")
        else:
            print(
                "Введите текст для добавления в файл. Завершите ввод с помощью или Ctrl+Z (в Windows).")
            text = sys.stdin.read()
            with open(full_path, 'a', encoding='utf-8') as file:
                file.write(text)
            print("Текст добавлен в файл.")

    # функция читает данные из файла
    def read_file(self, file_name):
        full_path = os.path.join(self.current_directory, file_name)
        if not self.validate_path(file_name):
            self.print_error("Файл находится не в рабочей папке.")
        elif not os.path.exists(full_path):
            self.print_error("Файл не существует.")
        elif os.path.isdir(full_path):
            self.print_error("Не указан файл.")
        else:
            with open(full_path, 'r', encoding='utf-8') as file:
                content = file.read()
            print("Содержимое файла:")
            print(content)

    # функция копирует файл
    def copy_file(self, source_file_name, destination_file_name):
        source_full_path = os.path.join(self.current_directory, source_file_name)
        destination_full_path = os.path.join(self.current_directory, destination_file_name)

        if not self.validate_path(source_file_name):
            self.print_error("Файл находится не в рабочей папке.")
        elif not os.path.exists(source_full_path):
            self.print_error("Файл не существует.")
        elif os.path.isdir(source_full_path):
            self.print_error("Указан не файл.")
        elif not self.validate_path(destination_file_name):
            self.print_error("Файл находится не в рабочей папке.")
        elif os.path.exists(destination_full_path):
            self.print_error("Файл с таким именем уже существует.")
        else:
            shutil.copy(source_full_path, destination_full_path)
            print("Файл успешно скопирован.")

    # функция перемещает файл
    def move_file(self, source_file_name, destination_file_name):
        source_full_path = os.path.join(self.current_directory, source_file_name)
        destination_full_path = os.path.join(self.current_directory, destination_file_name)

        if not self.validate_path(source_file_name):
            self.print_error("Файл находится не в рабочей папке.")
        elif not os.path.exists(source_full_path):
            self.print_error("Файл не существует.")
        elif os.path.isdir(source_full_path):
            self.print_error("Указан не файл.")
        elif not self.validate_path(destination_file_name):
            self.print_error("Файл находится не в рабочей папке.")
        elif os.path.exists(destination_full_path):
            self.print_error("Файл с таким именем уже существует.")
        else:
            shutil.move(source_full_path, destination_full_path)
            print("Файл успешно перемещен.")

    # функция переименовывает файл
    def rename_file(self, source_file_name, new_file_name):
        source_full_path = os.path.join(self.current_directory, source_file_name)
        destination_full_path = os.path.join(self.current_directory, new_file_name)

        if not self.validate_path(source_file_name):
            self.print_error("Файл находится не в рабочей папке.")
        elif not os.path.exists(source_full_path):
            self.print_error("Файл не существует.")
        elif os.path.isdir(source_full_path):
            self.print_error("Указан не файл.")
        elif not self.validate_path(new_file_name):
            self.print_error("Файл находится не в рабочей папке.")
        elif os.path.exists(destination_full_path):
            self.print_error("Файл с таким именем уже существует.")
        else:
            os.rename(source_full_path, destination_full_path)
            print("Файл успешно переименован.")

    # основной цикл программы. Принимает команды, вызывает соответствующие методы и обрабатывает ошибки
    def run(self):
        while True:
            relative_current_directory = self.get_relative_path(self.current_directory)
            print(f"Текущая директория: {relative_current_directory}")
            print("")
            self.list_files()
            print("")
            self.show_help()
            command = input("Введите команду: ").split()

            if len(command) == 0:
                continue

            command_name = command[0]
            command_args = command[1:]

            self.clear_screen()

            if command_name == "exit":
                break

            getattr(self, command_name, self.print_error("Неверная команда. Пожалуйста, введите команду еще раз."))(
                *command_args)


if __name__ == "__main__":
    manager = FileManager()
    manager.run()
