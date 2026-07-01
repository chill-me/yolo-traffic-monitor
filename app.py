from fastapi import FastAPI
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import HTMLResponse
import sqlite3

csv_file = "traffic_log.csv"

@app.get("/")
def home():
    return {
        "message": "Traffic Monitor"
    }

@app.get("/status")
def status():
    conn = sqlite3.connect("traffic.db")
    cursor = conn.cursor()

    cursor.execute(
            "SELECT COUNT(*) FROM traffic"
    )
    total_count = cursor.fetchone()[0]
    
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM traffic
        WHERE object_type = 'car'
        """
    )

    cars = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM traffic
        WHERE object_type = 'person'
        """
    )
    persons = cursor.fetchone()[0]
        
    return {
        "persons": persons, 
        "cars": cars, 
        "total_count": total_count
    }

@app.get("/hourly")
def hourly():
    conn = sqlite3.connect("traffic.db")
    cursor = conn.cursor()

    cursor.execute(
            """
            SELECT 
                substr(timestamp, 12, 2) as hour, 
                COUNT(*)
            FROM traffic
            GROUP BY HOUR
            ORDER BY HOUR
            """
    )
    rows = cursor.fetchall()
    conn.close()
    return {
            hour: count
            for hour, count in rows
    }


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
        conn = sqlite3.connect("traffic.db")
        cursor = conn.cursor()

        cursor.execute(
                "SELECT COUNT(*) FROM traffic"
        )
        total_count = cursor.fetchone()[0]
        
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM traffic
            WHERE object_type = 'car'
            """
        )

        cars = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM traffic
            WHERE object_type = 'person'
            """
        )
        persons = cursor.fetchone()[0]

        cursor.execute(
                """
                SELECT
                    substr(timestamp, 12, 2) as hour, 
                    COUNT(*)
                FROM traffic
                GROUP BY hour
                ORDER BY hour
                """
        )
        hourly_html = ""
        labels = []
        values = []

        hourly_counts = cursor.fetchall()
        for hour, count in hourly_counts:
            hourly_html += f"<p>{hour}時: {count}台</p>"
            labels.append(hour)
            values.append(count)

        conn.close()


        return f"""
                    <html>
                    <head>
                        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                    </head>
                    <body>

                    <canvas id="hourlyChart"></canvas>

                    <script>

                            const labels = {labels};
                            const values = {values};

                            <!-- JavaScript -->
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
                            <!-- JavaScript -->

                    </script>

                            {hourly_html}
                        </body>
                    </html>
                """