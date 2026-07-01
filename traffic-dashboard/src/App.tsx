import { useEffect, useState } from "react";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    } from "chart.js";

import StarusCard from "./components/StatusCard"
import HourlyChart from "./components/HourlyChart"

function App() {
    const [status, setStatus] = 
        useState<Status | null>(null);

    useEffect(() => {
        const loadData = () => {
            .then(res => res.json())
            .then(data => {
                console.log("取得データ:", data);
                setStatus(data);
            })
            .catch(err => {
                console.error("Fetch Error:", err);
            });
        };
        loadData();

        const timer = setInterval(
            loadData,
            30000
        );
        return () => clearInterval(timer);

    }, []);

    const [hourly, setHourly] =
        useState<Hourly>({});
    useEffect(() => {
        const loadData = () => {
            .then(res => res.json())
            .then(data => {
                console.log("hourly", data);
                setHourly(data);
            })
            .catch(err => {
                console.error("Fetch Error:", err);
            });
        };
        loadData();

        const timer = setInterval(
            loadData,
            30000
        );
        return () => clearInterval(timer);

    }, []);

    const options = {
        plugins: {
            title: {
                display: true, 
                text: "Hourly Traffic Volume"
            }
        }
    };

    return (
        <>
            <h1>Traffic Monitor</h1>

            <p>Status value:</p>
            <pre>{JSON.stringify(status, null, 2)}</pre>
            <p>hourly value:</p>
            <pre>{JSON.stringify(hourly, null, 2)}</pre>

            {status && (
                <>
                    <StarusCard
                        cars={status.cars}
                        persons={status.persons}
                        total={status.total_count}
                    />
                    <HourlyChart
                        {hourly}
                    />
                </>
            )}
        </>
    );
}

export default App;