import sys
import importlib
from datetime import datetime
import logging
from abc import abstractmethod, ABCMeta
import os
from .Exceptions import *
import threading
import time

_LEVEL2TXT = {
    0: "NOT SET",
    10: "DEBUG",
    20: "INFO",
    30: "WARNING",
    40: "ERROR",
    50: "CRITICAL",
}

_TXT2LEVEL = {v: k for k, v in _LEVEL2TXT.items()}
_UNIT2DEN = {"k": 1024, "M": 1024**2, "G": 1024**3}


class LoggerGenerator:
    """
    Examples:
    ---------
        >>> from LoggerGenerator import logger_gen
        >>> logger_gen(globals())
        >>> log.info("...")
    """
    def __init__(self):
        self._is_generated: bool = False
        self._LOG_FOLDER: str = "./"
        self._LOG_FOLDER_SET: bool = False
        self._log: logging.Logger = None
        self._pre_level: int = None
        self._FILENAME: str = None
        self._FORMAT: str = "%(asctime)s - %(levelname)s (%(filename)s) : %(message)s"
        self._fmt = logging.Formatter(self._FORMAT)
        self._IS_PRINT: bool = True
        self._IS_FILE: bool = True
        self._SPLIT_SIZE: int = -1
        self._SPLIT_UNIT: str = "k"
        self._split_cnt: int = 1
        self._is_stop = False
        # check time (second) for split file
        self._SPLIT_CHECK_DURATION: int = 30
        self._split_th = None
        self._IS_FILENAME_SET = False
        self._IS_FORMAT_SET = False
        self._IS_FOLDER_SET = False
        self._IS_PRINT_STATUS_SET = False
        self._IS_FILE_STATUS_SET = False
        self._IS_SPLIT_SET = False
        self._globals = []
        self._SAVE_FILE_NUM = -1
        self._fh = None
        self._sh = None

    def check_initialize(base: bool = True):
        """ check _is_generated"""
        def _check_initialize(func):
            def _wrapper(self, *args, **kwargs):
                assert self._is_generated == base
                return func(self, *args, **kwargs)

            return _wrapper

        return _check_initialize

    @check_initialize()
    def get_level(self) -> str:
        """Get log level

        Returns:
        --------
            {str} -- log level 

        Examples:
        ---------
            >>> from LoggerGenerator import logger_gen
            >>> logger_gen.get_level()      # Raise exception because logger is not generated.
            >>> logger_gen(globals())       # Once call this code, logger is generated.
            >>> logger_gen.get_level()
        """
        global _LEVEL2TXT
        return _LEVEL2TXT[self._log.level]

    @check_initialize()
    def set_level(self, level: str) -> str:
        global _TXT2LEVEL
        assert level in _TXT2LEVEL
        self._pre_level = self._log.level
        self._log.setLevel(_TXT2LEVEL[level])

    @check_initialize()
    def stop(self):
        self._pre_level = self._log.level
        self._log.setLevel(1000)
        self._is_stop = True

    @check_initialize()
    def restart(self):
        self._log.setLevel(self._pre_level)
        self._is_stop = False

    @check_initialize(False)
    def set_filename(self, filename: str):
        if not self._IS_FILENAME_SET:
            self._FILENAME = filename
            self._IS_FILENAME_SET = True

    @check_initialize(False)
    def set_format(self, _format: str):
        if not self._IS_FORMAT_SET:
            self._FORMAT = _format
            self._IS_FORMAT_SET = True

    @check_initialize(False)
    def set_folder(self, log_folder: str):
        if not self._IS_FOLDER_SET:
            assert os.path.exists(log_folder)
            assert not self._LOG_FOLDER_SET, AlreadySetFolderException()

            self._LOG_FOLDER = log_folder
            if not self._LOG_FOLDER[-1] == "/":
                self._LOG_FOLDER += "/"

            self._LOG_FOLDER_SET = True

    @check_initialize(False)
    def set_print_status(self, status: bool):
        if not self._IS_PRINT_STATUS_SET:
            self._IS_PRINT = status
            self._IS_PRINT_STATUS_SET = True

    @check_initialize(False)
    def set_file_status(self, status: bool):
        if not self._IS_FILE_STATUS_SET:
            self._IS_FILE = status
            self._IS_FILE_STATUS_SET = True


    @check_initialize(False)
    def _generate_log(self):
        self._is_generated = True
        now = datetime.now()
        year = str(now.year)
        month = str(now.month).zfill(2)
        day = str(now.day).zfill(2)
        hour = str(now.hour).zfill(2)
        minute = str(now.minute).zfill(2)
        second = str(now.second).zfill(2)

        if self._FILENAME is None:
            self._FILENAME = f"{self._LOG_FOLDER}{year}{month}{day}-{hour}{minute}{second}_{self._split_cnt}.log"

        self._log = self._get_log()

    def _get_log(self) -> logging.Logger:
        log = logging.getLogger(__name__)
        log.setLevel(logging.DEBUG)

        if self._IS_PRINT:
            self._generate_sh()
            log.addHandler(self._sh) 
        
        if self._IS_FILE:
            self._generate_fh()
            log.addHandler(self._fh)

        return log

    def _generate_sh(self):
        self._sh = logging.StreamHandler(sys.stdout)
        self._sh.setLevel(logging.DEBUG)
        self._sh.setFormatter(self._fmt)

    def _generate_fh(self):
        self._fh = logging.FileHandler(self._FILENAME, mode="w")
        self._fh.setFormatter(self._fmt)
          
    def _update_log(self):
        if self._IS_PRINT:
            self._log.removeHandler(self._sh)
            self._generate_sh()
            self._log.addHandler(self._sh)
        if self._IS_FILE:
            self._log.removeHandler(self._fh)
            self._generate_fh()
            self._log.addHandler(self._fh)

    @check_initialize(False)
    def split_log_by_size(self, size: int, unit: str = "k", duration: int = 30):
        """Split log file according to the file size.
        Once you call this function, split function is enabled and thread will be started.

        Arguments:
        ----------
            size {int} -- criteria for split

        Keyword Arguments:
        ------------------
            unit {str} -- unit of specified size (default: k)
                          you can specify the unit k, M and G.
            duration {int} -- duration for checking (default: 30)
        """
        if not self._IS_SPLIT_SET:
            assert unit in ("k", "M", "G")
            self._SPLIT_UNIT = unit
            self._SPLIT_SIZE = size
            self._SPLIT_CHECK_DURATION = duration
            self._IS_SPLIT_SET = True
    
    def _update_filename(self):
        split_filename = self._FILENAME.split("_")
        self._FILENAME = "_".join(split_filename[:-1]) + f"_{self._split_cnt}.log"

    def _get_remove_filename(self) -> str:
        split_filename = self._FILENAME.split("_")
        return "_".join(split_filename[:-1]) + f"_{self._split_cnt-self._SAVE_FILE_NUM+1}.log"

    def _split_thread(self):
        global _UNIT2DEN
        last_check_time = time.time()
        while not self._is_stop:
            if time.time() - last_check_time > self._SPLIT_CHECK_DURATION:
                importlib.reload(logging)
                filesize = os.path.getsize(self._FILENAME) / _UNIT2DEN[self._SPLIT_UNIT]
                if filesize > self._SPLIT_SIZE:
                    self._split_cnt += 1
                    self._update_filename()
                    self._update_log()

                    if 0 < self._SAVE_FILE_NUM < self._split_cnt + 1:
                        os.remove(self._get_remove_filename())

                last_check_time = time.time()

    @check_initialize(False)
    def remove_old_files(self, save_num: int):
        self._SAVE_FILE_NUM = save_num
    
    def __call__(self, g: dict) -> logging.RootLogger:
        if not self._is_generated:
            self._generate_log()

        g["log"] = self._log
        self._split_th = threading.Thread(target=self._split_thread)
        self._split_th.start()
        self._globals.append(g)

    def __del__(self):
        self._is_stop = True


logger_gen = LoggerGenerator()
