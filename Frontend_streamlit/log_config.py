import logging

file_log = logging.FileHandler("log_out.log")

console_log = logging.StreamHandler()

log_format = '| %(levelname)s || %(message)s | %(filename)s:%(lineno)s || %(asctime)s'

logging.basicConfig(handlers=(file_log, ),level=logging.INFO,format=log_format,datefmt='%Y-%m-%d %H:%M:%S')