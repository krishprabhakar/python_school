from location import Location

"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
@type WAITING: str
    A constant used for the waiting rider status.
@type CANCELLED: str
    A constant used for the cancelled rider status.
@type SATISFIED: str
    A constant used for the satisfied rider status
"""

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:

    def __init__(self, unique_identifier, origin, destination, patience):
        """
        Initializes a rider

        @type self: Rider
        @type unique_identifier: str
        @type origin: Location
        @type destination: Location
        @type patience: int
        @rtype: None
        """
        self.id, self.origin, = unique_identifier, origin
        self.destination, self.patience = destination, patience
        self.status = WAITING

    def __str__(self):
        """
        Returns a user-friendly string representation of Rider self

        @type self : Rider
        @return: str

        >>> origin = Location(5,2)
        >>> destination = Location(3,2)
        >>> kal = Rider("kal", origin, destination, 5)
        >>> print(kal)
        unique_identifier: kal , origin: (5,2), destination: (3,2), patience: 5, status: waiting
        """
        return "unique_identifier: {} , origin: ({}), destination: ({}), " \
               "patience: {}, status: {}".format(self.id, self.origin,
                                                  self.destination,
                                                  self.patience, self.status)
    def cancel(self):
        """
        Sets the status of the rider to cancelled

        @type self : Rider
        @return: None

        >>> origin = Location(5,2)
        >>> destination = Location(3,2)
        >>> kal = Rider("kal", origin, destination, 5)
        >>> print(kal)
        unique_identifier: kal , origin: (5,2), destination: (3,2), patience: 5, status: waiting
        >>> kal.cancel()
        >>> print(kal)
        unique_identifier: kal , origin: (5,2), destination: (3,2), patience: 5, status: cancelled
        """
        self.status = CANCELLED

    def wait(self):
        """
        Sets the status of the rider to waiting

        @type self : Rider
        @return: None

        >>> origin = Location(5,2)
        >>> destination = Location(3,2)
        >>> kal = Rider("kal", origin, destination, 5)
        >>> print(kal)
        unique_identifier: kal , origin: (5,2), destination: (3,2), patience: 5, status: waiting
        >>> kal.cancel()
        >>> print(kal)
        unique_identifier: kal , origin: (5,2), destination: (3,2), patience: 5, status: cancelled
        >>> kal.wait()
        >>> print(kal)
        unique_identifier: kal , origin: (5,2), destination: (3,2), patience: 5, status: waiting
        """

        self.status = WAITING

    def satisfied(self):
        """
        Sets the status of the rider to cancelled

        @type self : Rider
        @return: None

        >>> origin = Location(5,2)
        >>> destination = Location(3,2)
        >>> kal = Rider("kal", origin, destination, 5)
        >>> print(kal)
        unique_identifier: kal , origin: (5,2), destination: (3,2), patience: 5, status: waiting
        >>> kal.satisfied()
        >>> print(kal)
        unique_identifier: kal , origin: (5,2), destination: (3,2), patience: 5, status: satisfied
        """

        self.status = SATISFIED


if __name__ == "__main__":

    from location import Location
    origin = Location(5,2)
    destination = Location(3,2)
    x = Rider("kal", origin, destination, 5)
    print(x)
    x.satisfied()
    print(x)

