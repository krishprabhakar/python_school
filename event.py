"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from driver import Driver
from location import deserialize_location
from monitor import RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF
from rider import Rider, WAITING, CANCELLED, SATISFIED
from container import PriorityQueue
from location import Location
from dispatcher import Dispatcher
from monitor import Monitor


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    """

    def __init__(self, timestamp):
        """Initialize an Event with a given timestamp.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other):
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other):
        """Return True iff this Event is not equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other):
        """Return True iff this Event is less than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other):
        """Return True iff this Event is less than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other):
        """Return True iff this Event is greater than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other):
        """Return True iff this Event is greater than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self):
        """Return a string representation of this event.

        @type self: Event
        @rtype: str
        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher, monitor):
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        @type self: Event
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    @type rider: Rider
        The rider.
    """

    def __init__(self, timestamp, rider):
        """Initialize a RiderRequest event.

        @type self: RiderRequest
        @type rider: Rider
        @rtype: None

        >>> events = PriorityQueue()
        >>> rider1 = RiderRequest(7, Rider("kal",Location(5,4),Location(2,3),2,5))
        >>> rider2 = RiderRequest(2, Rider("bal",Location(5,4),Location(2,3),2,5))
        >>> rider3 = RiderRequest(5, Rider("cal",Location(5,4),Location(2,3),2,5))
        >>> events.add(rider1)
        >>> events.add(rider2)
        >>> events.add(rider3)
        >>> for x in events._items: print(x)
        2 -- unique_identifier: bal , origin: (5,4), destination: (2,3), patience: 2, status: waiting, timestamp: 5: Request a driver
        5 -- unique_identifier: cal , origin: (5,4), destination: (2,3), patience: 2, status: waiting, timestamp: 5: Request a driver
        7 -- unique_identifier: kal , origin: (5,4), destination: (2,3), patience: 2, status: waiting, timestamp: 5: Request a driver

        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        @type self: RiderRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        >>> events = PriorityQueue()
        >>> rider1 = RiderRequest(7, Rider("kal",Location(5,4),Location(2,3),2,5))
        >>> rider2 = RiderRequest(2, Rider("bal",Location(5,4),Location(2,3),2,5))
        >>> rider3 = RiderRequest(5, Rider("cal",Location(5,4),Location(2,3),2,5))
        >>> events.add(rider1)
        >>> events.add(rider2)
        >>> events.add(rider3)
        """
        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.id, self.rider.origin)

        events = []
        driver = dispatcher.request_driver(self.rider)
        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time, self.rider, driver))
        events.append(Cancellation(self.timestamp + self.rider.patience, self.rider))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: RiderRequest
        @rtype: str
        """
        return "{} -- {}: Request a driver".format(self.timestamp, self.rider)


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    @type driver: Driver
        The driver.
    """

    def __init__(self, timestamp, driver):
        """Initialize a DriverRequest event.

        @type self: DriverRequest
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event.

        @type self: DriverRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        >>> dis = Dispatcher()
        >>> mon = Monitor()
        >>> fire = Driver("fire", Location(5,5), 5)
        >>> inferno = Driver("inferno", Location(5,20), 5)
        >>> kal = Rider("kal", Location(5,2), Location(3,2), 5, 3)
        >>> print(kal)
        unique_identifier: kal , origin: (5,2), destination: (3,2), patience: 5, status: waiting, timestamp: 3
        >>> print(dis.request_driver(kal))
        None
        >>> print(dis.waiting_list[0])
        unique_identifier: kal , origin: (5,2), destination: (3,2), patience: 5, status: waiting, timestamp: 3
        >>> dis2 = Dispatcher()
        >>> driverrequest1 = DriverRequest(3, fire)
        >>> print(driverrequest1.do(dis2,mon))
        []
        >>> print(dis2.request_rider(fire))
        None
        >>> PickupEvent = driverrequest1.do(dis,mon)
        >>> print(PickupEvent[0])
        TimeStamp:3.6 -- Rider:unique_identifier: kal , origin: (5,2), destination: (3,2), patience: 5, status: waiting, timestamp: 3 -- Driveridentifier:fire, location:(5,5), speed:5 idle status:False destination:(5,2): Pickup Event





        """
        # Notify the monitor about the request.
        monitor.notify(self.timestamp, DRIVER, REQUEST,
                       self.driver.id, self.driver.location)

        # Request a rider from the dispatcher.
        events = []
        rider = dispatcher.request_rider(self.driver)
        # If there is one available, the driver starts driving towards the
        # rider, and the method returns a Pickup event for when the driver
        # arrives at the riders location.
        if rider is not None:
            travel_time = self.driver.start_drive(rider.origin)
            #REMEMBER TO CHECK THE OREDER OF THE PICKUP CALL AND WHETHER IT AFFECTS ANYTHING
            events.append(Pickup(self.timestamp + travel_time,self.driver,rider))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: DriverRequest
        @rtype: str
        """
        return "{} -- {}: Request a rider".format(self.timestamp, self.driver)


class Cancellation(Event):
    """A rider cancels ride request.

    === Attributes ===
    @type rider: Rider
        The rider.
    """
    def __init__(self, timestamp, rider):
        """Initialize the cancellation request.

        @type time: int
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider


    def do(self, dispatcher, monitor):
        """Cancel the rider's request if he is still waiting and not picked up

        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Events]
        """
        # Notify the monitor about the request.


        if self.rider.status is not SATISFIED:
            self.rider.cancel()
            # Notify the monitor about the request.
            monitor.notify(self.timestamp, RIDER, CANCEL,
                       self.rider.id, self.rider.origin)
        event = []

        return event

    def __str__(self):
        """Return String Representation of this event

        @return:
        @rtype: String
        """

        return "{} -- {}: Cancel Event".format(self.timestamp, self.rider)


class Pickup(Event):
    # TODO
    # do the docstring
    """A Driver picks up a rider

    === Attributes ===
    @type rider: Rider
        The rider.
    @type driver: Driver
        The Driver

    """
    def __init__(self, timestamp, driver, rider):
        """

        @param timestamp: timestamp of the event
        @type timestamp: int
        @param driver: driver of the vehicle
        @type driver: Driver
        @param rider: rider being picked up
        @type rider: Rider
        """
        super().__init__(timestamp)
        self.driver, self.rider, self.timestamp = driver, rider, timestamp

    def do(self, dispatcher, monitor):
        """ Pickup the rider based on the status of the rider

        @param dispatcher: Dispatches the driver to the rider
        @type dispatcher: Dispatcher
        @param monitor: monitors the events
        @type monitor: Monitor
        @return: events of a dropoff or new rider
        @rtype: list[Event]
        """

        event=[]
        self.driver.start_drive(self.rider.origin)
        self.driver.end_drive()
        if self.rider.status is WAITING:
            self.driver.start_ride(self.rider)
            event.append(Dropoff(self.timestamp, self.driver, self.rider))
            # Notify the monitor about the successful pickup request
            monitor.notify(self.timestamp, RIDER, PICKUP,
                       self.rider.id, self.rider.origin)
            # Notify the monitor about the request.
            monitor.notify(self.timestamp, DRIVER, PICKUP,
                       self.driver.id, self.driver.location
                           )
        elif self.rider.status is CANCELLED:
            event.append(DriverRequest(self.timestamp, self.driver))
        return event

    def __str__(self):
        """ Return String representation of this event

        @return:
        @rtype: String
        """

        return "TimeStamp:{} -- Rider:{} -- Driver{}: Pickup Event".format(self.timestamp, self.rider,
                                                     self.driver)


class Dropoff(Event):
    # TODO
    """ A Driver drops off a rider and looks for a new Rider

     === Attributes ===
    @type rider: Rider
        The rider.
    @type driver: Driver
        The Driver

    """
    def __init__(self, timestamp, driver, rider):
        """ Initializes a dropoff event

        @param timestamp:
        @type timestamp:
        @param driver:
        @type driver:
        @param rider:
        @type rider:
        """
        super().__init__(timestamp)
        self.driver, self.rider, self.timestamp = driver, rider, timestamp

    def do(self, dispatcher, monitor):
        """ Driver drops off rider and looks for a new rider

        @param dispatcher:
        @type dispatcher:
        @param monitor:
        @type monitor:
        @return:
        @rtype:
        """
        event = []
        self.driver.end_ride()
        self.rider.satisfied()

        event.append(DriverRequest(self.timestamp, self.driver))
        # Notify the monitor about the request.
        monitor.notify(self.timestamp, DRIVER, DROPOFF,
                       self.driver.id, self.driver.location)
        # Notify the monitor about the request.
        monitor.notify(self.timestamp, RIDER, DROPOFF,
                       self.rider.id, self.rider.destination)

        return event



def create_event_list(filename):
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    @param filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]
    """
    events = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                # Skip lines that are blank or start with #.
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'RiderRequest', 'Cerise', '4,2', '1,5', '15'].
            # Note that these are strings, and you'll need to convert some
            # of them to a different type.
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = tokens[1]
            if event_type == 'DriverRequest':
                driver_id = tokens[2]
                location = tokens[3]
                speed = int(tokens[4])
                driver = Driver(driver_id,deserialize_location(location), speed)
            elif event_type == 'RiderRequest':
                rider_id = tokens[2]
                origin = tokens[3]
                destination = tokens[4]
                patience = int(tokens[5])
                rider = Rider(rider_id, deserialize_location(origin),
                              deserialize_location(destination), WAITING,
                              patience)



            # HINT: Use Location.deserialize to convert the location string to
            # a location.

            if event_type == "DriverRequest":
                # TODO
                # Create a DriverRequest event.
                event = DriverRequest(timestamp, driver)
            elif event_type == "RiderRequest":
                # TODO
                # Create a RiderRequest event.
                event = RiderRequest(timestamp, rider)

            events.append(event)

    return events
