"""
Класс, осуществляющий хранение данных, необходимых для создания бекапа.
"""

import os
import datetime


class Backup():
    def __init__(self, name: str, sources, target: str, hide_contents: bool=False, exclude=None) -> None:
        self.name = name
        self.sources = sources
        self.target = target
        self.hide_contents = hide_contents
        self.exclude = exclude

    @property
    def excluded_files(self) -> str:
        if self.exclude:
            return [f'-xr!{e}' for e in self.exclude]
        return ''

    @property
    def hide_contents_flag(self) -> str:
        if self.hide_contents:
            return '-mhe=on'
        return '-mhe=off'

    @property
    def target_with_date(self) -> str:
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d_%H%M")
        name, ext = os.path.splitext(self.target)
        new_path = f'{name}_{date}{ext}'
        return new_path

    def some_sources_missing(self):
        missing = False
        for source in self.sources:
            if not os.path.exists(source):
                missing = True
                print(f'ERROR: Path "{source}" does not exist.')
        return missing

    def __str__(self) -> str:
        return self.name
