"""Бекапер с помощью 7z.

Способ использования:
1. Указать путь к 7z.exe в SEVEN_ZIP_PATH
2. Создать файл config.json (используя config_example.json как пример).
3. Заполнить в нём поля "password" и "backup_entries".
4. Запустить main.py

Требования:
Python 3.10
Установленный 7zip.
"""

import os
import json
import subprocess

from console_selector import ConsoleSelect
from backup_logic import Backup

CONFIG_FILENAME = 'config.json'
SEVEN_ZIP_PATH = r'c:\Program Files\7-Zip\7z.exe'


def create_backup(backup: Backup, password: str):
    """
    Запускает 7zip для создания архива с содержимым, указанным в объекте backup.
    """
    command = list(filter(None, [
        SEVEN_ZIP_PATH,
        'a',
        backup.target_with_date,
        *backup.sources,
        '-t7z',
        '-mx=9',
        '-bb3',
        backup.hide_contents_flag,
        *backup.excluded_files,
        f'-p{password}',
    ]))
    print(command)
    result = subprocess.run(command, capture_output=True)
    return result


def main() -> None:
    """
    Показывает все доступные пункты и делает бекап выбранных.
    """
    if not os.path.exists(SEVEN_ZIP_PATH):
        print('7z.exe not found, check your SEVEN_ZIP_PATH path.')
        return

    if not os.path.exists(CONFIG_FILENAME):
        print(f'{CONFIG_FILENAME} not found, read documentation on how to create one.')
        return

    with open(CONFIG_FILENAME, 'r') as i:
        try:
            config_data = json.loads(i.read())
        except ValueError as e:
            print(f'Bad JSON in {CONFIG_FILENAME}: \n {str(e)}')
            return
    password = config_data.get('password')

    if not password:
        print('Empty password is not allowed.')
        return

    
    backup_entries = config_data.get('backup_entries')
    backup_objects = [Backup(**data) for data in backup_entries]

    selected_backups = ConsoleSelect(backup_objects, name_key='name').get_selected()
    if not selected_backups:
        print('Nothing selected')
        return
    for backup in selected_backups:
        print(f"Making a backup of '{backup.name}'...")
        result = create_backup(backup, password)
        print(result.stdout.decode('utf-8'))
        if result.returncode:
            print('ERROR')
            print('Return code:', result.returncode)
            print(result.stderr.decode('utf-8'))
            return
    input('Completed.')


if __name__ == "__main__":
    main()
