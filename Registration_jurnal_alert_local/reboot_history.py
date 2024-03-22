import sqlite3
from pathlib import Path
from spark2.spscript import (ConfigLocal_main, Script, Logger_main)
import spark2.spsetting as settings
import os

script = Script(app_name='reboot_history', app_description='Очищение истории локальной БД', app_id='2')
logger = Logger_main(script=script, 
                    path_log=str(Path(os.path.dirname(__file__))))
config = ConfigLocal_main(script=script)
config.get(settings.OPT_MAIN_SEC, 'alerts_db')
# Создание соединения с базой данных
conn = sqlite3.connect(config.alerts_db)

c = conn.cursor()

# Выполнение запроса
c.execute("SELECT COUNT(message) FROM alerts")
rows = c.fetchall()
logger.info(f'Всего строк: {rows[0][0]}')
c.execute("DELETE FROM alerts")

rows = c.fetchall()
if not rows: 
    logger.info(f'Результат: {rows} - Успешно')
else: 
    logger.info(f'Результат: {rows} - НЕ успешно')


# Закрытие соединения
conn.commit()
conn.close()
script.close()