import logging
from rich.logging import RichHandler

class NestFormatter(logging.Formatter):
    pass


handler = RichHandler(
    rich_tracebacks=True,
    show_path=False,
    show_time=False,
)

handler.setFormatter(
    NestFormatter(
        "[Parser] %(process)d - %(asctime)s %(levelname)-8s [%(name)s] %(message)s",
        "%d/%m/%Y %H:%M:%S",
    )
)

logging.basicConfig(
    level=logging.INFO,
    handlers=[handler],
)

logger = logging.getLogger("Practice")