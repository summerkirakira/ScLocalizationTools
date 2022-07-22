import pathlib
from pathlib import Path
from typing import Dict


root_path: Path = pathlib.Path('./')
working_in_progress_path: Path = root_path / 'working_in_progress'
history_path: Path = root_path / 'history files'
release_path: Path = pathlib.Path('./release')

if not release_path.exists():
    release_path.mkdir()


class LocalizationFile:
    def __init__(self, path: Path):
        """
        Initializes the class with the path to the file
        :param path:
        """
        self.path: Path = path
        if not self.path.exists():
            print(f'{self.path} does not exist')
            raise FileNotFoundError
        self.data: Dict[str, str] = {}
        self.read()

    def read(self):
        """
        Reads the file and stores the data in a dictionary
        :return:
        """
        with self.path.open('r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                self.data[key] = value

    def show_diff(self, old: 'LocalizationFile'):
        """
        Shows the differences between the old and new file
        :param old:
        :return:
        """
        for key, value in self.data.items():
            if key in old.data:
                # if value != old.data[key]:
                #     print(f'{key}={old.data[key]} -> {value}')
                pass
            else:
                print(f'+ {key}={value}')

    def save_diff(self, old: 'LocalizationFile'):
        """
        Saves the differences between the old and new file
        :param old:
        :return:
        """
        for key, value in self.data.items():
            if key in old.data:
                # if value != old.data[key]:
                #     with open("diff.temp.txt", "a") as f:
                #         f.write(f'{key}={old.data[key]} -> {value}\n')
                self.data[key] = old.data[key]
                pass
            else:
                with open("../diff.temp.txt", "a") as f:
                    f.write(f'+ {key}={value}\n')

    def load_diff(self, diff_path: Path):
        """
        Loads the differences from a file
        :param diff_path:
        :return:
        """
        with diff_path.open('r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('+ '):
                    line = line[2:]
                if not line or line.startswith('#'):
                    continue
                if '->' in line:
                    raise ValueError(f'{line} is not a valid line')
                key, value = line.split('=', 1)
                self.data[key] = value

    def save(self, file_path: Path):
        """
        Saves the data to the file
        :return:
        """
        with open(file_path.absolute(), "w+") as f:
            for key, value in self.data.items():
                f.write(f'{key}={value}\n')

    def save_to_xlsx(self, xlsx_path: Path):
        """
        Saves the data to an xlsx file
        :param xlsx_path:
        :return:
        """
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Global'
        for key, value in self.data.items():
            ws[key] = value
        wb.save(xlsx_path)


if __name__ == "__main__":
    to_version = '3_17_2PTU'
    for file in working_in_progress_path.iterdir():
        if file.suffix == '.txt':
            file_name = file.name
            localization_type = file_name.split(']')[0].split('[')[1]
            from_version = file_name.split(']')[1].split('to')[0].strip().replace('.', '_')
            to_version = file_name.split(']')[1].split('to')[1].strip().replace('.txt', '').replace('.', '_')
            old_file: Path = history_path / localization_type / f'global.{from_version}.ini'
            old_global: LocalizationFile = LocalizationFile(old_file)
            old_global.load_diff(file)
            old_global.save(release_path / f'[{localization_type}][{to_version.replace("_", ".")}]global.ini')
    en_file: Path = history_path / 'en' / f'global.{to_version}.ini'
    if en_file.exists():
        en_global: LocalizationFile = LocalizationFile(en_file)
        en_global.save(release_path / f'[en][{to_version.replace("_", ".")}]global.ini')
    print(to_version.replace("_", "."))

