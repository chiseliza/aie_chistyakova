from pathlib import Path
import yaml


def load_configs() -> dict:
    file_root = Path(__file__).resolve()
    project_root = file_root.parent.parent.parent
    configs_path = project_root / "configs" / "configs.yaml"

    if not configs_path.exists():
        raise FileNotFoundError(f"Файл конфигов не найден")

    with open(configs_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
