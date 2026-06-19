from fastapi import FastAPI
app = FastAPI()

import pandas as pd

csv_file = "traffic_log.csv"

@app.get("/")
def home():
    return {
        "message": "Traffic Monitor"
    }
@app.get("/status")
def status():
    df = pd.read_csv(csv_file)
    cars = len(df[df["type"] == "car"])
    persons = len(df[df["type"] == "person"])
    total_count = len(df)

    return {
        "persons": persons, 
        "cars": cars, 
        "total_count": total_count
    }
@app.get("/hourly")
def hourly():
    df = pd.read_csv(csv_file)
    df["timestamp"] = pd.to_datetime(
        df{"timestamp"}, 
        format="%Y-%m-%d-%H:%M:%S"
    )
    df["timestamp"].dt.hour
    hourly_car_counts = (
        df.groupby(
            df("timestamp").dt.hour, 
        )
        .size()
    )

