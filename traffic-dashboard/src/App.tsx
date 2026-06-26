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
    
import { Bar } from "react-chartjs-2";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

function App() {
    const [status, setStatus] = useState<any>(null);
    useEffect(() => {
        const loadData = () => {
            fetch("http://localhost:8000/status")
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
            5000
        );

    }, []);

    const [hourly, setHourly] = useState<any>({});
    useEffect(() => {
        fetch("http://localhost:8000/hourly")
            .then(res => res.json())
            .then(data => {
                console.log("hourly", data);
                setHourly(data);
            });
    }, []);

    const chartData = {
        labels: Object.keys(hourly), 
        datasets: [
            {
                label: "Vehicles per Hour", 
                data: Object.values(hourly)
            },
        ],
    };
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
                    <p>Cars: {status.cars}</p>
                    <p>Persons: {status.persons}</p>
                    <p>Total: {status.total_count}</p>
                    <Bar 
                        data={chartData}
                        options={options}
                    />
                </>
            )}
        </>
    );
}

export default App;