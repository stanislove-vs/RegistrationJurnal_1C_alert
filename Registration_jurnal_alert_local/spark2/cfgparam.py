#!/usr/bin/env python3.6
# -*- coding: cp1251 -*-

# cp1251

# -----------------------------------------------------------------------------------------------------------------------------------
# version: 1.0
# Data: 29.06.2022
# Mod: 29.06.2022
# Description: Общие функции и процедуры для скриптов
# -----------------------------------------------------------------------------------------------------------------------------------


import configparser
# from xlwt import *

# Разделение числа на разряды
def get_gidit_capacity (digit):
	res = '{0:,}'.format(digit).replace(',',' ')
	return res

def get_config(vPath):
    config = configparser.ConfigParser()
    config.read(vPath)
    return config

def get_setting(path,section,setting):
    config = get_config(path)
    value = config.get(section,setting)
    return value

def get_setting_has(path,section,setting,null_value):
    config = get_config(path)
    value = null_value
    if config.has_option(section,setting):
        value = config.get(section,setting)
    return value

def set_setting(path,section,setting,value):
    config = get_config(path)
    config.set(section,setting,value)
    with open(path,'w') as configfile:
        config.write(configfile)

def set_section(path,section):
    config = get_config(path)
    config.sections()
    config.add_section(section)
    config.sections()
    with open(path,'w') as configfile:
        config.write(configfile)

def remove_config_section(path,section):
    config = get_config(path)
    with open (path,'r+') as s:
        config.remove_section(section)
        s.seek(0)
        config.write(s)
        s.truncate()

def open_sql_query(sql_query):
    f = open(sql_query, encoding='utf-8')
    line = f.readline()
    SQLstr = ""
    while line:
        SQLstr = SQLstr + line
        line = f.readline()
        
    f.close
    return SQLstr

def open_text_file(text_file):
    f = open(text_file, encoding='utf-8')
    line = f.readline()
    SQLstr = ""
    while line:
        TXTstr = TXTstr + line
        line = f.readline()
    f.close
    return TXTstr

def open_json(file):
    import json
    with open(file,'r') as data:
        file_data = data.read().encode('utf-8')
        json_data = json.loads(file_data)
    return json_data

def urlopen(*args, **kwargs):
    import urllib.request as urllib2
    return urllib2.urlopen(*args, **kwargs)

def json_get_request(query,url,gmethod,header):
    import json
    import urllib.request as urllib2
    data = json.dumps(query)
    data = data.encode('utf-8')
    req = urllib2.Request(url,data)
    req.get_method = lambda: gmethod
    req.add_header(header[0],header[1])
    res = urlopen(req)
    res_str = res.read().decode('utf-8')
    res_json = json.loads(res_str)
    return res_json

def mssql_init_null(use_host,use_user,use_pass,use_database,use_port):
    import pymssql
    DBconnect = pymssql.connect(host=use_host,user=use_user,password=use_pass,database=use_database,port=use_port)
    return DBconnect

def mssql_init(use_host,use_user,use_pass,use_database,SQLstr):
    import pymssql
    DBconnect = pymssql.connect(host=use_host,user=use_user,password=use_pass,database=use_database)
    cursor = DBconnect.cursor()
    cursor.execute('use [' + use_database + ']; \n' + SQLstr)
    row = cursor.fetchone()
    return  DBconnect,cursor,row

def mssql_init_exec(use_host,use_user,use_pass,use_database,SQLstr):
    import pymssql
    DBconnect = pymssql.connect(host=use_host,user=use_user,password=use_pass,database=use_database)
    cursor = DBconnect.cursor()
    cursor.execute('use [' + use_database + ']; \n' + SQLstr)
#    row = cursor.fetchone()
    result = 1
    return  DBconnect,result

def firebird_init(DBaddress,DBname,SQLstr):
    import firebirdsql
    err_st = 0
    try:
        DBconnect = firebirdsql.connect(
                    host = DBaddress,
                    database = DBname,
                    user='TWUSER', password='54321'
        )
    except Exception:
        err_st = 1
        DBconnect = None
        cur = None
    else:
        cur = DBconnect.cursor()
        cur.execute(SQLstr)
    return DBconnect,cur,err_st

def firebird_init_null(DBaddress,DBname):
    import firebirdsql
    err_st = 0
    try:
        DBconnect = firebirdsql.connect(
                    host = DBaddress,
                    database = DBname,
                    user='TWUSER', password='54321'
        )
    except Exception:
        err_st = 1
        DBconnect = None
        cur = None
    else:
        cur = DBconnect.cursor()
    return DBconnect,cur,err_st

def powershell_init(use_host,login,passw,pscript):
    from pypsrp.powershell import PowerShell, RunspacePool
    from pypsrp.wsman import WSMan
    import winrm
    import re
    wsman = WSMan(use_host,username=login,password=passw,ssl=False,auth='negotiate')
    with RunspacePool(wsman) as pool:
        ps = PowerShell(pool)
        ps.add_script(pscript)
        ps.invoke(['string',2])
    return ps

def powershell_exec(use_host,login,passw,pscript):
    from pypsrp.client import Client
    import winrm
    import re
    client = Client(use_host,username=login,password=passw,port=5985,ssl=False,auth='negotiate')
    output,streams,had_errors = client.execute_ps(pscript)
    return output + '\n',str(streams) + '\n','errors: '+ str(had_errors)

def dateconvert(in_date,format,orig_format):
    import datetime
    import time
    format_mas = [
                   '%Y-%m-%d %H:%M:%S.%f',
                   '%Y-%m-%d %H:%M:%S'
                  ]
    d_new = None
    if (in_date != None):
        d_int = datetime.datetime.strptime(str(in_date),format_mas[orig_format])
        d_new = d_int.strftime(format)
    else:
        d_new = None
    return d_new

def dateconvert_has(in_date,format):
    import datetime
    import time
    format_mas = [
                   '%Y-%m-%d %H:%M:%S.%f',
                   '%Y-%m-%d %H:%M:%S'
                  ]
    d_new = None
    if (in_date != None):
        try:
            d_int = datetime.datetime.strptime(str(in_date),format_mas[0])
        except Exception:
            d_int = datetime.datetime.strptime(str(in_date),format_mas[1])
        else:
            d_new = d_int.strftime(format)
    else:
        d_new = None
    return d_new

def get_logger(lname,log_path,file_name,code_type,view_name,backup_count):
    import logging.handlers
    import os
    ctype = {'win':'cp1251','unicode':'utf-8'}
    logger = logging.getLogger(lname)
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), u'{}'.format(log_path),
                                                   u'{}'.format(file_name)), maxBytes=102400, encoding=ctype[code_type], backupCount=backup_count)
    handler.setLevel(logging.INFO)
#    formatter = logging.Formatter(fmt = u'%(levelname)-5s %(name)-6s  %(asctime)-15s  %(message)s', datefmt = u'%d.%m.%Y %H:%M:%S')
    if (view_name == True):
        formatter = logging.Formatter(fmt = u'%(name)-6s  %(asctime)-15s  %(message)s', datefmt = u'%d.%m.%Y %H:%M:%S')
    else:
        formatter = logging.Formatter(fmt = u'%(asctime)-15s  %(message)s', datefmt = u'%d.%m.%Y %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger,handler


'''
def get_mail
destlst = config.get('MAIL', 'To').split(',')
for dstaddr in destlst:
    Msg = MIMEMultipart()
    Msg.set_charset('windows-1251')
    Msg['From'] = '{}<{}>'.format(config.get('MAIL','FromTag'),config.get('MAIL', 'From'))
    Msg['To'] = dstaddr.strip()
    Msg['Subject'] = make_header([('Отчет по Актам приходования по РМК', 'windows-1251')])
    Msg['Date'] = formatdate(localtime = True)

    Msg.attach(MIMEText('Отчет по Актам приходования по РМК', 'plain', 'windows-1251'))

    Part = MIMEBase('application', "octet-stream")
    Part.set_payload(open(config.get('BASE', 'ExpPath') + "check_apr.xls", "rb").read())
    encoders.encode_base64(Part)
    Part.add_header('Content-Disposition', 'attachment; filename="check_apr.xls"')
    Msg.attach(Part)

    Smtp = smtplib.SMTP(config.get('MAIL', 'Server'), config.get('MAIL', 'Port'))
    Smtp.sendmail(config.get('MAIL', 'From'), dstaddr.strip(), Msg.as_string())
    Smtp.quit()
'''

# Кириллица в заголовке эл.писем
def QuoHead(String):
    import quopri
    s = quopri.encodestring(String.encode('UTF-8'), 1, 0)
    return "=?utf-8?Q?" + s.decode('UTF-8') + "?="

# Передача сообщения списком
def get_mail (fromtag,server,port,mail_from,mail_to,theme,body,codes):
    import smtplib
    import base64
    from email.mime.text import MIMEText
    from email.utils import formatdate
    from email.header import make_header
    from email.mime.multipart import MIMEMultipart
#    destlst = mail_to.split(',')
#    for dstaddr in destlst:
    Msg = MIMEMultipart()
    Msg.set_charset(codes)
    fromtag_conv = QuoHead(fromtag).replace('=\n', '')
    Msg['From'] = '{}<{}>'.format(fromtag_conv,mail_from)
    Msg['To'] = mail_to.strip()
    Msg['Subject'] = make_header([(theme, codes)])
    Msg['Date'] = formatdate(localtime = True)
    Msg.set_charset(codes)
    Msg.attach(MIMEText('\n'.join(body), 'plain', codes))
#    Msg.attach(MIMEText(body, 'plain', codes))
    Smtp = smtplib.SMTP(server, port)
    Smtp.sendmail(mail_from, mail_to.strip(), Msg.as_string())
    Smtp.quit()

# Передача сообщения текстом
def get_mail_text (fromtag,server,port,mail_from,mail_to,theme,body,codes):
    import smtplib
    import base64
    from email.mime.text import MIMEText
    from email.utils import formatdate
    from email.header import make_header
    from email.mime.multipart import MIMEMultipart
    Msg = MIMEMultipart()
    Msg.set_charset(codes)
    fromtag_conv = QuoHead(fromtag).replace('=\n', '')
    Msg['From'] = '{}<{}>'.format(fromtag_conv,mail_from)
    Msg['To'] = mail_to.strip()
    Msg['Subject'] = make_header([(theme, codes)])
    Msg['Date'] = formatdate(localtime = True)
    Msg.attach(MIMEText(body, 'plain', codes))
    Smtp = smtplib.SMTP(server, port)
    Smtp.sendmail(mail_from, mail_to.strip(), Msg.as_string())
    Smtp.quit()

# Передача сообщения с вложением
def get_mail_file (fromtag,server,port,mail_from,mail_to,theme,body,codes,file_path,file_name):
    import smtplib
    from email.mime.text import MIMEText
    from email.utils import formatdate
    from email.header import make_header
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    Msg = MIMEMultipart()
    Msg.set_charset(codes)
    fromtag_conv = QuoHead(fromtag).replace('=\n', '')
    Msg['From'] = '{}<{}>'.format(fromtag_conv,mail_from)
    Msg['To'] = mail_to.strip()
    Msg['Subject'] = make_header([(theme, codes)])
    Msg['Date'] = formatdate(localtime = True)
    Msg.attach(MIMEText(body, 'plain', codes))
    Part = MIMEBase('application', "octet-stream")
    Part.set_payload(open(file_path + file_name, "rb").read())
    encoders.encode_base64(Part)
    Part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(file_name))
    Msg.attach(Part)
    Smtp = smtplib.SMTP(server, port)
    Smtp.sendmail(mail_from, mail_to.strip(), Msg.as_string())
    Smtp.quit()

# Считывание размера файла и дату последней модификации
def get_file_info (file):
    import os
    import time
    file_stat = None
    fsize = 0
    ftime = ''
    error = ''
    date_format = '%d.%m.%Y %H:%M'
    if os.path.exists(file):
        # Определение размера файла
        file_stat = os.stat(file)
        fsize = file_stat.st_size
        fsize = get_gidit_capacity(fsize)

        # Определение времени последней модификации
        import datetime as dt
        time_utc = time.gmtime(file_stat.st_mtime)
        ftime_str = time.strftime(date_format, time_utc)
        ftime_tm = dt.datetime.strptime(ftime_str,date_format)
        # Определение смещения часового пояса в сек.
        # т.к. время извлекается в UTC без применения часового пояса
        tomsk_tz = time.timezone * -1
        # Корректировка полученного времени в соответствии с часовым поясом
        timedelta = ftime_tm + dt.timedelta(seconds = int(tomsk_tz))
        ftime = timedelta.strftime(date_format)
    else:
        error = 'Файл не найден.'
    return fsize, ftime, error

# Установка прав на файл
def set_file_right(file,user,group,other):
    import os,stat
    import grp
    import pwd
    owner_perm = {'r':stat.S_IRUSR,'w':stat.S_IWUSR,'x':stat.S_IXUSR}
    group_perm = {'r':stat.S_IRGRP,'w':stat.S_IWGRP,'x':stat.S_IXGRP}
    other_perm = {'r':stat.S_IROTH,'w':stat.S_IWOTH,'x':stat.S_IXOTH}
    owner_sum = 0
    group_sum = 0
    other_sum = 0
    for key_owner in user:
        owner_sum = owner_sum + owner_perm[key_owner]
    for key_group in group:
        group_sum = group_sum + group_perm[key_group]
    for key_other in other:
        other_sum = other_sum + other_perm[key_other]
    os.chmod(file,(owner_sum+group_sum+other_sum))

# Установка владельца и группы файла
def set_file_owner(file,user,group):
    import os,stat
    import grp
    import pwd
    gid = pwd.getpwnam(group).pw_gid
    uid = pwd.getpwnam(user).pw_uid
    os.chown(file,uid,gid)

def check_file_request(path,file):
    import os
    check_bit = False
    fsql_query = '{}/{}'.format(path,file)
    if os.path.exists(fsql_query):
        check_bit = True
        text = open_sql_query(fsql_query)
    else:
        check_bit = False
        text = None
    return check_bit,text

# Разбить число на разряды
def digit_grouping(digit,group):
    group_separator = ''
    if (group == True):
        group_separator = ' '
    rez = '{0:,}'.format(digit).replace(',', group_separator)
    return rez

#Проверка
def check_file_request_path(path_sql_query):
    import os
    check_bit = False
    
    if os.path.exists(path_sql_query):
        check_bit = True
        text = open_sql_query(path_sql_query)
    else:
        check_bit = False
        text = None
    return check_bit,text

from datetime import datetime
class All_logs: 
    def __init__(self, app_name = 'all_logs', path = '/mnt/sp-qnap/', log_file = 'Лог неопознанных скриптов.log', name_script = 'Empty') -> None:
        self._logger, self.handler = get_logger(app_name, path, log_file, 'win', False, backup_count = 5)
        self.name_script = name_script

    def info(self, text): 
        self._logger.info(f'{self.name_script}: {text}')

    def handler_close(self):
        self.handler.close()
    
class Executer: 
    def __init__(self, sql_path, formater = []) -> None:
        self.sql_path = sql_path
        self._formater = formater
        self.sql_select = sql_path
        

    @property 
    def sql_select(self): 
        return self._sql_select
    @sql_select.setter
    def sql_select(self, sql_path): 
        check, self._sql_select = check_file_request_path(self.sql_path)
        if not check: 
            raise FileNotFoundError('Файл sql запроса отсутсвует')
        # if self.__formater: 
        self._sql_select = self.sql_select.format(*self._formater)
    
    @staticmethod
    def set_description(description_sql_response): 
        column_names = [row[0] for row in description_sql_response]
        return dict(zip(column_names, range(len(column_names))))
    
    def __call__(self, con):
        self.con = con
        self.cur = con.cursor()
        self.cur.execute(self.sql_select)
        self.description = self.set_description(self.cur.description)
        return self
    
    def close(self): 
        self.cur.close()

    def commit(self): 
        self.con.commit()
        
    def __getitem__(self, item):
        item = item.upper() 
        return self.description[item]
    
    def __iter__(self): 
        return iter(self.cur)
    
    def __next__(self): 
        yield from self.cur

    def columns(self, field_width = 15): 
        data = (f"{{:<{field_width}}}".format(element) for element in self.description.keys())
        return " ".join(data)
    
    def row_formater(self, field_width = 15): 
        return f"{{:<{field_width}}} " * len(self.description)

def log_deccorator(logger, message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as info: 
                logger.error(f'{message}: {info}')
        return wrapper
    return decorator
        


