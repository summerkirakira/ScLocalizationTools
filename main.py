import pathlib
from pathlib import Path
from typing import Dict


old_path: Path = pathlib.Path('./old/global.ini')
new_path: Path = pathlib.Path('./new/global.ini')
diff_path: Path = pathlib.Path('./diff.temp.txt')


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
                if value != old.data[key]:
                    print(f'{key}={old.data[key]} -> {value}')
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
                if value != old.data[key]:
                    with open("diff.temp.txt", "a") as f:
                        f.write(f'{key}={old.data[key]} -> {value}\n')
            else:
                with open("diff.temp.txt", "a") as f:
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

    def save(self):
        """
        Saves the data to the file
        :return:
        """
        with open("global.ini.new", "w") as f:
            for key, value in self.data.items():
                f.write(f'{key}={value}\n')


if __name__ == "__main__":
    if old_path.exists() and new_path.exists():
        pass
    else:
        print("请将旧的global.ini文件放在old文件夹下，新的global.ini文件放在new文件夹下")
        exit(1)
    old = LocalizationFile(old_path)
    new = LocalizationFile(new_path)
    while True:
        try:
            code = input("-----------\n1.查看差异\n2.保存差异\n3.加载差异\n4.保存文件\n5.退出\n请输入操作编号：")
            if code == "1":
                new.show_diff(old)
            elif code == "2":
                new.save_diff(old)
                print("差异已保存到diff.temp.txt文件中")
            elif code == "3":
                new.load_diff(diff_path)
            elif code == "4":
                new.save()
            elif code == "5":
                exit(0)
        except ValueError as e:
            print(e)
            continue
