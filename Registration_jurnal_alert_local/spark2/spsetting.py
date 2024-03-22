#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------------------------------------------------------------
# version: 1.0
# Data: 29.06.2022
# Mod: 29.03.2023
# Description: Глобальные константы для скриптов
# -----------------------------------------------------------------------------------------------------------------------------------

ZABBIX_CONF_PATH    = '/etc/zabbix/zabbix_agentd.conf'
ZABBIX_SENDER_PATH  = '/usr/bin/zabbix_sender'
MSSQL_USER = 'sa'
FB_AWARDA_USER = 'TWUSER'
MAIN_JSON_FILE = '/spscript/sp.json'

# -- Параметры почты Zabbix для отправки сообщений --
EMAIL_SERVER = '192.168.0.1'
EMAIL_PORT   = 25
EMAIL_FROM   = 'zabbix@stroyparkdiy.ru'
EMAIL_FROM_TAG = 'Центр мониторинга'

# -- Стандартные директории --
REQUEST_DIR = 'sql'
CFG_DIR     = 'cfg'
CMD_DIR     = 'cmd'
APPLOG_DIR  = 'log'
IMPORT_DIR  = 'import'
EXPORT_DIR  = 'export'
ROOT_DIR    = '/spscript'
SYSLOG_DIR  = '/scriptlog'
QNAP_LOGS_MAIN = '/mnt/sp-qnap/'
ALL_LOGS_UPLOAD = '/mnt/sp-qnap/uploads_zabbix'
ALL_LOGS_MONITORING = '/mnt/sp-qnap/monitoring_zabbix'
ALL_LOGS_RECALC =  '/mnt/sp-qnap/recalc_zabbix'
ALL_LOGS_RARELY_USED = '/mnt/sp-qnap/rarely_used_zabbix'
ALL_LOGS_SCHEDULERS = '/mnt/sp-qnap/schedulers_zabbix'
ALL_LOGS_RC_SCHEDULERS = '/mnt/sp-qnap/04_RC_schedulers'
ALL_LOGS_SP_SCHEDULERS = '/mnt/sp-qnap/01_SP_schedulers'
ALL_LOGS_YZH_SCHEDULERS = '/mnt/sp-qnap/06_YZH_schedulers'
ALL_LOGS_SPC_SCHEDULERS = '/mnt/sp-qnap/09_SPC_schedulers'
SP_SCHEDULERS_FILE_FOR_ALL_LOGS = 'all_logs_sp_schedulers.log'
RC_SCHEDULERS_FILE_FOR_ALL_LOGS = 'all_logs_rc_schedulers.log'
YZH_SCHEDULERS_FILE_FOR_ALL_LOGS = 'all_logs_yzh_schedulers.log'
SPC_SCHEDULERS_FILE_FOR_ALL_LOGS = 'all_logs_spc_schedulers.log'
FIREBIRD_DIR = 'Firebird'
MSSQL_DIR    = 'Mssql'
RETAIL_DIR   = 'Retail'
TELECOM_DIR  = 'Telecom'
SHEDULER_DIR = 'Scheduler/sp'
TSD_DIR = 'TSD'
RECALC_DIR = 'recalc'
RECALC_DIR_SP = 'recalc_ka_sp'
RECALC_DIR_KASSA_SP = 'recalc_kassa_sp'
REGLAMENT_DIR = 'reglament'
OBMEN_DIR = '/spobmen'
SHEDULER    = 'Scheduler'
INPUT = 'input'

# -- Кодировки --------------
FIREBIRD_CHARSET = 'WIN1251'
MSSQL_CHARSET    = 'cp1251'
FILES_CHARSET    = 'windows-1251'
FILES_CHARSET1   = 'cp1251'

# -- Форматы названий файлов --
FORMAT_LOG_FILE = r'{}.log'
NAME_LOG_FILE   = r'{}. {}'
REPORT_LOG_FILE = r'{}. {}. {}'
REPORT_LOG_FILE_DEFAULT = r'{}_{}. {}'

# -- Конфигурационные файлы --
CFGFILE            = 'conf.cfg'
GLOBAL_FB_CFG      = 'fb.cfg'
GLOBAL_MSSQL_CFG   = 'mssql.cfg'
GLOBAL_KASSA_CFG   = 'kassy.cfg'
GLOBAL_POSTGRE_CFG = 'postgre.cfg'

GLOBAL_CFG_DIR    = '/spscript/lib/conf'


REQUEST_VIEW_TYPE = r'{}_view.sql'
REQUEST_MAIN_TYPE = r'{}_main.sql'
REQUEST_FILE      = r'{}.sql'

# Опции Телеграмм --
TELEGRAM_DIR  = '/spscript/Telecom/telegram'
TELEGRAM_BOTS_DIR = 'bots'
TELEGRAM_CHAN_DIR  = 'json'
SEND_TELEGRAM_FILE = 'sendtelegram.py'
SEND_TELEGRAM_TEST_FILE = 'sendtelegram_test.py'

TELEGRAM_BOTS_EXT = '.py'
TELEGRAM_CHAN_EXT = '.json'

TELEGRAM_BOT_SP = '{}{}'.format('stroypark',TELEGRAM_BOTS_EXT)
TELEGRAM_BOT_TEST = '{}{}'.format('test',TELEGRAM_CHAN_EXT)

TELEGRAM_CHAN_ZABBIX = '{}'.format('zabbix')
TELEGRAM_CHAN_KASSY = '{}'.format('kassy')
TELEGRAM_CHAN_TEST = '{}'.format('test')
TELEGRAM_MAIN_CHANEL_FILE = '/spscript/Telecom/telegram/telegram_new/telegram_message.py'
TELEGRAM_TEST_CHANEL_FILE = '/spscript/Telecom/telegram/telegram_test_2/telegram_message.py'
TELEGRAM_UT_CHNEL_FILE = '/spscript/Telecom/telegram/telegram_1c/telegram_message.py'
TELEGRAM_SYMBOLS = '[а-яА-Я \.a-zA-Z:/0-9\,\n\(\)\{\}]'

# -- Стандартные аргументы --
ARG_DB_NAME  = 'db_name'
ARG_USE_HOST = 'use_host'
ARG_CFG_FILE = 'cfg_file'


# Стандартные опции конфигов
OPT_IDDB        = 'id_db'
OPT_IPADDRESS   = 'ip_address'
OPT_DESCRIPTION = 'description'
OPT_HOSTNAME    = 'host_name'
OPT_DBNAME      = 'db_name'
OPT_PORT        = 'port'
OPT_USER        = 'user'
OPT_PASS        = 'pass'
OPT_ENABLED     = 'enabled'
OPT_TIMEOUT     = 'con_timeout'
OPT_VIEW_ONLY_ERROR = 'view_only_error'
OPT_VIEWON_WINDOW   = 'view_on_window'
OPT_VIEW_DETAIL     = 'view_detail'
OPT_ZABBIX_SEND     = 'zabbix_send'
OPT_ZABBIX_KEY      = 'zabbix_key'
OPT_TELEGRAM_SEND   = 'telegram_send'
OPT_MSG_SENDER      = 'msg_sender'
OPT_EMAIL_SEND      = 'email_send'
OPT_EMAIL_SERVER    = 'server'
OPT_EMAIL_PORT      = 'port'
OPT_EMAIL_USER      = 'user'
OPT_EMAIL_PASS      = 'password'
OPT_EMAIL_SUBJ      = 'subject'
OPT_EMAIL_FROMTAG   = 'FromTag'
OPT_EMAIL_FROM      = 'from'
OPT_EMAIL_TO        = 'to'
OPT_TELEGRAM_BOT    = 'bot'
OPT_TELEGRAM_CHAN   = 'channel'
OPT_SHARE_PATH        = 'share_path' 
OPT_LIMITATION      = 'limitation'
OPT_INPUT_PATH      = 'input_path'
 
 

#Опции ТСД 
TSD_DIRECTS     = 'TSD_directs'
TSD_IN          = 'in'
TSD_OUT         = 'out'
TSD_GOODS_ATTRIBUTES = 'goods_attributes'
TSD_EXCEPTIONS  = 'except_TSD'
TSD_LOAD_PARAMETR = 'load_parametr'
TSD_WAREHOUSES_LIDS = 'warehouses_lids'
DM_ARTS = '%d_%m_%Y_Arts.dm'
DM_BARCODES = '%d_%m_%Y_BarCodes.dm'
DM_UNITS = '%d_%m_%Y_Units.dm'
DM_USERS = '%d_%m_%Y_Users.dm'
DM_TEMPLATES = '%d_%m_%Y_TempLates.dm'
DM_DOC = '%d_%m_%Y_Doc.dm'
DM_WAREHOUSES = '%d_%m_%Y_Warehouses.dm'
TSD_UPLOADS_DIR = 'uploads'
TSD_UPLOADS_COMPARE_DIR = 'uploads_compare'
TSD_CURRENT_PATH = 'current' 
TSD_PEVIOUS_PATH = 'previous'
DM_ARTS_UPDATE = '%d_%m_%Y_updated_Arts.dm'
DM_BARCODES_UPDATE = '%d_%m_%Y_updated_BarCodes.dm'
#Шаблоны ТСД
TSD_BARCODES_TEMPLATE = '{};{};{};{};{};{};{};'


# Стандартные разделы конфигов
OPT_MAIN_SEC   = 'MAIN'
OPT_ZABBIX_SEC = 'ZABBIX'
OPT_TELEGRAM_SEC = 'TELEGRAM'
OPT_EMAIL_SEC = 'MAIL'
OPT_TSD_SEC = 'TSD'
OPT_RECALC_SP       = 'RECALC_KA_SP'
OPT_RECALC_SP_KASSA = 'RECALC_KASSA_SP'

from pathlib import Path
import sys
spark_lib = Path('/spscript','lib','libs','spark')
sys.path.append(str(spark_lib))
import json
#import spark.cfgparam as cfparams
import cfgparam as cfparams

def get_databases (db_platform,db_name):
    query = cfparams.open_json(MAIN_JSON_FILE)
    return query['databases'][db_platform][db_name]

def get_mail (mail_name):
    query = cfparams.open_json(MAIN_JSON_FILE)
    return query['email'][mail_name]
