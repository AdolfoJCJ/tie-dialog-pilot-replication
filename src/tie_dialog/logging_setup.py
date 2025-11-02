
from rich.logging import RichHandler
import logging

def setup_logger(name: str = "tie_dialog", level: int = logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    return logging.getLogger(name)
