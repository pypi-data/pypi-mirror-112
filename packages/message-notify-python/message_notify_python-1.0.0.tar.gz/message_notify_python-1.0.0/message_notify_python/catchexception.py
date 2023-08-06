# -*- coding: utf-8 -*-

import sys
from . import messagenotify
from . import messagebody
import traceback

def handle_exception(exc_type, exc_value, exc_traceback):
    try:
        (filename, number, function, line_text) = traceback.extract_tb(exc_traceback)[-1]
        message_notify = messagenotify.MessageNotify.getInstance()
        message_body = messagebody.MessageBody()
        traceback_code = exc_traceback.tb_frame.f_code
        message_body.setType(1)
        message_body.setTitle(exc_value)
        message_body.setLine(str(number))
        message_body.setFile('文件名：{},函数或者模块:{}'.format(traceback_code.co_filename, function))
        message_body.setMessage(line_text)
        message_notify.addMessage(message_body).push()
    except Exception:
        pass

sys.excepthook = handle_exception