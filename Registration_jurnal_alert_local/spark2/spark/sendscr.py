#!/usr/bin/env python3


# Универсальная процедура для отправки сообщения в телеграмм (с дополнительной информацией)
def get_telegram(use_host,priority,msg_body,oth_data,sendtelegram_file,mes_status,mes_title):
    import datelog as datelog

    # Формирование сообщения в соответствии с правилами парсинга
    current_date = datelog.GetDateLogFull()
    err_header = '{} {} {}'.format(mes_status,mes_title,use_host)
    err_body1 = 'Начало: {}'.format(current_date)
    # К телу сообщения добавляем информацию о кассе через разделитель "___"
    err_body2 = 'Событие: {}'.format(msg_body + '___' + oth_data)
    err_body3 = 'Важность: {}'.format(priority)

    # Сформированное сообщение об ошибке
    err_body = '{} {} {}'.format(err_body1,err_body2,err_body3)
    

    # Отправка сообщения через Telegram-канал
#    sender_path = '/spscript/Retail/kassy_retail/telegram_kassy.py'
    sender_path = sendtelegram_file

    import os
    import subprocess
    import shlex
    TelegramSend =  '"' + sender_path + '"' +  ' "' + err_header + '" ' + '"' + err_body + '"'
    cmd = TelegramSend
    args = shlex.split(cmd)
    
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.communicate()[0]
    # print(out)

# Универсальная процедура для отправки сообщения в телеграмм
def get_telegram_main(use_host,priority,msg_body,sendtelegram_file,mes_status,mes_title):
    import datelog as datelog

    # Формирование сообщения в соответствии с правилами парсинга
    current_date = datelog.GetDateLogFull()
    err_header = '{} {} {}'.format(mes_status,mes_title,use_host)
    err_body1 = 'Начало: {}'.format(current_date)
    err_body2 = 'Событие: {}'.format(msg_body)
    err_body3 = 'Важность: {}'.format(priority)

    # Сформированное сообщение об ошибке
    err_body = '{} {} {}'.format(err_body1,err_body2,err_body3)

    # Отправка сообщения через Telegram-канал
#    sender_path = '/spscript/Retail/kassy_retail/telegram_kassy.py'
    sender_path = sendtelegram_file
    
    import os
    import subprocess
    import shlex
    TelegramSend =  '"' + sender_path + '"' +  ' "' + err_header + '" ' + '"' + err_body + '"'
    cmd = TelegramSend
    args = shlex.split(cmd)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.communicate()[0]
    print(out)

