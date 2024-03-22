# version: 1.0.
# Date: 12.03.2024
# Mod: 22.03.2024
# Description: Отправка сообщений из журнала регистрации 1С в Telegram 
# Author:  Соколов С.В.
# Logfile: 

В скрипте registration_jurnal_alert.py используется база данных alerts.db, в которую заносятся
сообщения отправленные сегодня. Если текст очередного блока уже был ранее отправлен за текущий день, 
то повторения отправки не будет. (Запуск start.cmd)

Очистка истории сообщений 
Скрипт reboot_history.py очищает все данные в таблице alerts.db внутренней БД, что позволяет использовать 
скрипт registration_jurnal_alert.py без учёта ранее отправленных за текущий день сообщений. 

При перенастройке в файле конфигурации conf.cfg:  
enabled = 1 - вкл/выкл выполненния программы (1/0)
path_jurnal = /mnt/sp-qnap/1Cv8Logsp_docs/ - Путь к журналам регистрации 
jurnal_extension = .lgp - Расширение  файлов журнала регистрации 
last_jurnal_datetime = 20240314000003 - Время последнего журнала к которому программа будет обращаться 
                                        формат %Y%m%d%H%M%S. Изменяется после запуска на самую познюю.
last_block_jurnal_datetime = 20240314145355 - Время последнего блока сообщений к которому программа будет обращаться 
                                              формат %Y%m%d%H%M%S. Изменяется после запуска на самую позднюю.
alerts_db = /spscript/1C/Registration_jurnal_alert/alerts.db - файл локальной базы данных, содержит в себе таблицу alerts 
                                                (id INTEGER PRIMARY KEY, message TEXT, date DATE)

В Registration_jurnal_alert_local\telegram_1c\telegram_message.py прописать: 
api_token = 'BOT TOKEN' 
file = "ПУТЬ К ФАЙЛУ JSON"

В Registration_jurnal_alert_local\telegram_1c\1c_ut.json (JSON файл, можно изменить название) прописать: 
"chat_id":"ID чата",

В дирректории Registration_jurnal_alert_local\telegram_1c\ скомпилировать .exe файл 
pyinstaller --onefile telegram_message.py


