from fastapi import FastAPI, Request
from pydantic import BaseModel
from prophet import Prophet
import pandas as pd
from typing import List
import uvicorn

app = FastAPI()

class InputRow(BaseModel):
    Item_No: str
    Location_Code: str
    ds: str
    y: float

@app.post("/forecast")
async def forecast_endpoint(data: List[InputRow]):
    df = pd.DataFrame([item.dict() for item in data])
    result = []

    for (item, loc), group in df.groupby(["Item_No", "Location_Code"]):
        m = Prophet()
        group = group[["ds", "y"]]
        group["ds"] = pd.to_datetime(group["ds"])
        m.fit(group)

        future = m.make_future_dataframe(periods=30)  # 30-day forecast
        forecast = m.predict(future)

        for row in forecast[-30:].to_dict(orient="records"):
            result.append({
                "Item_No": item,
                "Location_Code": loc,
                "ds": row["ds"].strftime("%Y-%m-%d"),
                "yhat": row["yhat"],
                "yhat_lower": row["yhat_lower"],
                "yhat_upper": row["yhat_upper"]
            })

    return result