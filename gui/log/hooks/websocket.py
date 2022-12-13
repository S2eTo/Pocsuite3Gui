from logging import LogRecord
from pocsuite3.gui.log.hooks import Hook

from pocsuite3.gui.main import socketio


class WebSocketHook(Hook):
    def hook(self, record: LogRecord):
        socketio.emit('message', {'action': 'logger', 'data': {
            "strftime": record.strftime,
            "levelname": record.levelname,
            "levelno": record.levelno,
            "msg": record.msg
        }}, namespace='/ws')
