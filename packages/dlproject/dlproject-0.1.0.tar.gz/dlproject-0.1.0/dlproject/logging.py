"""Define the log.

The log level can be set from the command line by defining the environment variable LOG_LEVEL.
"""

import logging
import os
from colorlog import ColoredFormatter

log = logging.getLogger("vertview")


def configure_logging(level=logging.INFO) -> None:
    """Configure the log for vertview, if not using hydra.

    If the environment variable LOG_LEVEL is set, then it supersedes `level`.

    Args:
        level: The logging level.

    """
    ch = logging.StreamHandler()
    ch.setLevel(os.environ.get("LOG_LEVEL", level))
    cf = ColoredFormatter(
        "[%(cyan)s%(asctime)s%(reset)s][%(blue)s%(name)s%(reset)s][%(log_color)s%(levelname)s%(reset)s] - %(log_color)s%(message)s%(reset)s"
    )
    ch.setFormatter(cf)
    log.addHandler(ch)
