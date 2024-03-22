from datetime import datetime, date
from pathlib import Path 
import re 
import os 


class Backup: 
    """Класс бэкапа. Определяет название, дату бэкапа по переданному пути"""        
    def __init__(self, path) -> None:
        self.path = Path(path)
        self.date = self.backup_date()
        self.name = self.path.name

    def backup_date(self): 
        return datetime.fromtimestamp(self.path.stat().st_atime)
    @property 
    def name(self): 
        return self._name 
    @name.setter 
    def name(self, path_name): 
        self._name = re.sub(f"{self.date.strftime('_%Y-%m-%d')}|\.dt", '', path_name)

class Backups_1C: 
    """Класс бэкапов 1С. Создаёт итерируемый объект с экземплярами класса Backup по пути к папке бэкапов"""
    def __init__(self, path) -> None:
        self.path = path
        self.backups = []
        
    @property
    def backups(self): 
        return self._backups 
    @backups.setter
    def backups(self, start): 
        self._backups = start
        with os.scandir(self.path) as entries: 
            for backup in entries: 
                self._backups.append(Backup(backup.path))
    
    def __iter__(self): 
        return iter(self.backups)
    
    # Создаёт словарь название бэкапа: список всех дат в которые он был успешно сделан 
    def get_dictionary_all(self): 
        dictionary_backup_dates = {}
        for backup in self.backups: 
            dictionary_backup_dates.setdefault(backup.name, []).append(backup.date)
        return dictionary_backup_dates
    
    # Создаёт словарь название бэкапа: список всех дат в текущем месяце в которые он был успешно сделан 
    def get_dictionary_this_month(self): 
        dictionary_this_month_dates = {} 
        _today = date.today()
        for backup in self.backups: 
            if _today.year == backup.date.year and _today.month == backup.date.month:
            # if _today.year == backup.date.year and _today.month - 1 == backup.date.month:
                dictionary_this_month_dates.setdefault(backup.name, []).append(backup.date)
        return dictionary_this_month_dates
