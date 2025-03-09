from log_setup import setup_logging, log
from pathlib import Path
from sub import sub


def main():
    setup_logging(Path("log.log"))
    log.debug("I used .debug")
    log.info("I used .info!")
    log.warning("I used .warning!")
    log.error("I used .error!")
    sub()
