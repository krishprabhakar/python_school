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

    def __init__(self, identifier, origin, speed):
        """Initialize a Driver.

        @type self: Driver
        @type identifier: str
        @type location: Location
        @type speed: int
        @rtype: None
        """
        # TODO
        self.id, self.location, self.speed = identifier, origin, speed

        self.destination = None
        self.is_idle = True
        self.rider = False

    def __str__(self):
        """Return a string representation of the driver.

        @type self: Driver
        @rtype: str

        >>> origin = Location(5,2)
        >>> destination = Location(3,2)
        >>> fire = Driver("fire", origin, 5)
        >>> print(fire)
        identifier:fire, location:(5,2), speed:5 idle status:True destination:(None)
        """
        # TODO
        return 'identifier:{}, location:({}), speed:{} idle status:{} ' \
               'destination:({})'.format(self.id, self.location, self.speed,
                                         self.is_idle, self.destination)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @type self: Driver
        @rtype: bool

        >>> origin = Location(5,2)
        >>> destination = Location(3,2)
        >>> fire = Driver("fire", origin, 5)
        >>> ice = Driver("ice",destination, 5)
        >>> fire == ice
        False
        """
        # TODO
        return (type(self) == type(other) and
                self.id == other.id and
                self.location == other.location and
                self.speed == other.destination and
                self.is_idle == other.is_idle and
                self.destination == other.destination)

    def get_travel_time(self, destination):
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        @type self: Driver
        @type destination: Location
        @rtype: int

        >>> origin = Location(5,2)
        >>> destination = Location(30,2)
        >>> kal = Driver("fire", origin, 5)
        >>> kal.get_travel_time(destination)
        5
        >>> bal = Driver("ice", origin, 4)
        >>> bal.get_travel_time(destination)
        6
        """
        # TODO
        travel_time = (manhattan_distance(self.location, destination) /
                       self.speed)
        return travel_time

    def start_drive(self, location):
        """Start driving to the location and return the time the drive will take.

        @type self: Driver
        @type location: Location
        @rtype: int

        >>> origin = Location(5,2)
        >>> destination = Location(30,2)
        >>> kal = Driver("fire", origin, 5)
        >>> kal.start_drive(destination)
        5
        >>> print(kal)
        identifier:fire, location:(5,2), speed:5 idle status:False destination:(30,2)
        """
        # TODO
        self.destination = location
        self.is_idle = False

        return self.get_travel_time(self.destination)

    def end_drive(self):
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None

        >>> origin = Location(5,2)
        >>> destination = Location(30,2)
        >>> kal = Driver("fire", origin, 5)
        >>> kal.start_drive(destination)
        5
        >>> kal.end_drive()
        >>> print(kal)
        identifier:fire, location:(30,2), speed:5 idle status:True destination:(None)
        """
        # TODO
        self.location = self.destination
        self.destination = None
        self.is_idle = True

    def start_ride(self, rider):
        """Start a ride and return the time the ride will take.

        @type self: Driver
        @type rider: Rider
        @rtype: int

        >>> ado = Rider("ado",Location(30,2),Location(30,32),5,3)
        >>> kal = Driver("fire", Location(5,2), 5)
        >>> kal.start_drive(ado.origin)
        5
        >>> kal.end_drive()
        >>> print(kal)
        identifier:fire, location:(30,2), speed:5 idle status:True destination:(None)
        >>> kal.start_ride(ado)
        6
        >>> print(kal)
        identifier:fire, location:(30,2), speed:5 idle status:False destination:(30,32)
        """
        # TODO
        ride_time = (manhattan_distance(rider.origin, rider.destination) /
                     self.speed)
        self.destination = rider.destination
        self.is_idle = False
        self.rider = rider
        return ride_time

    def end_ride(self):
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None

        >>> ado = Rider("ado",Location(30,2),Location(30,32),5, 3)
        >>> kal = Driver("fire", Location(5,2), 5)
        >>> kal.start_drive(ado.origin)
        5
        >>> kal.end_drive()
        >>> print(kal)
        identifier:fire, location:(30,2), speed:5 idle status:True destination:(None)
        >>> kal.start_ride(ado)
        6
        >>> print(kal)
        identifier:fire, location:(30,2), speed:5 idle status:False destination:(30,32)
        >>> kal.end_ride()
        >>> print(kal)
        identifier:fire, location:(30,32), speed:5 idle status:True destination:(None)
        """
        # TODO
        self.location = self.destination
        self.is_idle = True
        self.destination = None
        self.rider = False
