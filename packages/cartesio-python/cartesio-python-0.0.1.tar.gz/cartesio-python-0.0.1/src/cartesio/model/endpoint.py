
from abc import ABC, abstractmethod
from typing import List

import cv2
import numpy as np
from skimage.segmentation import watershed
from cania_utils.image import imnew, contours, BINARY_FILL_COLOR


class EndpointABC(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, entries: List):
        pass
    '''
    @classmethod
    def from_json(cls, json_data):
        if json_data == 'W':
            return EndpointWatershed()
        if json_data == 'L':
            return EndpointMaskToLabels()
        if json_data == 'C':
            return EndpointCounting()
    '''


class EndpointOptimizer(ABC):
    def __init__(self, endpoint: EndpointABC):
        self.endpoint = endpoint

    @abstractmethod
    def optimize(self):
        pass


class EndpointEllipse(EndpointABC):
    def __init__(self, min_axis, max_axis):
        self.min_axis = min_axis
        self.max_axis = max_axis

    def execute(self, entries):
        mask = entries[0]
        n = 0
        new_mask = imnew(mask.shape)
        new_seeds = imnew(mask.shape)
        labels = []

        contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if len(cnt) >= 5:
                (x, y), (MA, ma), angle = cv2.fitEllipse(cnt)
                if self.min_axis <= MA <= self.max_axis and self.min_axis <= ma <= self.max_axis:
                    cv2.ellipse(new_mask, ((x, y), (MA, ma), angle), BINARY_FILL_COLOR, thickness=-1)
                    cv2.ellipse(new_seeds, ((x, y), (3, 3), angle), BINARY_FILL_COLOR, thickness=-1)
                    labels.append(((x, y), (MA, ma), angle))
                    n += 1

        return new_mask, new_seeds, n, labels


class EndpointCounting(EndpointABC):
    def __init__(self):
        super().__init__('C')

    def execute(self, entries):
        cnts = contours(entries[0])
        output = {'mask': entries[0], 'count': len(cnts)}
        return output


class EndpointMaskToLabels(EndpointABC):
    def __init__(self):
        super().__init__('L')

    def execute(self, entries):
        mask_pred = entries[0]
        ret, labels = cv2.connectedComponents(mask_pred)
        return mask_pred, None, len(np.unique(labels)) - 1, labels


class EndpointRescale(EndpointABC):
    def __init__(self, scale_factor):
        super().__init__('R')
        self.scale_factor = 1. / scale_factor

    def execute(self, entries):
        mask_pred = cv2.resize(entries[0], None, fx=self.scale_factor, fy=self.scale_factor, interpolation=cv2.INTER_CUBIC)
        return mask_pred, mask_pred, mask_pred, mask_pred


class EndpointWatershed(EndpointABC):
    def __init__(self, watershed_line=True, use_centroids=False):
        super().__init__('W')
        self.watershed_line = watershed_line
        self.use_centroids = use_centroids

    def execute(self, entries):
        mask = entries[0]
        markers = entries[1]

        if self.use_centroids:
            output = cv2.connectedComponentsWithStats(markers, connectivity=8)
            markers = np.zeros(markers.shape)
            for i in range(output[0]):
                x = int(round(output[3][i, 0]))
                y = int(round(output[3][i, 1]))
                markers[y, x] = i
        else:
            _, markers = cv2.connectedComponents(markers, connectivity=8)

        labels = watershed(-mask, markers=markers, mask=mask, watershed_line=self.watershed_line)
        output = {
            'mask': mask,
            'markers': markers,
            'count': len(np.unique(labels)) - 1,
            'labels': labels
        }
        return output


class EndpointHoughCircle(EndpointABC):
    def __init__(self, min_distance, min_radius, max_radius):
        self.min_distance = min_distance
        self.p1 = 1
        self.p2 = 12
        self.min_radius = min_radius
        self.max_radius = max_radius

    def execute(self, entries):
        mask_pred = entries[0]
        new_mask = imnew(mask_pred.shape)
        new_seeds = imnew(mask_pred.shape)

        circles = cv2.HoughCircles(mask_pred, cv2.HOUGH_GRADIENT, 1, self.min_distance, param1=self.p1, param2=self.p2, minRadius=self.min_radius, maxRadius=self.max_radius)
        if circles is None:
            # return empty image (mask and seeds) and 0 cells
            return new_mask, new_seeds, 0, None

        circles = np.uint16(np.around(circles))

        n_seeds = len(circles[0])

        for i in range(n_seeds):
            cv2.circle(new_seeds, (circles[0, i][0], circles[0, i][1]), 3, i, -1)
            cv2.circle(new_mask, (circles[0, i][0], circles[0, i][1]), circles[0, i][2], BINARY_FILL_COLOR, -1)

        return new_mask, new_seeds, n_seeds, None


'''

class FitnessElasticNet(FitnessWatershed):
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
