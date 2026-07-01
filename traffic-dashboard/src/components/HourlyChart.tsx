import { Bar } from "react-chartjs-2";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

const chartData = {
    labels: Object.keys(hourly), 
    datasets: [
        {
            label: "Vehicles per Hour", 
            data: Object.values(hourly)
        },
    ],
};

type Hourly = {
    [hour: string]: number
};

return (
    <Bar ={hourly}/>
);