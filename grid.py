class Grid:

    def __init__(self, size: int, values: str, scores: list=None):

        values_parameter = values

        if size <= 0:
            raise ValueError("Size of the grid must be greater than 0")

        if not values or not isinstance(values, str) or len(values) == 0:
            raise ValueError("Values of the grid must be a non-empty list")

        values_list = list(map(int, values.split(',')))

        if len(values_list) != size * size:
            raise ValueError("Size of the grid does not correspond with the size provided")

        self._size = size
        self._values = values
        if scores:
            self._scores = scores
        else:
            self._scores = self._calculate_scores(values_list)

    @property
    def size(self):
        return self._size

    @property
    def values(self):
        return self._values

    @property
    def scores(self):
        return self._scores

    def _calculate_position(self, x: int, y: int) -> int:
        if (x < 0) or (y < 0) or (x >= self._size) or (y >= self._size):
            return -1

        return (y * self._size) + x

    def _calculate_scores(self, values_list: list) -> list:
        scores = []
        for index, value in enumerate(values_list):
            x_position = index // self._size
            y_position = index % self._size

            position_score = 0

            for x_index in range(x_position - 1, x_position + 2):
                if x_index < 0 or x_index >= self._size:
                    continue
                for y_index in range (y_position - 1, y_position + 2):
                    if y_index < 0 or y_index >= self._size:
                        continue
                    current_position = self._calculate_position(y_index, x_index)
                    position_score += values_list[current_position]

            score_dict = dict(x=x_position,
                              y=y_position,
                              score=position_score)

            scores.append(score_dict)

        return scores
