

const TripCard = ({ numberOfTrips }: {
    numberOfTrips: number;
}) => {
    return (
        <button class="btn text-primary">
            Trips: {numberOfTrips}
        </button>
    );
};

export default TripCard;
