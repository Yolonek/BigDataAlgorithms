import numpy as np
import itertools
import functools
import numba
from time import time


class BinsNotEmpty(object):

    def __init__(self, num_of_bins=0, num_of_trials=0):
        self.bins = num_of_bins
        self.trials = num_of_trials
        self.trials_array = None

    def change_bins(self, num_of_bins):
        self.bins = num_of_bins

    def change_trials(self, num_of_trials):
        self.trials = num_of_trials

    def simulate_bins_and_balls_1(self):
        histogram_data = {bin_: 0 for bin_ in range(1, self.bins + 1)}
        upper_bound = self.bins + 1
        while 0 in histogram_data.values():
            histogram_data[np.random.randint(1, upper_bound)] += 1
        return np.array(list(histogram_data.values())).sum()

    def simulate_bins_and_balls_2(self, _):
        occurrences = set()
        counter = 0
        upper_bound = self.bins + 1
        while len(occurrences) < self.bins:
            occurrences.add(np.random.randint(1, upper_bound))
            counter += 1
        return counter

    def simulate_bins_and_balls_3(self):
        occurrences = set()
        upper_bound = self.bins + 1
        for counter in itertools.count(start=1, step=1):
            occurrences.add(np.random.randint(1, upper_bound))
            if len(occurrences) == self.bins:
                return counter

    def repeat_experiments_1(self):
        return np.fromiter((self.simulate_bins_and_balls_3() for _ in range(self.trials)), int)

    def repeat_experiments_2(self):
        return np.array(list(map(self.simulate_bins_and_balls_2, np.zeros(self.trials))))

    def repeat_experiments_3(self):
        results = np.zeros(self.trials)
        for i in range(self.trials):
            results[i] = self.simulate_bins_and_balls_3()
        return results


if __name__ == '__main__':
    bins = 1000
    trials = 20
    biba = BinsNotEmpty(num_of_bins=bins,
                        num_of_trials=trials)
    # print(biba.simulate_bins_and_balls_2())

    time_1 = time()
    res1 = biba.repeat_experiments_1()
    time_2 = time()
    print(res1, time_2-time_1)

    time_1 = time()
    res2 = biba.repeat_experiments_2()
    time_2 = time()
    print(res2, time_2 - time_1)

    time_1 = time()
    res3 = biba.repeat_experiments_3()
    time_2 = time()
    print(res3, time_2 - time_1)