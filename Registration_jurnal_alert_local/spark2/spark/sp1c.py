from abc import ABC, abstractmethod
import re
from datetime import datetime
import os 
from  pathlib import Path

class Jurnal(ABC): 
    def __init__(self) -> None:
        pass

class DataBlockIterator:
    '''Итератор принимает путь журнала регистрации, возвращает блоки сообщений'''
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = None
        self.pattern = re.compile(r'^},\n', re.MULTILINE)
        self.blocks = []
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if not self.blocks:
            if not self.file:
                self.file = open(self.file_path, 'r', encoding='utf-8')
                data = self.file.read()
                self.blocks = self.pattern.split(data)
                self.blocks = [block for block in self.blocks if block.strip() and block.strip().startswith('{')]
            if not self.blocks:
                self.file.close()
                raise StopIteration
        block = self.blocks.pop(-1)
        self.index += 1
        return block

    def __del__(self):
        if self.file:
            self.file.close()

class JournalEntry:
    '''Блок сообщений журнала регистрации 1С'''
    def __init__(self, timestamp = None, event_type = None, session_id = None, message_type=None, message_id=None, message_code=None, message=None, details=None):
        self.timestamp = timestamp
        self.event_type = event_type
    
        # self.session_id = session_id
        self.message_type = message_type
        # self.message_id = message_id
        # self.message_code = message_code
        self.message = message
        # self.details = details

    # def __str__(self):
    #     return f"{self.timestamp} {self.event_type} {self.session_id} {self.message_type} {self.message_id} {self.message_code} {self.message} {self.details}"

class JournalEntryFactory: 
    '''Фарика по созданию блока сообщений '''
    # Время сообщения 
    @staticmethod
    def get_timestamp(row): 
        regx = re.compile(r'\d{14}')
        try:
            return datetime.strptime(regx.findall(row)[0], '%Y%m%d%H%M%S')
        except: 
            return None
    
    # Тип сообщения   
    @staticmethod 
    def get_event_type(row): 
        regx = re.compile(r'\d{14},([a-zA-Z])')
        try: 
            return regx.findall(row)[0]
        except: 
            return None

    # Информация или ошибка в сообщении?  
    @staticmethod 
    def get_error_info_type(block): 
        regx = re.compile(r'([EI]),"(.*?)",[0-9]', re.DOTALL)
        try:
            return regx.findall(block)[0]
        except:
            return None, None
    
    def create_JournalEntry(self, block: str) -> JournalEntry: 
        """Метод создаёт объекты класса блока сообщений из строкового представления"""
        rows = block.split('\n')
        timestamp = self.get_timestamp(rows[0])
        event_type = self.get_event_type(rows[0])
        message_type, message = self.get_error_info_type(block)
        return JournalEntry(timestamp=timestamp, 
                            event_type=event_type, 
                            message_type=message_type, 
                            message= message)
    
# Журнал регистрации 1С
class RegistrationJurnal1C(Jurnal):
    
    def __init__(self, entry: os.DirEntry) -> None:
        self.date = datetime.fromtimestamp(entry.stat().st_mtime)
        self.path = Path(entry.path)
        self.blocks = DataBlockIterator(self.path) # Итератор выдаёт блоки сообщений Журнала регистрации
        self.factory = JournalEntryFactory() # Имеет методы создания объектов сообщений, с которыми можно работать 
    
    def __iter__(self): 
        return self 

    def __next__(self): 
        block = next(self.blocks)
        return self.factory.create_JournalEntry(block)