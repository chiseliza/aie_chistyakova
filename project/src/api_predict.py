import uvicorn
from src.utils.configs import load_configs

config = load_configs()
svc = config.get("service", {})


def main():
    uvicorn.run(
        "src.service.app:app",
        host=svc.get("host", "0.0.0.0"),
        port=svc.get("port", 8000),
        log_level=svc.get("log_level", "info"),
        reload=False,
    )


if __name__ == "__main__":
    main()
