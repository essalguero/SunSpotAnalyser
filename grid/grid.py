class Grid:

    def __init__(self, size: int, values: str, scores: list = None):
        """
        Class __init__
        :param size: Grid is a matrix of size * size elements
        :param values: values stored in the grid
        :param scores: list of the calculated scores
        """

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
        """
        Receiving the two coordinates of a grid, calculates the equivalent position in a list
        :param x:
        :param y:
        :return: converted matrix position into list position
        """
        if (x < 0) or (y < 0) or (x >= self._size) or (y >= self._size):
            return -1

        return (y * self._size) + x

    def _calculate_scores(self, values_list: list) -> list:
        """
        Perform the calculation of the score for every position of the grid
        :param values_list: List of integers with the value of every position of the grid
        :return: list of dictionaries containing the position in the grid and the score
        """
        scores = []
        for index, value in enumerate(values_list):
            x_position = index // self._size
            y_position = index % self._size

            position_score = 0

            for x_index in range(x_position - 1, x_position + 2):
                if x_index < 0 or x_index >= self._size:
                    continue
                for y_index in range(y_position - 1, y_position + 2):
                    if y_index < 0 or y_index >= self._size:
                        continue
                    current_position = self._calculate_position(y_index, x_index)
                    position_score += values_list[current_position]

            score_dict = dict(x=x_position,
                              y=y_position,
                              score=position_score)

            scores.append(score_dict)

        return scores

    def _get_scores_sorted(self) -> list:
        """
        Sorts in ascending order of score

        :return: List with the scores of the grid ordered in ascending order
        """
        list_sorted = sorted(self.scores, key=lambda d: d['score'], reverse=True)

        return list_sorted

    def get_biggest_values(self, number_items=0) -> list:
        """
        Method to obtain a number of the scores calculated for the grid, in ascending order

        :param number_items: Number of total 'biggest values' to be returned
        :return: A list ordered by descending scores containing the biggest 'number_items' elements
        """
        if number_items < 0:
            raise ValueError("Size must be greater or equal to 0")

        if number_items > len(self.scores):
            raise ValueError("Size cannot be greater than scores size")

        sorted_scores_list = self._get_scores_sorted()

        if number_items:
            return sorted_scores_list[:number_items]

        return sorted_scores_list

    def get_average_value(self) -> float:
        """
        Calculate average of the scores of the grid

        :return: Average value of the scores
        """
        total_items = len(self._scores)
        value = 0
        for cell in self._scores:
            value += cell['score']

        average = value / total_items
        return average
