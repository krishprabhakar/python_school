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
        """
        # TODO
        return "row: {} column:{}".format(self.row, self.column)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @rtype: bool
        """
        # TODO
        return type(self) == type(other) and(self.row, self.column
                                             == other.row, other.column)


def manhattan_distance(origin, destination):
    """Return the Manhattan distance between the origin and the destination.

    @type origin: Location
    @type destination: Location
    @rtype: int
    """
    # TODO
    # 8,6
    distance = abs(destination.y - origin.y) + abs(destination.x - origin.x)
    return distance


def deserialize_location(location_str):
    """Deserialize a location.

    @type location_str: str
        A location in the format 'row,col'
    @rtype: Location
    """
    # TODO
    location_list = []
    for char in location_str:
        location_list.append(char)

    row = int(location_list[0])
    column = int(location_list[2])

    return Location(row, column)
