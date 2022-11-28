from thefuzz import process
import pathlib
from pathlib import Path
from typing import Dict

english_path: Path = pathlib.Path('./history files/en/global.3_17_4PU.ini')
chinese_path: Path = pathlib.Path('./history files/zh-cn/global.3_17_4PU.ini')


class EnglishLocalizationFile:
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
        self.value_list: list[str] = []
        self.read()
    
    def read(self):
        """
        Reads the file and stores the data in a dictionary
        :return:
        """
        with self.path.open('r', encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                if len(value) < 10 or len(value) > 40:
                    continue
                self.data[value] = key
                self.value_list.append(value)
    
    def get_most_relative_patterns(self, word: str):
        results = process.extract(word, self.value_list, limit=5)
        result_keys = []
        for result in results:
            result_keys.append(self.data[result[0]])
        return result_keys, results

    def get_values(self, key_list: list[str]):
        results = []
        for key in key_list:
            if key in self.data:
                results.append(self.data[key])
        return results


class ChineseLocalizationFile:
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
        self.value_list: list[str] = []
        self.read()

    def read(self):
        """
        Reads the file and stores the data in a dictionary
        :return:
        """
        with self.path.open('r', encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                self.data[key] = value
                self.value_list.append(value)

    def get_most_relative_patterns(self, word: str):
        results = process.extract(word, self.value_list, limit=5)
        result_keys = []
        for result in results:
            result_keys.append(result[0])
        return result_keys

    def get_values(self, key_list: list[str], value_list: list[str]):
        results = []
        for index, key in enumerate(key_list):
            if key in self.data:
                results.append(self.data[key])
                print(f"{value_list[index]}: {self.data[key]}")
        return results


if __name__ == "__main__":
    english_global = EnglishLocalizationFile(english_path)
    chinese_global = ChineseLocalizationFile(chinese_path)
    while True:
        key = input("Please input key values:")
        searched_keys, searched_value = english_global.get_most_relative_patterns(key)
        chinese_global.get_values(searched_keys, searched_value)