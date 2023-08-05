from cartesio.model.metric import Metric
import numpy as np
from numba import njit
import time


class MetricIOU(Metric):
    def compute(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        return self.__iou(y_true, y_pred)

    def __iou(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        if not np.any(y_true):
            y_true = 1 - y_true
            y_pred = 1 - y_pred
        intersection = np.logical_and(y_true, y_pred)
        union = np.logical_or(y_true, y_pred)
        iou_score = np.sum(intersection) / np.sum(union)
        return iou_score


# short-circuiting replacement for np.any()
@njit()
def _fast_any(array: np.ndarray) -> bool:
    for x in array.flat:
        if x:
            return True
    return False


@njit()
def _fast_iou(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    intersection = 0
    union = 0
    y_true_flat = y_true.flat
    y_pred_flat = y_pred.flat

    if _fast_any(y_true):
        for i in range(len(y_true_flat)):
            intersection += y_true_flat[i] * y_pred_flat[i]
            if y_true_flat[i] or y_pred_flat[i]:
                union += 1
    else:
        for i in range(len(y_true_flat)):
            y_true_flat[i] = 1 - y_true_flat[i]
            y_pred_flat[i] = 1 - y_pred_flat[i]
            intersection += y_true_flat[i] * y_pred_flat[i]
            if y_true_flat[i] or y_pred_flat[i]:
                union += 1
    return intersection / union


class MetricFastIOU(Metric):
    def compute(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        return _fast_iou(y_true, y_pred)


def main():
    ''' create metrics '''
    metric_iou = MetricIOU()
    metric_fast_iou = MetricFastIOU()

    ''' create y_true, y_pred, random binary matrices '''
    y_true = np.random.randint(2, size=(224, 224))
    y_pred = np.random.randint(2, size=(224, 224))

    ''' call standard iou '''
    t0 = time.time()
    iou = metric_iou.compute(y_true, y_pred)
    print(iou)
    t1 = time.time()-t0

    ''' call fast iou, first time is compilation '''
    fast_iou = metric_fast_iou.compute(y_true, y_pred)
    print(fast_iou)

    ''' call fast iou, compiled version '''
    t0 = time.time()
    fast_iou = metric_fast_iou.compute(y_true, y_pred)
    print(fast_iou)
    t2 = time.time()-t0

    print()
    print(f'{t1/t2:.2f} times faster')


if __name__ == "__main__":
    main()
