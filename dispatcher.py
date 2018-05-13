from driver import Driver
from rider import Rider
from location import Location


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    """

    def __init__(self):
        """Initialize a Dispatcher.

        @type self: Dispatcher
        @rtype: None
        """
        # TODO
        self.waiting_list = []
        self.driver_list = []
        # self.rider_list = []

    def __str__(self):
        """Return a string representation.

        @type self: Dispatcher
        @rtype: str
        """
        # TODO
        return ("waiting list of riders: {} \n driver registered list {}".
                format(self.waiting_list, self.driver_list))

    def request_driver(self, rider):
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: Driver | None

        >>> dis = Dispatcher()
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
        >>> print(dis2.request_rider(fire))
        None
        >>> dis2.request_rider(inferno)
        >>> print(dis2.request_driver(kal))
        identifier:fire, location:(5,5), speed:5 idle status:True destination:(None)

        """
        # TODO
        # checks the dictionary to see if there is an available driver
        driver = None

        for driver_registered in self.driver_list:
            if not driver_registered.rider and driver_registered.is_idle:
                # check for if this is the first person assigned
                if driver is None:
                    driver = driver_registered
                elif driver_registered.get_travel_time(rider.origin) < driver.get_travel_time(rider.origin):
                    driver = driver_registered

        if driver is None:
            self.waiting_list.append(rider)
        else:
            return driver

    def request_rider(self, driver):
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        @type self: Dispatcher
        @type driver: Driver
        @rtype: Rider | None

        >>> dis = Dispatcher()
        >>> origin = Location(5,2)
        >>> destination = Location(3,2)
        >>> origin2 = Location(5,6)
        >>> fire = Driver("fire", origin2, 5)
        >>> kal = Rider("kal", origin, destination, 5, 3)
        >>> dis2 = Dispatcher()
        >>> dis.request_driver(kal)
        >>> print(dis2.request_rider(fire))
        None
        >>> print(dis2.driver_list[0])
        identifier:fire, location:(5,6), speed:5 idle status:True destination:(None)
        >>> print(dis.request_rider(fire))
        unique_identifier: kal , origin: (5,2), destination: (3,2), patience: 5, status: waiting, timestamp: 3

        """
        # TODO
        # check if the driver is in the driver_dict
        if driver not in self.driver_list:
            self.driver_list.append(driver)


        if len(self.waiting_list) == 0:
            return None
        else:
            # this line will work but just to be safe im adding the loop
            # return self.waiting_list[0]
            rider = self.waiting_list[0]
            #this code returns the closest rider to the driver, but the assignment asks for the longest waiting
            #i.e the highest priority in the waiting list so I'll comment this bit out
            # for riders in self.waiting_list:
            #     if rider.timestamp < riders:
            #         rider = riders
            return rider

    def cancel_ride(self, rider):
        """Cancel the ride for rider.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: None

        >>> dis = Dispatcher()
        >>> origin = Location(5,2)
        >>> destination = Location(3,2)
        >>> kal = Rider("kal", origin, destination, 5, 3)
        >>> print(kal)
        unique_identifier: kal , origin: (5,2), destination: (3,2), patience: 5, status: waiting, timestamp: 3
        >>> dis.request_driver(kal)
        >>> dis.cancel_ride(kal)
        >>> print(kal)
        unique_identifier: kal , origin: (5,2), destination: (3,2), patience: 5, status: cancelled, timestamp: 3
        >>> print(dis.waiting_list)
        []
        """
        # TODO
        self.waiting_list.remove(rider)
        rider.cancel()
