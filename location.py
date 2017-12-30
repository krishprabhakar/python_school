import math


class Location:
    def __init__(self, row, column):
        """Initialize a location.

        @type self: Location
        @type row: int
        @type column: int
        @rtype: None
        """
        # TODO
        self.row, self.column = row, column

    def __str__(self):
        """Return a string representation.
        @type: str
        @rtype: str

        >>> origin = Location(5, 6)
        >>> print(origin)
        5,6
        """
        # TODO
        return "{},{}".format(self.row, self.column)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @rtype: bool

        >>> origin = Location(5, 6)
        >>> destination = Location(5, 7)
        >>> origin == destination
        False
        """
        # TODO
        return (type(self) == type(other) and
                self.row == other.row and
                self.column == other.column)


def manhattan_distance(p1, p2):
    """Return the Manhattan distance between the origin and the destination.

    @type origin: Location
    @type destination: Location
    @rtype: int

    >>> origin = Location(5, 3)
    >>> destination = Location(5, 6)
    >>> manhattan_distance(origin, destination)
    3
    >>> alpha = Location(13,7)
    >>> manhattan_distance(origin, alpha)
    12
    """
    # TODO
    # 8,6
    distance = (abs(p1.column - p2.column) +
                abs(p1.row - p2.row))
    return distance


def deserialize_location(location_str):
    """Deserialize a location.

    @type location_str: str
        A location in the format 'row,col'
    @rtype: Location

    >>> loc_str = '5,7'
    >>> compare = Location(5,7)
    >>> comp = deserialize_location(loc_str)
    >>> comp == compare
    True
    """
    # TODO
    location_list = []
    for char in location_str:
        location_list.append(char)

    row = int(location_list[0])
    column = int(location_list[2])

    return Location(row, column)
