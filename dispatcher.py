from driver import Driver
from rider import Rider


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
        self.driver_dict = {}
        self.rider_list=[]

    def __str__(self):
        """Return a string representation.

        @type self: Dispatcher
        @rtype: str
        """
        # TODO
        pass

    def request_driver(self, rider):
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: Driver | None
        """
        # TODO
        # checks the dictionary to see if there is an available driver
        available_drivers = []
        for driver in self.driver_dict:
            if self.driver_dict[driver] is None:
                available_drivers.append(driver)
        # checks if drivers are available, if not rider is put on waiting list
        if len(available_drivers) == 0:
            self.waiting_list.append(rider)
        else:
            first_driver = available_drivers[0]
            closest_time = first_driver.get_travel_time(rider.origin)
            assigned_driver = first_driver
            for driver in available_drivers:
                if driver.get_travel_time(rider.origin) <= closest_time:
                    assigned_driver = driver
        return assigned_driver

    def request_rider(self, driver):
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        @type self: Dispatcher
        @type driver: Driver
        @rtype: Rider | None
        """
        # TODO
        # check if the driver is in the driver_dict
        if driver not in self.driver_dict:
            self.driver_dict[driver] = None
        if len(self.waiting_list) == 0:
            return None
        else:
            return self.waiting_list[0]

    def cancel_ride(self, rider):
        """Cancel the ride for rider.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: None
        """
        # TODO
        rider._cancel()
