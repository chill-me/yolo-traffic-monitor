from fastapi import FastAPI
app = FastAPI()
from fastapi.responses import HTMLResponse
#import pandas as pd
import sqlite3

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
            df["timestamp"], 
            format="%Y-%m-%d-%H:%M:%S"
        )
        hourly_counts = (
            df.groupby(
                df["timestamp"].dt.hour, 
            )
            .size()
        )
        return hourly_counts.to_dict()

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
        conn = sqlite3.connect("traffic.db")
        cursor = conn.cursor()

        # df = pd.read_csv(csv_file)
        # total_count = len(df)
        cursor.execute(
                "SELECT COUNT(*) FROM traffic"
        )
        total_count = cursor.fetchone()[0]
        
        # cars = len(df[df["type"] == "car"])
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM traffic
            WHERE object_type = 'car'
            """
        )
        
        cars = cursor.fetchone()[0]

        # persons = len(df[df["type"] == "person"])
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM traffic
            WHERRE object_type = 'person'
            """
        )
        persons = cursor.fetchone()[0]

        # df["timestamp"] = pd.to_datetime(
        #     df["timestamp"], 
        #     format="%Y-%m-%d-%H:%M:%S"
        # )
        conn.close()

        #hourly_counts = (
        #    df.groupby(
        #        df["timestamp"].dt.hour, 
        #    )
        #    .size()
        #)
        #hourly_html = ""
        #for hour, count in hourly_counts.to_dict().items():
        #    hourly_html += f"<p>{hour}時: {count}台</p>"

        return f"""
                    <html>
                    <head>
                        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                    </head>
                    <canvas id="hourlyChart"></canvas>

                    <script>

                    fetch("/hourly")
                        .then(response => response.json())
                        .then(data => {{

                            const labels = Object.keys(data);
                            const values = Object.values(data);

                            new Chart(
                                document.getElementById("hourlyChart"), 
                                {{
                                    type: "bar",
                                    data: {{
                                        labels: labels, 

                                        datasets: [{{
                                            label: "Traffic Count", 
                                            data: values
                                        }}]
                                    }}
                                }}
                            );
                        }});
                    </script>

                        <body>
                            <h1>Traffic Monitor</h1>

                            <p>Cars: {cars}</p>
                            <p>Persons: {persons}</p>
                            <p>Total Count: {total_count}</p>
                            <h2>Hourly Statistics</h2>
                            {hourly_html}
                        </body>
                    </html>
                """