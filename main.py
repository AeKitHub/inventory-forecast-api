from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
from prophet import Prophet

app = FastAPI()

class InputRow(BaseModel):
    Item_No: str
    Location_Code: str
    ds: str
    y: float

@app.post("/forecast")
async def forecast(data: List[InputRow]):
    df = pd.DataFrame([item.dict() for item in data])
    result = []

    for (item, loc), group in df.groupby(["Item_No", "Location_Code"]):
        m = Prophet()
        group = group[["ds", "y"]]
        group["ds"] = pd.to_datetime(group["ds"])
        m.fit(group)

        future = m.make_future_dataframe(periods=30)
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
