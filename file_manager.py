import os
import configparser
from datetime import datetime

class FileManager:
    def __init__(self, config_file="settings.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        working_directory = self.config.get("FileManager", "working_directory")
        if not os.path.exists(working_directory):
            print(f"Ошибка: рабочий каталог '{working_directory}' не существует.")
            exit(1)

        self.working_directory = working_directory
        self.current_directory = self.working_directory       
           
    def list_files(self):
        print("Файлы и директории в текущей директории:")
        print(f"{'Имя':<25} {'Размер':<10} {'Изменено'}")
        for item in os.listdir(self.current_directory):
            item_path = os.path.join(self.current_directory, item)
            size = os.path.getsize(item_path) if os.path.isfile(item_path) else "-"
            modified_time = datetime.fromtimestamp(os.path.getmtime(item_path)).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{item:<25} {size:<10} {modified_time}")
    
    def show_error(self, message):
        print(f"****** Ошибка: {message} ******")
        
    def is_valid_path(self, path):
        full_path = os.path.join(self.current_directory, path)
        return os.path.abspath(full_path).startswith(os.path.abspath(self.working_directory))
    
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

    def clear_screen(self):
        if os.name == 'nt':  # для Windows
            os.system('cls')
        else:  # для UNIX-систем
            os.system('clear')
            
    def get_relative_path(self, path):
        relative_path = os.path.relpath(path, self.working_directory)
        return relative_path if relative_path.startswith(os.sep) else os.sep + relative_path

    def run(self):
        while True:
            relative_current_directory = self.get_relative_path(self.current_directory)
            print(f"Текущая директория: {relative_current_directory}")
            print("-------------------------------")
            self.list_files()
            print("-------------------------------")
            self.show_help()
            command = input("Введите команду: ").split()

            if len(command) == 0:
                continue

            command_name = command[0]
            command_args = command[1:]
            
            self.clear_screen()
            print("===============================")

            if command_name == "exit":
                break
            else:
                self.show_error("Неверная команда. Пожалуйста, введите команду еще раз.")


if __name__ == "__main__":
    manager = FileManager()
    manager.run()
