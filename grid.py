class Grid:

    def __init__(self, size: int, values: list):

        if size <= 0:
            raise ValueError("Size of the grid must be greater than 0")

        if not values or not isinstance(list, values) or len(values) == 0:
            raise ValueError("Values of the grid must be a non-empty list")

        if len(values) != size * size:
            raise ValueError("Size of the grid does not correspond with the size provided")

        self._size = size
        self._values = values

    @property.getter
    def size(self):
        return self._size

    @property.getter
    def values(self):
        return self._values
