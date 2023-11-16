from datetime import date
import logging
from logging.config import dictConfig


LOG_LEVEL: str = "DEBUG"
FORMAT: str = (
    "%(levelprefix)s %(asctime)s | %(module)s.%(filename)s: %(lineno)d |"
    " %(message)s"
)
FORMAT_FILE: str = (
    " %(levelname)-8s [%(asctime)s][%(module)s.%(filename)s"
    " %(lineno)d]  %(message)s "
)
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": FORMAT,
        },
        "filr": {
            "format": FORMAT_FILE,
        },
    },
    "handlers": {
        "console": {
            "formatter": "basic",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "level": LOG_LEVEL,
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "filr",
            "filename": (
                f"logs/{date.today().strftime('%Y-%m-%d')}-logconfig.log"
            ),
            "encoding": "utf-8",
            "level": LOG_LEVEL,
        },
    },
    "loggers": {
        "__name__": {
            "handlers": ["console", "file"],
            "level": LOG_LEVEL,
            # "propagate": False
        }
    },
}


def set_logger():
    dictConfig(logging_config)

    logging.getLogger("__name__")
