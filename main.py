"""Бекапер с помощью 7z.

Способ использования:
1. Создать файл config.json (используя config_example.json как пример).
2. Заполнить в нём нужные поля.
3. Запустить main.py

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


def create_backup(backup: Backup, seven_zip_path: str, password: str):
    """
    Запускает 7zip для создания архива с содержимым, указанным в объекте backup.
    """
    command = list(filter(None, [
        seven_zip_path,
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
    if not os.path.exists(CONFIG_FILENAME):
        print(f'{CONFIG_FILENAME} not found, read documentation on how to create one.')
        return

    with open(CONFIG_FILENAME, 'r', encoding='utf-8') as i:
        try:
            config_data = json.loads(i.read())
        except ValueError as e:
            print(f'Bad JSON in {CONFIG_FILENAME}: \n {str(e)}')
            return

    password = config_data.get('password')
    seven_zip_path = config_data.get('7z_path')

    if not password:
        print('Empty password is not allowed.')
        return

    if not seven_zip_path:
        print('Empty 7z_path is not allowed.')
        return

    if not os.path.exists(seven_zip_path):
        print('7z.exe not found, check your 7z_path variable.')
        return
    
    backup_entries = config_data.get('backup_entries')
    backup_objects = [Backup(**data) for data in backup_entries]

    selected_backups = ConsoleSelect(backup_objects, name_key='name').get_selected()
    if not selected_backups:
        print('Nothing selected')
        return

    for backup in selected_backups:
        print(f"Making a backup of '{backup.name}'...")

        if backup.some_sources_missing():
            return

        result = create_backup(backup, seven_zip_path, password)
        print(result.stdout.decode('utf-8'))
        if result.returncode:
            print('ERROR')
            print('Return code:', result.returncode)
            print(result.stderr.decode('utf-8'))
            return
    print('Completed.')


if __name__ == "__main__":
    main()
    input('Press any key to exit.')
