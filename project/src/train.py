from src.models.train_models import train_model
from src.utils.configs import load_configs
from src.utils.logging import logs
from pathlib import Path

logger = logs()

config = load_configs()


def train() -> None:
    processed_data_path = config["data"]["processed_path"]
    train_model(processed_data_path)


if __name__ == "__main__":
    train()
    logger.info("Обучение модели завешено")
