from pathlib import Path
import logging
import logging.config
import logging.handlers
import sys

log = logging.getLogger("App")


class SyslogFormatter(logging.Formatter):
    """Create an RFC 5424 compliant syslog formatter.

    The logging syslog formatter as-is is non-compliant.
    See the URL below for details.
    https://docs.python.org/3/howto/logging-cookbook.html#inserting-a-bom-into-messages-sent-to-a-sysloghandler
    """

    def format(self, record):
        return "\ufeff" + super().format(record)


def setup_logging(log_path: Path):
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(module)s %(levelname)s %(message)s")

    # File logging.
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Stream logging.
    stream_handler = logging.StreamHandler(stream=sys.stderr)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)

    # Stream logging.
    sys_handler = logging.handlers.SysLogHandler(
        address="/dev/log", facility=logging.handlers.SysLogHandler.LOG_LOCAL1
    )
    syslog_formatter = SyslogFormatter("%(name)s %(module)s %(levelname)s %(message)s")
    sys_handler.setFormatter(syslog_formatter)
    sys_handler.setLevel(logging.WARNING)

    # Add handlers.
    log.addHandler(file_handler)
    log.addHandler(stream_handler)
    log.addHandler(sys_handler)
