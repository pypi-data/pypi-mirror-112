import math
import numpy as np

# from glmnet import ElasticNet, LogitNet

import pandas as pd
from abc import ABC, abstractmethod
from cartesio.model.metric import MetricIOU, MetricPrecision, MetricCount


class FitnessABC(ABC):
    def evaluate(self, y_true, y_pred):
        return [self._evaluate_one(y_true, individual_pred) for individual_pred in y_pred]

    def _evaluate_one(self, y_true, y_pred):
        fitnesses = []
        for i in range(len(y_true)):
            fitnesses.append(self._fitness(y_true[i][0].copy(), y_pred[i][0].copy()))
        return np.mean(np.array(fitnesses))

    @abstractmethod
    def _fitness(self, y_true, y_pred):
        pass


class FitnessAP05(FitnessABC):
    def __init__(self):
        self.AP05 = MetricCellpose()

    def evaluate_one_individual(self, y_true, y_pred):
        y_true_labels = [y[0] for y in y_true]
        y_pred_labels = [y[3] for y in y_pred]
        ap, _, _, _ = self._fitness(y_true_labels, y_pred_labels)
        return 1. - np.mean(np.array(ap))

    def _fitness(self, y_true, y_pred):
        return self.AP05.average_precision(y_true, y_pred, threshold=[0.5])


class FitnessWithCount(FitnessABC, ABC):
    def __init__(self):
        self.count_metric = MetricCount()

    def _evaluate_one(self, y_true, y_pred):
        fitnesses = []
        for i in range(len(y_true)):
            fitnesses.append(self._fitness(y_true[i], y_pred[i]))
        return np.mean(np.array(fitnesses))


class FitnessMSE(FitnessABC):
    def _fitness(self, y_true, y_pred):
        return math.sqrt(np.mean(np.square(y_true - y_pred)))


class FitnessIOU(FitnessABC):
    def __init__(self):
        super(FitnessIOU, self).__init__()
        self.iou_metric = MetricIOU()

    def _fitness(self, y_true, y_pred):
        return 1. - self.iou_metric.compute(y_true, y_pred)


class FitnessCount(FitnessWithCount):
    def __init__(self):
        super(FitnessCount, self).__init__()
        self.precision_metric = MetricIOU()

    def _fitness(self, y_true, y_pred):
        mask_true, count_true = y_true
        count = self.count_metric.compute(count_true, y_pred['count'])
        precision = 1 - self.precision_metric.compute(mask_true, y_pred['mask'])
        score = count + precision
        return score


class FitnessCountAndIOU(FitnessWithCount):
    def __init__(self):
        super(FitnessCountAndIOU, self).__init__()
        self.iou_metric = MetricIOU()
        self.precision_metric = MetricPrecision()

    def _fitness(self, y_true, y_pred):
        mask_true, count_true = y_true
        mask_pred, count_pred, seeds = y_pred
        iou = 1 - self.iou_metric.compute(mask_true, mask_pred)
        count = self.count_metric.compute(count_true, count_pred)
        precision = 1 - self.precision_metric.compute(mask_true, seeds)
        score = iou + count + precision
        return score


class FitnessEllipse(FitnessCountAndIOU):
    def __init__(self, min_axis, max_axis):
        super(FitnessEllipse, self).__init__(EndpointEllipse(min_axis, max_axis))


class FitnessElasticNet(FitnessABC):
    def __init__(self):
        super(FitnessElasticNet, self).__init__()
        self.model = LogitNet(n_splits=0)

    def mask_to_features(self, mask, seeds):
        mask_pred, seeds, n_seeds, labels = self.watershed(mask.copy(), seeds.copy())
        count = 0
        for l in labels:
            count += np.count_nonzero(l)
        return count

    def _fitness(self, y_true, y_pred):
        mask_pred, seeds = y_pred
        if not mask_pred.any() or mask_pred.all() or np.count_nonzero(mask_pred) == 0:
            feature = 0
        else:
            feature = self.mask_to_features(mask_pred, seeds)
        return feature

    def evaluate_one_individual(self, y_true, y_pred):
        features = []
        for one_y_true, one_y_pred in zip(y_true, y_pred):
            features.append(self._fitness(one_y_true.copy(), one_y_pred))
        x = pd.Series(features)
        y = pd.Series(np.array(y_true).flatten())

        score = x.corr(y)

        if score == 0:
            return 0
        if score > 0.:
            return 1 - score

        return 2 - score

        '''
        try:
            self.model.fit(x, y)
            new_pred = self.model.predict(x)
            print(new_pred)
            score = y_true - new_pred
        except ValueError:
            score = 10.
        except IndexError:
            score = 10.
        
        '''
