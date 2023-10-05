from pathlib import Path


def replace_string_in_file(old_file: Path, new_file: Path):
    """
    Replaces a string in a file
    :param old_file:
    :param new_file:
    :param old_string:
    :param new_string:
    :return:
    """
    with old_file.open('r', encoding='cp1256') as f:
        data = f.read()
    with new_file.open('w', encoding='cp1256') as f:
        f.write(data.replace("=[PH] ", ",P="))


def main():
    old_file = Path("old/global.ini")
    new_file = Path("old/global.new.ini")

    replace_string_in_file(old_file, new_file)


if __name__ == '__main__':
    main()