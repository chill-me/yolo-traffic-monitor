type props = {
    cars: number;
    persons: number;
    total: number;

};

function StatusCard({ cars, persons, total }: props) {
    return(
        <>
            <h2>Status</h2>
            <p>Cars: {cars}</p>
            <p>Persons: {persons}</p>
            <p>Total: {total}</p>
        </>
    );
}

export default StatusCard;
