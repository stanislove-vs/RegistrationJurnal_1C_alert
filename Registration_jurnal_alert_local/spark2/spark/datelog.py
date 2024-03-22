#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------------------------------------------------------------
# version: 1.0
# Data: 29.06.2022
# Mod: 29.06.2022
# Description: Функции преобразования даты/времени
# -----------------------------------------------------------------------------------------------------------------------------------

def GetDateLog():
    from datetime import datetime
    import time
    CurrentDate = datetime.now()
    DateLog = CurrentDate.strftime('%d.%m.%Y %H:%M')
    return DateLog

def GetDateLogFull():
    from datetime import datetime
    import time
    CurrentDate = datetime.now()
    DateLog = CurrentDate.strftime('%Y-%m-%d %H:%M:%S')
    return DateLog


def GetDateNow():
    from datetime import datetime
    import time
    CurrentDate = datetime.now()
    DateLog = CurrentDate.strftime('%d.%m.%Y')
    return DateLog
