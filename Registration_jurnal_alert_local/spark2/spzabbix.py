#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------------------------------------------------------------
# version: 1.0
# Data: 10.12.2021
# Mod: 10.12.2021
# Description: Библиотека функций и процедур для работы с Zabbix через API
# -----------------------------------------------------------------------------------------------------------------------------------

import json
import spark.cfgparam as cfparams

URL               = "http://10.1.222.16/api_jsonrpc.php"
HEADER            = ['Content-Type','application/json-rpc']
GMETHOD           = "POST"
json_PATH         = '/spscript/zabbix/json/'
json_EXT          = '.json'

f_list_pref       = '_list'
f_del_pref        = '_del'
f_ins_pref        = '_create'
f_upd_pref        = '_update'

FILE_ACTION       = 'action'
FILE_AUTH         = 'auth'
FILE_TEMPLATE     = 'template'
FILE_GROUP        = 'group'
FILE_HOST         = 'host'
FILE_ITEM         = 'item'
FILE_TRIGGER      = 'trigger'
FILE_USER         = 'user'
FILE_USER_GROUP   = 'user_group'


items_type = {  "zabbiz_agent"     :0,
                "zabbix_agent_act" :7,
                "trapper"          :2
             }

value_types = { "float"		: 0,
                "char" 		: 1,
                "int"  		: 3
              }

prioritys = {   "info"	    :1,
                "warning"	:2,
                "middle"	:3,
                "high"	    :4,
                "critical"	:5
            }

statuses = {'active':0,'deactive':1}
mediatypes = {'all':0,'email':1}
evaltypes = {'and_or':0,'and':1,'or':2}
condition_types = {'group_host'  :0,
                   'host'        :1,
                   'trigger'     :2,
                   'trigger_name':3,
                   'group_elem'  :15,
                   'tag'         :25,
                   'tag_value'   :26
                  }
operators = {"равно"       :0,
             "не_равно"    :1,
             "содержит"    :2,
             "не_содержит" :3
            }

sctype = ['backup','replicator','fs','kassa','delta']

def send_request(query):
    result = cfparams.json_get_request(query,URL,GMETHOD,HEADER)
    return result

def zabbix_auth(self):
    file = json_PATH + FILE_AUTH + json_EXT
    auth_query = cfparams.open_json(file)
    auth_tmp = send_request(auth_query)
    auth_rez = auth_tmp['result']
    return auth_rez

def get_template (template_name):
    file = json_PATH + FILE_TEMPLATE + json_EXT
    query = cfparams.open_json(file)
    query['auth'] = zabbix_auth(1)
    query['params']['filter']['host'] = template_name
    rez = send_request(query)['result'][0]
    return rez['templateid'], rez['name'], rez['host']

def get_group (group_name):
    file = json_PATH + FILE_GROUP + json_EXT
    query = cfparams.open_json(file)
    query['auth'] = zabbix_auth(1)
    query['params']['filter']['name'] = group_name
    rez = send_request(query)['result'][0]
    return rez['groupid'], rez['name']

def get_host (host_name):
    file = json_PATH + FILE_HOST + json_EXT
    query = cfparams.open_json(file)
    query['auth'] = zabbix_auth(1)
    query['params']['filter']['host'] = host_name
    rez = send_request(query)['result'][0]
    return rez['hostid'],rez['host'],rez['name']

def get_user (*user_alias):
    file = json_PATH + FILE_USER + json_EXT
    query = cfparams.open_json(file)
    query['auth'] = zabbix_auth(1)
    query['params']['filter']['alias'] = user_alias
    rez = send_request(query)['result'][0]
    return rez['userid'],rez['surname'],rez['alias']

def get_user_group (user_group_name):
    file = json_PATH + FILE_USER_GROUP + json_EXT
    query = cfparams.open_json(file)
    query['auth'] = zabbix_auth(1)
    query['params']['filter']['name'] = user_group_name
    rez = send_request(query)['result'][0]
    return rez['usrgrpid'], rez['name']

def get_action (action_name):
    file = json_PATH + FILE_ACTION + json_EXT
    query = cfparams.open_json(file)
    query['auth'] = zabbix_auth(1)
    query['params']['filter']['name'] = action_name
    rez = send_request(query)['result'][0]
    return rez['actionid'], rez['name']

def item_add (item_name,item_name_prefix,host_name,tmp_name,type,value_type,status,key_prefix):
    file = json_PATH + FILE_ITEM + f_ins_pref + json_EXT
    hostid = 0
    if (host_name != None):
        hostid,host,name = get_host(host_name)
    if (tmp_name != None):
       hostid,name_full,name = get_template(tmp_name)
    query = cfparams.open_json(file)
    query['auth'] = zabbix_auth(1)
    key_work = key_prefix + item_name.lower()
    query['params']['name'] = item_name_prefix + item_name
    query['params']['key_'] = key_work
    query['params']['hostid'] = hostid
    query['params']['type'] = type
    query['params']['value_type'] = value_type
    query['params']['status'] = status
    rez = send_request(query)
    return rez,name,key_work

def trigger_add (description,error_expression,priority,tag_main,tag_value,
                 recovery,recovery_expression,tstatus,manual_close):
    file = json_PATH + FILE_TRIGGER + f_ins_pref + json_EXT
    query = cfparams.open_json(file)
    query['auth'] = zabbix_auth(1)
    query['params']['description'] = description
    query['params']['expression'] = error_expression
    query['params']['priority'] = priority
    query['params']['tags'][0]['tag'] = tag_main
    query['params']['tags'][0]['value'] = tag_value
    query['params']['recovery_mode'] = recovery
    query['params']['recovery_expression'] = recovery_expression
    query['params']['status'] = tstatus
    query['params']['manual_close'] = manual_close
    rez = send_request(query)
    return rez

def action_add (name,def_shortdata,def_longdata,
                r_shortdata,r_longdata,username,status,mediatypeid,value,
                evaltype,conditiontype,operator):
    file = json_PATH + FILE_ACTION + f_ins_pref + json_EXT
    query = cfparams.open_json(file)
    query['auth'] = zabbix_auth(1)
    userid,surname,alias = get_user(username)
    query['params']['name'] = name
    query['params']['status'] = status
    query['params']['def_shortdata'] = def_shortdata
    query['params']['def_longdata'] = def_longdata
    query['params']['r_shortdata'] = r_shortdata
    query['params']['r_longdata'] = r_longdata
    query['params']['operations'][0]['opmessage_usr'][0]['userid'] = userid
    query['params']['recovery_operations'][0]['opmessage_usr'][0]['userid'] = userid
    query['params']['recovery_operations'][0]['opmessage']['mediatypeid'] = mediatypeid
    query['params']['operations'][0]['opmessage']['mediatypeid'] = mediatypeid
    query['params']['filter']['evaltype'] = evaltype
    query['params']['filter']['conditions'][0]['value'] = value
    query['params']['filter']['conditions'][0]['conditiontype'] = conditiontype
    query['params']['filter']['conditions'][0]['operator'] = operator
    rez = send_request(query)
    return rez

def action_upd (action_name,def_shortdata,def_longdata,
                r_shortdata,r_longdata,username,status,mediatypeid,value):
    file = json_PATH + FILE_ACTION + f_upd_pref + json_EXT
    query = cfparams.open_json(file)
    query['auth'] = zabbix_auth(1)
    userid,surname,alias = get_user(username)
    actionid,aname = get_action(action_name)
    query['params']['actionid'] = 15
    query['params']['status'] = status
    query['params']['def_shortdata'] = def_shortdata
    query['params']['def_longdata'] = def_longdata
    query['params']['r_shortdata'] = r_shortdata
    query['params']['r_longdata'] = r_longdata
    query['params']['operations'][0]['opmessage_usr'][0]['userid'] = userid
    query['params']['recovery_operations'][0]['opmessage_usr'][0]['userid'] = userid
    query['params']['recovery_operations'][0]['opmessage']['mediatypeid'] = mediatypeid
    query['params']['operations'][0]['opmessage']['mediatypeid'] = mediatypeid
    query['params']['filter']['conditions'][0]['value'] = value
    rez = send_request(query)
    return rez

def host_add (host_name,view_name,host_group,ip_address,tmp_name):
    file = json_PATH + FILE_HOST + f_ins_pref + json_EXT
    query = cfparams.open_json(file)
    query['auth'] = zabbix_auth(1)
    group_id,group_name = get_group(host_group)
    template_id,template_name,hname = get_template(tmp_name)
    query['params']['host'] = host_name
    query['params']['name'] = view_name
    query['params']['interfaces'][0]['ip'] = ip_address
    query['params']['groups'][0]['groupid'] = group_id
    query['params']['templates'][0]['templateid'] = template_id
    rez = send_request(query)
    return rez








#templates = get_request(json_templates)['result']
#templateid = templates[0]['templateid']




#diction = get_request(json_hosts)['result']
#print(diction[0]['hostid'])
#print(diction[0]['host'])
#print(diction[0]['interfaces'][0]['ip'])





#create_item = get_request(json_item_create)
#print(create_item)

#create_trigger = get_request(json_trigger_create)
#print(create_trigger)

###print(templates[0]['templateid'])
###print(templates[0]['host'])


#session = requests.Session()
#response = session.post(url, headers={'Content-Type': 'application/json-rpc'})
#json_auth = response.json()
