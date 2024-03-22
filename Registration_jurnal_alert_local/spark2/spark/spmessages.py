#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------------------------------------------------------------
# version: 1.0
# Data: 29.06.2022
# Mod: 29.06.2022
# Description: Глобальные сообщения, используемые в скриптах
# -----------------------------------------------------------------------------------------------------------------------------------

MSG_ENABLED_OFF = 'Запуск программы отключен'

CFGFILE    = 'conf.cfg'
GLOBAL_FB_CFG = 'fb.cfg'
GLOBAL_MSSQL_CFG = 'mssql.cfg'
GLOBAL_POSTGRE_CFG = 'postgre.cfg'
GLOBAL_CFG_DIR = '/spscript/lib/conf'

REQUEST_VIEW_TYPE = r'{}_view.sql'
REQUEST_MAIN_TYPE = r'{}_main.sql'

MSG_CFG_NOT_FOUND         = 'Отсутствует файл конфигурации {}.'
MSG_LOCCFG_NOT_FOUND      = 'Отсутствует файл локальной конфигурации.'
MSG_LOCCFG_NOT_FOUND_INFO = 'Отсутствует файл локальной конфигурации {}.'
MSG_GLBCFG_NOT_FOUND      = 'Отсутствует файл глобальной конфигурации.'
MSG_GLBCFG_NOT_FOUND_INFO = 'Отсутствует файл глобальной конфигурации {}.'
MSG_REGLAMENTCFG_NOT_FOUND = 'Отсутствует файл конфигурации запуска скрипта.'
MSG_REGLAMENTCFG_NOT_FOUND_INFO = 'Отсутствует файл конфигурации запуска скрипта {}. '
MSG_CFG_NOT_FOUND_INFO          = 'Отсутствует файл {} конфигурации: {}'

MSG_CFG_IO_ERROR         = 'Ошибка чтения файла конфигурации {}.'
MSG_LOCCFG_IO_ERROR      = 'Ошибка чтения локального файла конфигурации.'
MSG_LOCCFG_IO_ERROR_INFO = 'Ошибка чтения локального файла конфигурации {}.'
MSG_GLBCFG_IO_ERROR      = 'Ошибка чтения глобального файла конфигурации.'
MSG_GLBCFG_IO_ERROR_INFO = 'Ошибка чтения глобального файла конфигурации {}.'
MSG_REGLAMENTCFG_IO_ERROR = 'Ошибка чтения файла конфигурации запуска скрипта.'
MSG_REGLAMENTCFG_IO_ERROR_INFO = 'Ошибка чтения файла конфигурации запуска скрипта {}.'

MSG_GLBCFG_FILE          = 'Файл глобальной конфигурации: {}.'
MSG_LOCCFG_FILE          = 'Файл локальной конфигурации: {}.'
MSG_CFG_FILE             = 'Файл {} конфигурации: {}.'
MSG_REGLAMENTCFG_FILE       = 'Файл конфигурации запуска скрипта {}'
MSG_SQL_FILE                 = 'Файл запроса SQL:{}/{}' 


MSG_BASE_CONNECTION = 'Подключение к базе данных: {}.'

MSG_DBMON_DISABLED           = 'Мониторинг базы данных {} отключен.'
MSG_OPTION_DISABLE           = 'Опция отключена. ({})'
MSG_OPTIONNAME_DISABLE       = 'Опция: {} отключена. ({})'
MSG_DBCONNECT_ERROR          = 'Ошибка подключения к БД {}.'
MSG_DBCONNECT_ERROR_INFO     = 'Ошибка подключения к БД {}. {}'
MSG_DBCONNECT_ERROR_INFO_SRV = '{} Ошибка подключения к БД {}. {}'
MSG_REQUESTS_NOTFOUND        = 'Файл запроса {}\{} не найден.'
MSG_REQUESTS_NULL            = 'Файл запроса {}\{} пуст.'
MSG_ZABBIX_SEND_DISABLED     = 'Функция отправки данных {} в zabbix отключена.'
MSG_FUNCTION_DISABLED_ADMIN  = 'Функция "{}" отключена администратором.'
MSG_FUNCTION_DISABLED        = 'Функция "{}" отключена пользователем.'



MSG_LOG_BEGIN             = u'--- Начало работы.'
MSG_LOG_OVER              = u'--- Конец работы.'
MSG_BEGIN_SEPARATOR       = '-----------------------------------------------------------'
MSG_BEGIN_SEPARATOR_SMALL = '--'

#Оповещения по выгрузке
MSG_GOODS_UPLOAD = 'Выгружено {} шт. товаров всего'
MSG_DISCOUNT_UPLOAD = 'Выгружено {} шт товаров, учавствующих в МА'
MSG_FILE_NOT_FOUND = 'Файл выгрузки {} не обнаружен!'
MSG_BARCODES_UPLOAD = 'Выгружено {} шт. штрихкодов'
MSG_WAREHOUSES_UPLOAD = 'Выгружено {} наборов данных по складам'
MSG_UNITS_UPLOAD = 'Выгружено {} единиц измерения'
MSG_TSD_DIRNAME_UPLOAD = 'Файл выгружен на ТСД №: {}'
MSG_PROGRESS_BAR = 'Заполнение файла'
MSG_TIME_PROGRAM_EXECUTION   = 'Время выполнения программы: {}'
MSG_TSD_UPLOAD_ERROR = 'Ошибка перемещения файлв {}'

#Оповещения по пересчёту 
MSG_INPUT_FILE_KA           = 'Файл загрузки LID KA: {}.'
MSG_INPUT_FILE_KA_NOT_FOUND = 'Файл загрузки LID KA: {} не обнаружен.'
MSG_INPUT_FILE_KASSA        = 'Файл загрузки LID касс: {}.'
MSG_INPUT_FILE_KASSA_NOT_FOUND = 'Файл загрузки LID касс: {} не обнаружен.'
MSG_EMPTY_RECALC_LIST       = 'Файл пересчёта пуст.'
MSG_RECALC_KA_START         = 'Начало пересчёта контрагентов в базе {}'
MSG_RECALC_KASSA_START      = 'Начало пересчёта касс в базе {}'
MSG_RECALC_KA_STOP          = 'Окончание пересчёта контрагентов в базе {}'
MSG_RECALC_KA_LIMITATION    = 'Ограничение лимита пересчёта контрагентов: {} шт.'
MSG_RECALC_KA_LIST          = 'Список КА для пересчёта: {}'
MSG_RECALC_KASSA_LIMITATION = 'Ограничение лимита пересчёта касс: {} шт.'
MSG_RECALC_KASSA_LIST       = 'Список касс для пересчёта: {}'
MSG_RECALC_KA_LID_ERROR     = 'Ошибка пересчёта контрагента LID:{} : {}'
MSG_RECALC_KA_SUCCESS       = 'Пересчитан {} {} | RESULT:{} | MSG: {} | Пересчёт: {}'
MSG_RECALC_KASSA_LID_ERROR     = 'Ошибка пересчёта кассы LID:{} : {}'
MSG_RECALC_KASSA_SUCCESS       = 'Пересчитана {} {} | RESULT:{} | {}'


#Оповещения email
MSG_EMAIL_OFF = 'Отправка сообщений по Email отключена.'
MSG_EMAIL_TO = 'Отправленно письмо на: '

#Оповещения TELEGRAM
MSG_TELEGRAM_OFF = 'Отправка сообщений в Telegram отключена'
