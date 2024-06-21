from jmetal.core.observer import Observer
from tqdm import tqdm


class ProgressBarCycleObserver(Observer):

    def __init__(self, max: int) -> None:
        """ Show a smart progress meter with the number of evaluations and computing time.

        :param max: Number of expected iterations.
        """
        self.progress_bar = None
        self.progress = 0
        self._max = max
        self

    def update(self, *args, **kwargs):
        if not self.progress_bar:
            self.progress_bar = tqdm(total=self._max, ascii=True, desc='Progress')

        iterations = kwargs['ITERATIONS']
        self.progress_bar.update(iterations)
        self.progress +=iterations

        if self.progress >= self._max:
            self.progress_bar.close()