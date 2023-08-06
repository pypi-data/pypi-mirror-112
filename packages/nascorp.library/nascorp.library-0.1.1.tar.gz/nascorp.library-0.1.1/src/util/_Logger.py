import os
import json
import logging.config

import util._IsoFormatter


def config_logger(loader_path,
                  log_name='component',
                  configure_root=False,
                  root_level=logging.INFO,
                  max_files=5,
                  max_size=5242880,
                  add_error_handler=False):

    real_path = os.path.realpath(loader_path)
    if os.path.isfile(real_path) and real_path.endswith(".json"):
        with open(real_path, "rb") as f:
            json_loads = json.loads(f.read().decode("utf-8"))
            handlers = json_loads.get("handlers")
            if handlers:
                for handler in handlers:
                    file_name = sys_parsefilepath(handlers[handler].get("filename", ""))
                    if file_name:
                        handlers[handler]["filename"] = file_name

                loader_path = json_loads

    _config_logger(loader_path, log_name, configure_root, root_level, max_files, max_size, add_error_handler)


def _config_logger(loader_path,
                   log_name='component',
                   configure_root=False,
                   root_level=logging.WARN,
                   max_files=5,
                   max_size=5242880,
                   add_error_handler=False):

    if type(loader_path) == dict:
        logging.config.dictConfig(loader_path)
        return

    real_path = os.path.realpath(loader_path)
    if os.path.isfile(real_path) and real_path.endswith(".ini"):
        logging.config.fileConfig(real_path, disable_existing_loggers=False)
        return

    if os.path.isfile(real_path) and real_path.endswith(".json"):
        with open(real_path, "rb") as f:
            logging.config.dictConfig(json.loads(f.read().decode("utf-8")))
        return

    if os.path.isdir(real_path):
        dir_path = real_path
    else:
        dir_path = os.path.dirname(real_path)

    filename = os.path.join(dir_path, log_name + '.log')
    filename_error = os.path.join(dir_path, log_name + '.error.log')

    formatter = util._IsoFormatter.IsoFormatter()

    comp_logger = logging.getLogger(log_name)
    comp_logger.setLevel(logging.DEBUG)
    comp_logger.propagate = False

    rotating_file_logger = logging.handlers.RotatingFileHandler(filename, 'a', max_size, max_files)
    rotating_file_logger.setLevel(logging.DEBUG)
    rotating_file_logger.setFormatter(formatter)
    comp_logger.addHandler(rotating_file_logger)

    if add_error_handler:
        rotating_file_logger_error = logging.handlers.RotatingFileHandler(filename_error,
                                                                          'a',
                                                                          max_size,
                                                                          max_files)
        rotating_file_logger_error.setLevel(logging.ERROR)
        rotating_file_logger_error.setFormatter(formatter)
        comp_logger.addHandler(rotating_file_logger_error)

    if configure_root:
        root_logger = logging.getLogger()
        root_logger.addHandler(rotating_file_logger)
        root_logger.setLevel(root_level)
