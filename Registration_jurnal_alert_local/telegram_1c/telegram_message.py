#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import urllib.request as urllib2
import cfgparam as cfparams
import ssl
import argparse
import requests
from pathlib import Path
import os

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api_token = 'BOT TOKEN'
url = r'https://api.telegram.org/bot{}/sendMessage'.format(api_token)
gmethod = 'POST'
HEADER1 = ['Content-Type','application/json']
HEADER2 = ['Authorization','Bearer 17abac023e2011e6bacd29dbe8ed3543c5c1c840']
file = "ПУТЬ К ФАЙЛУ JSON"
emoji   = {'error':u'\U0001F4A5','recovery':u'\U0001F31F','clock':u'\U0001F552'}
message_status = {'error':'ОШИБКА!','recovery':'ОШИБКА УСТРАНЕНА'}

priority_icon  = {
                  'Информация'		:u'\U0001F4AC',
                  'Предупреждение'	:u'\U000026A0',
                  'Средняя'			:u'\U000026A1',
                  'Высокая'			:u'\U0001F525',
                  'Чрезвычайная'	:u'\U0001F525',
                  'Устранено'       :u'\U0001F552'
                 }

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

parser = argparse.ArgumentParser()
parser.add_argument('mes_theme')
parser.add_argument('mes_body')
namespace = parser.parse_args()

if namespace.mes_theme:
    mes_theme = namespace.mes_theme
if namespace.mes_body:
    mes_body = namespace.mes_body

# --- Выбор смайтика в зависимости от типа сообщения (Ошибка, Ошибка устранена)
status = ""
if (mes_theme[:7] == message_status['error']):
    status = {'emotion':emoji['error'],'text':message_status['error']}
if (message_status['recovery'] in mes_theme):
    status = {'emotion':emoji['recovery'],'text':message_status['recovery']}

query = cfparams.open_json(file)
query['text'] = ''

# --- Тема сообщения
themem = mes_theme.split('!')[1].strip(' ')

# --- ПАРСИНГ СООБЩЕНИЯ
# --- Если сообщение об ошибке
if (mes_theme[:7] == message_status['error']):
    priority = mes_body.split('Важность:')
    actionm = priority[0].split('Событие:')
    begin_action = actionm[0].split('Начало:')

# --- Если сообщение об устранении ошибки
if (str(message_status['recovery']) in str(mes_theme)):
    actionm = mes_body.split('Событие:')
    begin_action = actionm[0].split('Устранено:')
    priority = ('','Устранено')

query['text'] =  '{}*{}*'.format(status['emotion'],status['text']) + '\n' \
                 '*{}:*'.format(themem) + '\n' \
                 '_{}_'.format(actionm[1].strip(' ')) + '\n' \
                 '\n{} _{}_'.format(priority_icon[priority[1].strip(' ')], \
                                    begin_action[1].strip(' '))

#file1 = open('/spscript/Telecom/telegram/zabbix1.log','a')
#file1.write(query['text'])
#file1.close

# -- Отправка сообщения
s = requests.Session()
r = requests.post(url,params=query,
    headers={HEADER1[0]:HEADER1[1]},verify=False)
print(r.status_code)
# if r.status_code == requests.codes['ok']:
#     print(json.loads(r.content))
r.connection.close()


# СМАЙЛИКИ
# u'\U000026A0' - восклицательный знак
# u'\U00002B50' - звезда
# u'\U0001F31F' - звезда
# u'\U0001F4A5' - взрыв
# u'\U0001F198' - sos
# u'\U0001F197' - ok
# u'\U000026A1' - молния
# u'\U000026D4' - знак Кирпич
# u'\U0001F4A1' - лампочка
# u'\U0001F4CC' - скрепка
# u'\U0001F514' - колокольчик
# u'\U0001F552' - часы
# u'\U00002705' - галочка
# u'\U000026A1' - молния
# u'\U0001F4AC' - комментарий
# u'\U0001F4С6' - календарь
# u'\U0001F516' - стикер
# u'\U0001F525' - огонь

