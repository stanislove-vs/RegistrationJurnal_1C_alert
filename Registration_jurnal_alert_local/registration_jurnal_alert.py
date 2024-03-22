#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------------------
# version: 1.0.
# Date: 12.03.2024
# Mod: 13.03.2024
# Description: Отправка сообщений из мониторинга журнала 1С
# Author: Modification Соколов С.В.
#-----------------------------------------------------------------------------------------------------------------------------------

import os
import sys
import argparse
from pathlib import Path
from datetime import date
import time
import re
from datetime import datetime
import sqlite3
# Импорт пользовательских библиотек  
import spark2.cfgparam as cfparams
import spark2.spsetting as settings
import spark2.spmessages as messages
import spark2.sendscr as sendalarm
import spark2.spscript as spscript 
from spark2.spscript import ( Script, Logger_main, 
                             AllLogs, Telegram_sender_error, ConfigLocal_main, 
                             FireBirdConnector)
import spark2.sp1c as sp1c

if __name__ == '__main__':	

    # Создание строки параметров
    argparser = argparse.ArgumentParser(description= 'Test')
    argparser.add_argument(settings.ARG_DB_NAME, help='Host')
    argnamespace = argparser.parse_args() # Чтение строки параметров 

    # --------------------------------------------------------------------------
    # Базовый класс скрипта 
    script = Script(app_name = 'registration_jurnal_alert', 
                    app_description = f'Уведомления журнала регистрации по 1С {argnamespace.db_name}', 
                    app_id = '1', 
                    db_name = argnamespace.db_name)
    
    # Базовое логирование 
    logger = Logger_main(script=script, 
                        #  path_log=settings.ALL_LOGS_MONITORING)
                        path_log=str(Path(os.path.dirname(__file__))))
    # Настройка оповещения 
    telegram = Telegram_sender_error(script=script,
                                    db_name=argnamespace.db_name, 
                                    test=False, 
                                    message_title='Ошибка журнала регистрации',
                                    use_main_chanel=False, 
                                    send_file=str(Path(script.dirname, 'telegram_1c', 'dist', 'telegram_message.exe')))
    
    # Старт работы
    logger.info(messages.MSG_BEGIN_SEPARATOR)
    logger.info(messages.MSG_LOG_BEGIN)
    
    
    
    # ---------------------------------------------------------------------------
    
    #                              РАБОЧИЙ БЛОК                         #
    #--------------------------------------------------------------------  
    try:
        class Config(ConfigLocal_main): 
            date_patterns = ['%Y%m%d%H%M%S', '%Y%m%d', '%Y%m%d000000']
            def __init__(self, script: Script, file_config=settings.CFGFILE, name_config='локальной') -> None:
                super().__init__(script, file_config, name_config)
                # Путь к журналам регистрации
                self.path_jurnal = Path(self.config.get(settings.OPT_MAIN_SEC, 'path_jurnal'))
                # Расширение файлов журнала
                self.jurnal_extension = self.config.get(settings.OPT_MAIN_SEC, 'jurnal_extension')
                # Дата модификации последнего файла 
                self.last_jurnal_datetime = self.config.get(settings.OPT_MAIN_SEC, 'last_jurnal_datetime')
                # Дата последнего сообщения 
                self.last_block_jurnal_datetime = self.config.get(settings.OPT_MAIN_SEC, 'last_block_jurnal_datetime')
                # Связующий класс
                self.script: Script = script
                # База данных алёртов 
                self.alerts_db: str = self.config.get(settings.OPT_MAIN_SEC, 'alerts_db')

            # Формирует дату модификации последнего файла в datetime 
            @property
            def last_jurnal_datetime(self) -> datetime: 
                return self._last_jurnal_datetime
            @last_jurnal_datetime.setter
            def last_jurnal_datetime(self, date: str): 
                self._last_jurnal_datetime = None
                for pattern_date in self.date_patterns: 
                    try: 
                        self._last_jurnal_datetime = datetime.strptime(date, pattern_date)
                        break 
                    except: 
                        pass
                if self._last_jurnal_datetime is None: 
                    try: 
                        self._last_jurnal_datetime = datetime.fromtimestamp(date)
                    except Exception as info: 
                        script.logger.error(f'Не удалось найти дату последнего считанного файла: {info}')

            # Формирует дату последнего сообщения в datetime 
            @property 
            def last_block_jurnal_datetime(self): 
                return self._last_block_jurnal_datetime
            @last_block_jurnal_datetime.setter
            def last_block_jurnal_datetime(self, date: str): 
                self._last_block_jurnal_datetime = None
                try:
                    for pattern_date in self.date_patterns: 
                        try: 
                            self._last_block_jurnal_datetime = datetime.strptime(date, pattern_date)
                            break 
                        except: 
                            pass
                except Exception as info: 
                    script.logger.error(f'Не удалось найти дату последнего считанного собщения: {info}')
            
            # Метод установки нового параметра в конфигурацию 
            def set_setting(self, section,setting,value):
                cfparams.set_setting(self.path, section=section, setting=setting, value=value)



        # Подключение локальной конфигурации 
        config_loc = Config(script=script)
        # Флаг для фиксации самого позднего файла и сообщения
        flag_first = True
        conn = sqlite3.connect(config_loc.alerts_db)
        cur = conn.cursor()

        with os.scandir(config_loc.path_jurnal) as entries:
            # Используем сортировку в попрядке убывания для чтения файлов Журнала регистрации 
            sorted_entries = sorted(entries, key=lambda entry: entry.stat().st_mtime, reverse=True)
            for entry in sorted_entries:
                if entry.is_file(): 
                    # Фиксируем название, расширение и дату изменения файла
                    filename, file_extension = os.path.splitext(entry.name)
                    entry_datetime = datetime.fromtimestamp(entry.stat().st_mtime)
                    # Продолжаем работу только с файлами, у которых нужное расширение (Согласно указанному в конфигурации)
                    # При условии что их дата модификации выше последней даты 
                    if file_extension == config_loc.jurnal_extension and entry_datetime > config_loc.last_jurnal_datetime: 
                        print(filename)
                        try:
                            # Формируем объект журнала регистрации 
                            jurnal = sp1c.RegistrationJurnal1C(entry=entry)
                            # Обрабатывае блоки сообщений Журнала в случае если их дата больше предыдущего отправленного 
                            jurnal_next_block_massage = next(jurnal)
                            while jurnal_next_block_massage.timestamp > config_loc.last_block_jurnal_datetime:
                                # Фиксируем самые поздние значения дат и времени 
                                if flag_first: 
                                    new_last_jurnal_datetime = datetime.strftime(entry_datetime, '%Y%m%d%H%M%S')
                                    new_last_block_jurnal_datetime = datetime.strftime(jurnal_next_block_massage.timestamp, '%Y%m%d%H%M%S') 
                                flag_first = False
                                # logger.info(jurnal_next_block_massage.message_type)
                                # Отправка сообщения об ошибке
                                if jurnal_next_block_massage.message_type == 'E': 
                                    # Фиксация сообщений отправленных за текущий день 
                                    cur.execute("SELECT message FROM alerts WHERE date = DATE('now')")
                                    alerts_today = cur.fetchall()
                                    mes_age = ''.join((re.findall(settings.TELEGRAM_SYMBOLS, jurnal_next_block_massage.message)))
                                    # Проверка в локальной БД наличия подобных сообщений за текущий день 
                                    if (mes_age,) not in alerts_today:
                                        # Добвляем сообщения в базу если оно не было отправлено ранее в этот день  
                                        cur.execute(f"INSERT INTO alerts (message, date) VALUES ('{mes_age}', DATE('now'))")
                                        conn.commit()
                                        # Отправка оповещения об ошибке
                                        mes_age = f"{str(jurnal_next_block_massage.timestamp)}:\n {mes_age}"
                                        telegram.send_message(mes_age)
                                        time.sleep(2)
                                        
                                try:
                                    jurnal_next_block_massage = next(jurnal)
                                    # Обходим ошибку при попадании "некорректных" блоков в журнал регистрации (Пока не исследовано, потом уберу костыль)
                                    while jurnal_next_block_massage == False: 
                                        jurnal_next_block_massage = next(jurnal)
                                except StopIteration: 
                                    # print('Я пошёл')
                                    break
                        except Exception as info: 
                            logger.error(info)
        # Изменение значений  в локальном файле конфигурации 
        try: 
            config_loc.set_setting(settings.OPT_MAIN_SEC, 'last_jurnal_datetime', new_last_jurnal_datetime)
            config_loc.set_setting(settings.OPT_MAIN_SEC, 'last_block_jurnal_datetime', new_last_block_jurnal_datetime)
        except NameError: 
            pass 
                        
    except Exception as info:
        logger.info(f'Ошибка выполнения программы {info}')
        telegram.send_message('Ошибка выполнения программы')

    #                     ЗАВЕРШЕНИЕ РАБОТЫ ПРОГРАММЫ                   #
    #--------------------------------------------------------------------
    #Завершение работы, отключение логов
    script.close()
    conn.close()
    #---------------------------------------------------------------------
    


    

    




