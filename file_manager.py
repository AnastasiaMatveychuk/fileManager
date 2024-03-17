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
        for item in os.listdir(self.current_directory):
            item_path = os.path.join(self.current_directory, item)
            size = os.path.getsize(item_path) if os.path.isfile(item_path) else "-"
            modified_time = datetime.fromtimestamp(os.path.getmtime(item_path)).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{'Имя':<25} {'Размер':<10} {'Изменено'}")
            print(f"{item:<25} {size:<10} {modified_time}")
    
    def show_error(self, message):
        print(f"****** Ошибка: {message} ******")
        
    def is_valid_path(self, path):
        full_path = os.path.join(self.current_directory, path)
        return os.path.abspath(full_path).startswith(os.path.abspath(self.working_directory))

    def run(self):
        self.list_files()


if __name__ == "__main__":
    manager = FileManager()
    manager.run()
