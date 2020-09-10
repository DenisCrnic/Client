import sys
import time
import uos
<<<<<<< HEAD
import uerrno
=======
>>>>>>> d374d6200f5277db1067fa272415d52d6ba77b18

CRITICAL = 50
ERROR    = 40
WARNING  = 30
INFO     = 20
DEBUG    = 10
NOTSET   = 0

_level_dict = {
    CRITICAL: "CRIT",
    ERROR: "ERROR",
    WARNING: "WARN",
    INFO: "INFO",
    DEBUG: "DEBUG",
}

class Logger:

    level = NOTSET

    def __init__(self, name):
        self.name = name

    def _level_str(self, level):
        l = _level_dict.get(level)
        if l is not None:
            return l
        return "LVL%s" % level

    def setLevel(self, level):
        self.level = level

    def isEnabledFor(self, level):
        return level >= (self.level or _level)

    def check_log_size(self, log_file, max_log_size):
        while(uos.stat(log_file)[6] > max_log_size):
            print("Log file is TOO Large")
            print("Opening original file")
            with open(log_file, 'r') as original_file:
                data = original_file.read().splitlines(True)
                print("Closing original file")
                original_file.close()
                
            print("Opening new file")
            with open(log_file, 'w') as new_file:
                print("Writing new file")
                for line in data[1:]:
                    new_file.write(line)
                print("Closing new file")
                new_file.close()
            print("OK")

    def log(self, level, msg, *args):
        if level >= (self.level or _level):
            try:
                print(uos.stat("/main/web_files/log.html")[6])
            except OSError as exc:
                print(exc)
                if exc.args[0] == uerrno.ENOENT:
                    # print("File Doesn't exist, creating one")
                    temp_file = open("/main/web_files/log.html", "w")
                    temp_file.close()
                    # print("File created succsefully!")

            # print(uos.stat("/main/web_files/log.html")[6])
            self.check_log_size("/main/web_files/log.html", 2000)
            _stream = open("/main/web_files/log.html", "a+")
            print("[{}][{}][{}]: {}".format(time.ticks_ms(), self._level_str(level), self.name, msg))
            if not args:
                try:
                    print("[{}][{}][{}]: {}".format(time.ticks_ms(), self._level_str(level), self.name, msg), file=_stream)
                except Exception as err:
                    print("Exception: %s", err)
            else: # TUKAJ MI ŠE NI JASNO KAJ IN KAKO
                print(msg % args, file=_stream)
            _stream.close()

    def debug(self, msg, *args):
        self.log(DEBUG, msg, *args)

    def info(self, msg, *args):
        self.log(INFO, msg, *args)

    def warning(self, msg, *args):
        self.log(WARNING, msg, *args)

    def error(self, msg, *args):
        self.log(ERROR, msg, *args)

    def critical(self, msg, *args):
        self.log(CRITICAL, msg, *args)

    def exc(self, e, msg, *args):
        self.log(ERROR, msg, *args)
        sys.print_exception(e, _stream)

    def exception(self, msg, *args):
        self.exc(sys.exc_info()[1], msg, *args)

_level = INFO
_loggers = {}

def getLogger(name):
    if name in _loggers:
        return _loggers[name]
    l = Logger(name)
    _loggers[name] = l
    return l

def info(msg, *args):
    getLogger(None).info(msg, *args)

def debug(msg, *args):
    getLogger(None).debug(msg, *args)

def basicConfig(level=INFO, filename=None, stream=None, format=None):
    global _level, _stream
    _level = level
    if stream:
        _stream = stream
    if filename is not None:
        print("logging.basicConfig: filename arg is not supported")
    if format is not None:
        print("logging.basicConfig: format arg is not supported")
