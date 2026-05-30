import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.models.predict import predict, _load_model
from src.utils.configs import load_configs
from src.utils.logging import logs

logger = logs()
config = load_configs()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("запуск сервиса")
    _load_model()
    yield


app = FastAPI(
    title="Сервис предсказания цены авиабилетов",
    description=("Сервис предсказывает цену авиабилета по входным данным"),
    version="1.0.0",
    lifespan=lifespan,
)


class FlightFeatures(BaseModel):
    airline: str = Field(
        ...,
        example="IndiGo",
        description="The name of the airline company. Categorical feature having 6 different airlines.",
    )
    flight: str = Field(
        ...,
        example="6E-123",
        description="Flight stores information regarding the plane's flight code. Categorical feature.",
    )
    source_city: str = Field(
        ...,
        example="Delhi",
        description="City from which the flight takes off. Categorical feature having 6 unique cities.",
    )
    departure_time: str = Field(
        ...,
        example="Morning",
        description="Derived categorical feature obtained by grouping time periods into bins. Stores information about the departure time and has 6 unique time labels.",
    )
    stops: str = Field(
        ...,
        example="zero",
        description="Categorical feature with 3 distinct values that stores the number of stops between the source and destination cities.",
    )
    arrival_time: str = Field(
        ...,
        example="Morning",
        description="Derived categorical feature created by grouping time intervals into bins. Has 6 distinct time labels and keeps information about the arrival time.",
    )
    destination_city: str = Field(
        ...,
        example="Mumbai",
        description="City where the flight will land. Categorical feature having 6 unique cities.",
    )
    class_: str = Field(
        ...,
        example="Economy",
        alias="class",
        description="Categorical feature containing information on seat class; has two distinct values: Business and Economy.",
    )
    duration: float = Field(
        ...,
        example=2.5,
        description="Continuous feature that displays the overall amount of time it takes to travel between cities in hours.",
    )
    days_left: int = Field(
        ...,
        example=7,
        description="Derived characteristic calculated by subtracting the trip date by the booking date.",
    )


class PredictionResponse(BaseModel):
    pred_price: int = Field(..., description="Предсказанная цена")


@app.get("/health", summary="Работоспособность сервиса")
def health():
    from src.models.predict import _model

    return {
        "status": "ok",
        "model_loaded": _model is not None,
    }


@app.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Предсказание цены авиабилета",
)
def predict_price(applicant: FlightFeatures):

    try:
        result = predict(applicant.model_dump(by_alias=True))
        logger.info(f"Результат: {result}")
        return result
    except FileNotFoundError as e:
        logger.error(f"Модель не загружена: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Ошибка предсказания: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка предсказания: {e}")
