from location import Location, manhattan_distance
from rider import Rider


class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    @type id: str
        A unique identifier for the driver.
    @type location: Location
        The current location of the driver.
    @type is_idle: bool
        A property that is True if the driver is idle and False otherwise.
    @type destination: str
        A location the driver must drive towards, which may not exist
    """

    def __init__(self, identifier, location, speed):
        """Initialize a Driver.

        @type self: Driver
        @type identifier: str
        @type location: Location
        @type speed: int
        @rtype: None
        """
        # TODO
        self.id, self.location, self.speed = identifier, location, speed

        self.destination = None
        self.is_idle = True
        self.rider_time = 0

    def __str__(self):
        """Return a string representation of the driver.

        @type self: Driver
        @rtype: str
        """
        # TODO
        return 'identifier:{}, location:{}, speed:{} idle status:{} ' \
               'destination{}'.format(
            self.id, self.location, self.speed, self.is_idle, self.destination)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @type self: Driver
        @rtype: bool
        """
        # TODO
        return type(self) == type(other) and \
               self.id, self.location, self.speed, self.is_idle == other.id,\
               other.location, other.speed,other.is_idle and\
               self.destination == other.destination


     def get_travel_time(self, destination):
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        @type self: Driver
        @type destination: Location
        @rtype: int
        """
        # TODO
        travel_time = int(manhattan_distance(self.location, destination)
                               / self.speed)
        return travel_time

    def start_drive(self, location):
        """Start driving to the location and return the time the drive will take.

        @type self: Driver
        @type location: Location
        @rtype: int
        """
        # TODO
        self.destination = location
        return self.get_travel_time(self.destination)

    def end_drive(self):
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        """
        # TODO
        self.location = self.destination

    def start_ride(self, rider):
        """Start a ride and return the time the ride will take.

        @type self: Driver
        @type rider: Rider
        @rtype: int
        """
        # TODO
        self.rider_time = int(manhattan_distance(rider.origin, rider.destination)
                             /self.speed)
        self.destination = rider.destination
        return self.rider_time


    def end_ride(self):
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        """
        # TODO
        self.location = self.destination
