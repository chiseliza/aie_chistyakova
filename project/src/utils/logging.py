import logging
from pathlib import Path


def logs(
    level: int = logging.INFO,
    logs_dir: Path = Path("artifacts/logs"),
    filename: str = "logs.log",
) -> logging.Logger:
    logger = logging.getLogger()

    if logger.handlers:
        return logger

    logs_dir.mkdir(parents=True, exist_ok=True)
    logs_file = logs_dir / filename

    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    file_handler = logging.FileHandler(logs_file, encoding="utf-8", mode="a")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
