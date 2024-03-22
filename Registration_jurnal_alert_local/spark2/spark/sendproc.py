#!/usr/bin/env python3.6
# -*- coding: cp1251 -*-


def GetZabbix (ZabbixKey,ZabbixParam):
   import spark.spsetting as spsett
   sender_path = spsett.ZABBIX_SENDER_PATH
   conf_path = spsett.ZABBIX_CONF_PATH
   import os
   import subprocess
   import shlex
   ZabbixSend =  '"' + sender_path + '"' + ' -c ' + '"' + conf_path + '"' + ' -k ' + '"' + ZabbixKey + '"' + ' -o ' + '"' + str(ZabbixParam) + '"'
   cmd = ZabbixSend
   args = shlex.split(cmd)
   p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   out = p.communicate()[0]
   return out

def GetZabbix1 (ZabbixKey,ZabbixParam):
   import spark.spsetting as spsett
   sender_path = spsett.ZABBIX_SENDER_PATH
   conf_path = spsett.ZABBIX_CONF_PATH
   import os
   import subprocess
   ZabbixSend =  '"' + sender_path + '"' + ' -c ' + '"' + conf_path + '"' + ' -k ' + '"' + ZabbixKey + '"' + ' -o ' + '"' + str(ZabbixParam) + '"'
   cmd = ZabbixSend
   p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
   out = p.stdout.readlines()
   return out

def get_script (strProgramName):
   import os
   import subprocess
   import shlex
   cmd = strProgramName
   args = shlex.split(cmd)
   p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   out = p.communicate()
   outmod = out[0].decode('utf8')
   return outmod



