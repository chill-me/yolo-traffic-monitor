export async function getStatus() {
    const res = await fetch("http://localhost:8000/status")
    return res.json();
}

export async function getHourly() {
    const res = await fetch("http://localhost:8000/hourly")
    return res.json();
}
