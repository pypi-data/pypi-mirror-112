import numpy as np


class BaseOneDimensionMethod:
    """Class StandartUniformFunction is one of variants one-dimensions optimization

    Note: It's standard method which don't use numba's compilation

    Attributes
    ----------
    function: def
        Your one-dimension function
    borders: np.array([left search border, right search border])
    count_of_intervals: int
        Diving into count_of_intervals parts of your interval for calculation f(x_i)
    eps: np.float64
        Result error
    count_of_iterations_limit: np.int64
        Limit of deepening iterations

    Methods
    -------
    step()
        Delegate calculations at one interval to compiled by numba code

    predict()
        Calculate min for your task. Returns np.array([argminF(x), f(argminF(x))])

    """

    def __init__(self, function, borders: np.array, eps: np.float64 = 0.1, count_of_iterations_limit: np.int64 = -1):
        self.function = function
        assert borders.shape[0] == 2, "Border shape must have 2 parameters: left border, right border"
        self.start_borders = np.array([float(borders[0]), float(borders[1])])
        self.current_borders = self.start_borders
        assert eps > 0, "Epsilon must be more than zero"
        self.eps = eps
        self.current_min_coords: np.float64 = None
        self.iterations_limit = count_of_iterations_limit
        self.current_iteration = 0

    def _set_borders(self, current_borders: np.array) -> None:

        if current_borders[0] < self.start_borders[0]:
            self.current_borders[0] = self.start_borders[0]
        else:
            self.current_borders[0] = current_borders[0]
        if current_borders[1] > self.start_borders[1]:
            self.current_borders[1] = self.start_borders[1]
        else:
            self.current_borders[1] = current_borders[1]
        return

    def step(self):
        """
        Delegate calculations at one interval to compiled by numba code
        :return: None
        """
        pass
    def _is_not_ended_increase_current_iteration(self) -> bool:
        self.current_iteration += 1
        if self.current_borders[1] - self.current_borders[0] < self.eps:
            return False
        return self.current_iteration <= self.iterations_limit or self.iterations_limit == -1

    def predict(self) -> np.array:
        """
        Calculate min for your task.

        :return: np.array([argminF(x), f(argminF(x))])
        """

        while self._is_not_ended_increase_current_iteration():
            self.step()
        return self.current_min_coords
