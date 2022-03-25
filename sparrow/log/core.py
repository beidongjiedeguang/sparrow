import logging
from logging.handlers import RotatingFileHandler
from concurrent_log_handler import ConcurrentRotatingFileHandler
import os
import inspect
from pathlib import Path
import datetime
import abc
from rich.logging import RichHandler


class BaseLogger(metaclass=abc.ABCMeta):
    _saved_loggers = {}

    @abc.abstractmethod
    def get_logger(self, name, **kwargs):
        pass

    @abc.abstractmethod
    def debug(self, *msg, sep=" ", **kwargs):
        pass

    @abc.abstractmethod
    def info(self, *msg, sep=" ", **kwargs):
        pass

    @abc.abstractmethod
    def warning(self, *msg, sep=" ", **kwargs):
        pass

    @abc.abstractmethod
    def error(self, *msg, sep=" ", **kwargs):
        pass

    @staticmethod
    def _get_format_msg(currentframe, msg: tuple, level, sep=" "):
        filename = os.path.basename(currentframe.f_back.f_code.co_filename)
        lineno = currentframe.f_back.f_lineno
        msg_list = [str(i) for i in msg]
        msg = sep.join(msg_list)
        msg = f"[{filename}] [line:{(lineno): ^4}] {level: ^7} >>> " + msg
        return msg

    @staticmethod
    def _get_format_logger(name, log_abs_path, level=logging.INFO, multi_process=True, stream=True):
        default_formats = {
            "color_format": "%(log_color)s%(asctime)s-%(message)s",
            "log_format": "%(asctime)s-%(message)s",
        }

        log_path = Path(log_abs_path).absolute()
        log_dir = log_path.parent
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        logger = logging.Logger(name, level=level)

        file_formatter = logging.Formatter(
            default_formats["log_format"],
            datefmt="%y/%m/%d %H:%M:%S",
        )

        if multi_process:
            rotating_file_handler = ConcurrentRotatingFileHandler
        else:
            rotating_file_handler = RotatingFileHandler

        file_handler = rotating_file_handler(
            filename=log_path,
            maxBytes=10 * 1024 * 1024,
            backupCount=10,
            encoding="utf-8",
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        if stream:
            logger.addHandler(RichHandler())
        # logger.setLevel(level)
        return logger


class SimpleLogger(BaseLogger):

    def __init__(
            self,
            name="name",
            log_dir="./logs",
            print_stream=True,
            level=logging.DEBUG,
            multi_process=False,
            tz_is_china=True,
    ):
        if tz_is_china:
            logging.Formatter.converter = lambda sec, what: (
                    datetime.datetime.now(tz=datetime.timezone.utc)
                    + datetime.timedelta(hours=8)
            ).timetuple()
        log_path = Path(log_dir).joinpath(name + '.log')

        self._logger = self._get_format_logger(
            f"debug-{name}", log_path, level=level, stream=print_stream, multi_process=multi_process
        )
        self._saved_loggers[name] = self

    @classmethod
    def get_logger(cls,
                   name,
                   log_dir="./logs",
                   print_stream=True,
                   level=logging.DEBUG,
                   multi_process=False,
                   tz_is_china=True) -> "SimpleLogger":
        if name in cls._saved_loggers:
            return cls._saved_loggers[name]
        else:
            return cls(name,
                       log_dir=log_dir,
                       print_stream=print_stream,
                       level=level,
                       multi_process=multi_process,
                       tz_is_china=tz_is_china)

    def log(self, level, *msg, sep=" ", **kwargs):
        currentframe = inspect.currentframe()
        msg = self._get_format_msg(currentframe, msg, logging.getLevelName(level), sep=sep)
        self._logger.log(level, msg, **kwargs)

    def debug(self, *msg, sep=" ", **kwargs):
        currentframe = inspect.currentframe()
        msg = self._get_format_msg(currentframe, msg, "DEBUG", sep=sep)
        self._logger.debug(msg, **kwargs)

    def info(self, *msg, sep=" ", **kwargs):
        currentframe = inspect.currentframe()
        msg = self._get_format_msg(currentframe, msg, "INFO", sep=sep)
        self._logger.info(msg, **kwargs)

    def warning(self, *msg, sep=" ", **kwargs):
        currentframe = inspect.currentframe()
        msg = self._get_format_msg(currentframe, msg, "WARNING", sep=sep)
        self._logger.warning(msg, **kwargs)

    def error(self, *msg, sep=" ", **kwargs):
        currentframe = inspect.currentframe()
        msg = self._get_format_msg(currentframe, msg, "ERROR", sep=sep)
        self._logger.error(msg, **kwargs)


class Logger(BaseLogger):
    """
    Examples:
        >>> logger = Logger(name='train-log', log_dir='./log', print_debug=True)
        >>> logger.debug("hello", "list", [1, 2, 3, 4, 5])

        >>> logger2 = Logger.get_logger('train-log')
        >>> id(logger2) == id(logger)
        >>> True

    """

    def __init__(
            self,
            name="name",
            log_dir="./logs",
            debug_path="debug.log",
            info_path="info.log",
            warning_path="warn.log",
            error_path="error.log",
            multi_process=True,
            print_stream=True,
            print_debug=False,
            print_info=False,
            print_warning=False,
            print_error=False,
            single_mode=False,
            level=logging.DEBUG,
            tz_is_china=True,
    ):
        """
        Parameters
        ----------
            tz_is_china: bool
                time zone is China or not
        """
        if tz_is_china:
            logging.Formatter.converter = lambda sec, what: (
                    datetime.datetime.now(tz=datetime.timezone.utc)
                    + datetime.timedelta(hours=8)
            ).timetuple()
        if print_stream:
            if not any([print_debug, print_info, print_warning, print_error]):
                print_info, print_warning, print_error = True, True, True
            elif print_debug:
                print_info, print_warning, print_error = True, True, True
            elif print_info:
                print_error, print_warning = True, True
            elif print_warning:
                print_error = True

        debug_path = Path(log_dir).joinpath(debug_path)
        info_path = Path(log_dir).joinpath(info_path)
        warning_path = Path(log_dir).joinpath(warning_path)
        error_path = Path(log_dir).joinpath(error_path)

        self._debug_logger = self._get_format_logger(
            f"debug-{name}", debug_path, level=logging.DEBUG, stream=print_debug, multi_process=multi_process
        )
        self._info_logger = self._get_format_logger(
            f"info-{name}", info_path, level=logging.INFO, stream=print_info, multi_process=multi_process
        )
        self._warining_logger = self._get_format_logger(
            f"warning-{name}", warning_path, level=logging.WARNING, stream=print_warning, multi_process=multi_process
        )
        self._error_logger = self._get_format_logger(
            f"error-{name}", error_path, level=logging.ERROR, stream=print_error, multi_process=multi_process
        )
        self._single_mode = single_mode
        self._level = level
        self._saved_loggers[name] = self

    @classmethod
    def get_logger(cls, name, **kwargs) -> "Logger":
        if name in cls._saved_loggers:
            return cls._saved_loggers[name]
        else:
            return cls(name=name, **kwargs)

    def debug(self, *msg, sep=" ", **kwargs):
        currentframe = inspect.currentframe()
        msg = self._get_format_msg(currentframe, msg, "DEBUG", sep=sep)
        if self._level <= logging.DEBUG:
            self._debug_logger.debug(msg, **kwargs)

    def info(self, *msg, sep=" ", **kwargs):
        currentframe = inspect.currentframe()
        msg = self._get_format_msg(currentframe, msg, "INFO", sep=sep)
        if self._level <= logging.INFO:
            self._info_logger.info(msg, **kwargs)
            if not self._single_mode:
                self._debug_logger.info(msg, **kwargs)

    def warning(self, *msg, sep=" ", **kwargs):
        currentframe = inspect.currentframe()
        msg = self._get_format_msg(currentframe, msg, "WARNING", sep=sep)
        if self._level <= logging.WARNING:
            self._warining_logger.warning(msg, **kwargs)
            if not self._single_mode:
                self._debug_logger.warning(msg, **kwargs)
                self._info_logger.warning(msg, **kwargs)

    def error(self, *msg, sep=" ", **kwargs):
        currentframe = inspect.currentframe()
        msg = self._get_format_msg(currentframe, msg, "ERROR", sep=sep)
        if self._level <= logging.ERROR:
            self._error_logger.error(msg, **kwargs)
            if not self._single_mode:
                self._debug_logger.error(msg, **kwargs)
                self._info_logger.error(msg, **kwargs)
                self._warining_logger.error(msg, **kwargs)
