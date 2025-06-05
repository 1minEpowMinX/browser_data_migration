from logging import getLogger, basicConfig, FileHandler, StreamHandler, INFO
from pathlib import Path

LOG_FILE = Path("browser_data_migration.log")

basicConfig(
    level=INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        FileHandler(LOG_FILE, encoding="utf-8"),
        StreamHandler(),  # to see logs in console
    ],
)

logger = getLogger("browser_data_migration")
