from abc import ABC, abstractmethod
import time 
import os
import sys
import argparse
import configparser
import firebirdsql
import collections
import inspect
from pathlib import Path
import spark2.sendscr as sendalarm
import spark2.spsetting as settings 
import spark2.cfgparam as cfparams
import spark2.spmessages as messages

from spsetting import ALL_LOGS_RARELY_USED
# Абстракция отправки сообщений
class Sendler(ABC):
    def __init__(self, db_name, priority, send_file, message_status, message_title, logger) -> None:
        self.db_name = db_name
        self.priority = priority
        self.send_file = send_file
        self.message_status = message_status
        self.message_title = message_title
        self.logger = logger
    
    @abstractmethod
    def send_message(self): 
        pass
# Абстракция логирования
class Logger(ABC): 
    def __init__(self,
                 path_log=settings.ALL_LOGS_RARELY_USED, 
                 lbackup_count=5, 
                 log_name: str = 'empty.log',
                 logger_name: str = 'empty') -> None:
        self.path_log = Path(path_log) 
        self.log_name: str = log_name
        self.lbackup_count = lbackup_count
        self.logger_name: str = logger_name
        self.logger, self.handler = cfparams.get_logger(self.logger_name,self.path_log,self.log_name,'win',False, self.lbackup_count) #Для Zabbix
        
    @abstractmethod
    def info(self, body):
        pass

    @abstractmethod
    def error(self, error): 
        pass 

    def handler_close(self): 
        if self.handler:
            self.handler.close()

# Абстракция конфига 
class Config(ABC): 
    def __init__(self, path_config, file_config, logger: Logger, name_config = '') -> None:
        self.logger = logger
        self.name_config = name_config
        self.path = Path(path_config, file_config)
        self.config = configparser.ConfigParser()
        self.config.read(os.path.normpath(self.path), encoding='utf-8')
        
    @property
    def path(self): 
        return self._path
    @path.setter
    def path(self, path_config_full: Path): 
        if not os.path.exists(path_config_full): 
            self.logger.error((messages.MSG_CFG_NOT_FOUND_INFO).format(self.name_config, path_config_full))
            sys.exit(0)
        else: 
            self._path = path_config_full
            self.logger.info((messages.MSG_CFG_FILE).format(self.name_config, path_config_full))
            
    def get(self, section, option, *, raw = False, vars = None): 
        self.__dict__[option] = self.config.get(section, option, raw = raw, vars = vars)
        return self.__dict__[option]
    
class DataBaseConnector(ABC): 
    def __init__(self, host, database, user, password, charset, timeout, logger) -> None:
        self.host = host
        self.database: str = database 
        self.user = user 
        self.password = password
        self.charset = charset
        self.timeout = timeout
        self.logger = logger
    
    @abstractmethod
    def create_connection(self): 
        pass



# Главный класс, сожержит всю информацию по скрипту
class Script:
    def __init__(self, app_name='Empty', app_description='',
                 app_id='0', db_name='test-otchet') -> None:
    
        # Характеристики для формирования описания логов и др. 
        self.start_program_time = time.perf_counter() # "Запуск" работы таймера выполнения программы 
        self.app_name = app_name
        self.app_description = app_description
        self.app_id = app_id
        self.__connections = []
        stack = inspect.stack()
        # Второй элемент стека (индекс 1) - это вызывающий код
        calling_frame = stack[1]
        # Получаем путь к файлу, который вызвал импорт
        calling_file_path = calling_frame.filename
        self.dirname = os.path.dirname(calling_file_path)
        self.db_name = db_name, #  база данных
        # Флаг работы скрипта 
        self.enabled = True
        # Параметры которые устанавливаются при инициализации классов с аргументом script
        self.logger: Logger = None
        self.all_logger: Logger = None
        self.sendler: Sendler = None
        self.config_glb: Config = None
        self.config_loc: Config = None
        # self.connections: list = None
    
    def set_logger(self, logger: Logger): 
        self.logger: Logger = logger

    def set_all_logs(self, logger: Logger): 
        self.all_logger: Logger = logger

    def set_sendler(self, sendler: Sendler):
        self.sendler: Sendler = sendler
    
    def set_db_name(self, db_name: str):
        self.db_name = db_name
    
    # Закрытие подключений к базам данных
    def close_connections(self): 
        for con in self.connections: 
            try: 
                con.close()
            except Exception as info: 
                self.logger.error(f'Ошибка закрытия подключения к БД: {info}')

    def close(self): 
        self.close_connections()
        time_program_execution = time.perf_counter() - self.start_program_time # "Отключение" таймера выполнения программы
        self.logger.info((messages.MSG_TIME_PROGRAM_EXECUTION).format(time_program_execution))
        self.logger.info(messages.MSG_LOG_OVER)
        try:
            self.logger.handler_close()
        except: 
            pass 
        try: 
            self.all_logger.handler_close()
        except: 
            pass
        

    @property
    def db_name(self):
        return self._db_name 
    @db_name.setter
    def db_name(self, db): 
        if isinstance(db, tuple): 
            self._db_name = db[0]
        else: 
            self._db_name = db

    @property 
    def enabled(self): 
        return self._enabled 
    @enabled.setter
    def enabled(self, value: int): 
        self._enabled = bool(value)
        if not self._enabled: 
            self.logger.info(messages.MSG_ENABLED_OFF)
            sys.exit(0)

    @property 
    def connections(self): 
        return self.__connections
    @connections.setter
    def connections(self, connection): 
        self.__connections.append(connection)

        
# Класс базового логирования 
class Logger_main(Logger): 
    def __init__(self, script: Script, 
                 path_log=settings.ALL_LOGS_RARELY_USED, 
                 lbackup_count=5, 
                 log_name='', 
                 logger_name='empty') -> None:
        
        self.id = script.app_id
        self.description = script.app_description
        self.path_log = Path(path_log) 
        self.lbackup_count = lbackup_count
        self.log_name = log_name
        self.logger_name = script.app_name
        super().__init__(path_log, lbackup_count, log_name, logger_name)
        script.logger = self

    @property
    def log_name(self): 
        return self._log_name
    @log_name.setter
    def log_name(self, name = None):
        if name: 
            self._log_name = name
        if self.id and self.description and isinstance(self.id, str) and isinstance(self.description, str):
            log_name = (settings.NAME_LOG_FILE).format(self.id, self.description)
            self._log_name = (settings.FORMAT_LOG_FILE).format(log_name)  
        else: 
            raise AttributeError('ID и Название должны быть string')
        
    def info(self, body): 
        return self.logger.info(body)
    
    def error(self, error): 
        return self.logger.error(error)
    

class AllLogs(Logger):
    def __init__(self, 
                 script: Script,
                 path_log=settings.ALL_LOGS_RARELY_USED, 
                 lbackup_count=5, 
                 log_name='all_empty.log', 
                 logger_name='all_logs') -> None:
        super().__init__(path_log, lbackup_count, log_name, logger_name)
        self.name_script = script.app_description
        self.id = script.app_id
        script.all_logger = self
    def info(self, body):
        self.logger.info(f'{self.id}.{self.name_script}: {body}')

    def error(self, error):
        self.logger.error(f'{self.id}.{self.name_script}: {error}')
        
# Класс отправки ошибок в телеграмм
class Telegram_sender_error(Sendler): 
    
    def __init__(self,
                script: Script,
                db_name='test-othet', 
                priority='Высокая', 
                send_file='', 
                message_status='ОШИБКА!', 
                message_title='Краткое описание программы', 
                test = True, 
                use_main_chanel = True,
                ) -> None:   
        self.test = test
        self.use_main_chanel = use_main_chanel
        self.logger = script.logger
        super().__init__(db_name, priority, send_file, message_status, message_title, self.logger)
        script.sendler = self
    def send(self, message_body): 
        sendalarm.get_telegram_main(self.db_name.upper(), self.priority, message_body, self.send_file, self.message_status, self.message_title)
    
    def send_message(self, message):
        if self.logger: 
            try:
                if self.test: 
                    self.send_file = settings.TELEGRAM_TEST_CHANEL_FILE
                    return self.send(message)
                else:
                    if self.use_main_chanel: 
                        self.send_file = settings.TELEGRAM_MAIN_CHANEL_FILE
                        return self.send(message)
                    else: 
                        return self.send(message)
            except Exception as info: 
                self.logger.info(f'Проблемы с отправкой в телеграмм: {info}') 
        else: 
            raise AttributeError('Атрибут logger не найден')

class ConfigGlobal(Config): 
    def __init__(self, 
                 script: Script,
                 db_name: str,  
                 path_config=settings.GLOBAL_CFG_DIR,
                 file_config=settings.GLOBAL_FB_CFG, 
                 name_config='глобальной') -> None:
        super().__init__(path_config, file_config, script.logger, name_config)
        try:
            self.db_name = db_name
            self.id_db = self.config.get(self.db_name, settings.OPT_IDDB)
            self.ip_address = self.config.get(self.db_name, settings.OPT_IPADDRESS)
            self.descript = self.config.get(self.db_name, settings.OPT_DESCRIPTION)
            self.use_user = self.config.get(self.db_name, settings.OPT_USER)
            self.use_pass = self.config.get(self.db_name, settings.OPT_PASS)
            self.glb_enabled = self.config.get(self.db_name, settings.OPT_ENABLED)
            self.con_timeout = self.config.get(self.db_name, settings.OPT_TIMEOUT)
            
        except Exception as info: 
            self.logger.error(messages.MSG_GLBCFG_IO_ERROR)
            self.logger.error(info)
            script.all_logger.error('ОШИБКА!')
            script.sendler.send_message('Ошибка глобальной конфигурации!')
            sys.exit(0)

class ConfigGlobal_main(ConfigGlobal):
    def __init__(self, script: Script, path_config=settings.GLOBAL_CFG_DIR, file_config=settings.GLOBAL_FB_CFG, name_config='глобальной') -> None:
        super().__init__(script, script.db_name, path_config, file_config, name_config)
        script.config_glb = self

class ConfigLocal_main(Config): 
    def __init__(self, 
                 script: Script,
                 file_config=settings.CFGFILE, 
                 name_config='локальной') -> None:
        super().__init__(script.dirname, file_config, script.logger, name_config)  
        try: 
            self.enabled = self.config.get(settings.OPT_MAIN_SEC, settings.OPT_ENABLED)
        except Exception as info: 
            self.logger.error(messages.MSG_LOCCFG_IO_ERROR)
            self.logger.error(info)
            if script.all_logger: script.all_logger.error('ОШИБКА!')
            script.sendler.send_message('Ошибка локальной конфигурации!')
            sys.exit(0)      
        script.config_loc = self
        script.enabled = int(self.enabled)

class MainConnector(DataBaseConnector): 
    def __init__(self, script: Script,  config: ConfigGlobal) -> None:
        super().__init__(host=config.ip_address,
                         database=config.db_name, 
                         user=config.use_user, 
                         password=config.use_pass, 
                         charset=settings.FIREBIRD_CHARSET, 
                         timeout=config.con_timeout, 
                         logger=script.logger)
        self.script = script
    
    def create_connection(self):
        pass

class FireBirdConnector: 
    def __init__(self, script: Script) -> None:
        self.script = script

    def create_connection(self, db_name: str):
        self.config = ConfigGlobal(script=self.script, db_name=db_name, name_config=f'глобальной для {db_name}')
        try: 
            con =  firebirdsql.connect(host = self.config.ip_address, database = self.config.db_name, 
                                    user = self.config.use_user, password = self.config.use_pass, 
                                    charset = settings.FIREBIRD_CHARSET,
                                    timeout = self.config.con_timeout)
            self.script.connections = con
            self.script.logger.info((messages.MSG_BASE_CONNECTION).format(db_name))
            return con

        except Exception as info: 
            self.script.all_logger.error('ОШИБКА!')
            self.script.logger.error((messages.MSG_DBCONNECT_ERROR_INFO).format(db_name.upper(), info))
            self.script.sendler.send_message(f'Ошибка подключения к БД Firebird! {db_name.upper()}')
            sys.exit(0)

    



        
