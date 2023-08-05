import numpy as np
from abc import ABC, abstractmethod
from sklearn.metrics import jaccard_score, recall_score
from scipy.optimize import linear_sum_assignment


class MetricABC(ABC):
    @abstractmethod
    def compute(self, y_true: np.ndarray, y_pred: np.ndarray):
        pass


class MetricCellpose(MetricABC):
    '''
    from MouseLand/cellpose:
    https://github.com/MouseLand/cellpose/blob/5cc03de9c2aa342d4b4469ff476ca04541b63414/cellpose/metrics.py
    '''
    def compute(self, label, pred):
        return self.aggregated_jaccard_index(label, pred)

    def aggregated_jaccard_index(self, masks_true, masks_pred):
        """ AJI = intersection of all matched masks / union of all masks

        Parameters
        ------------

        masks_true: list of ND-arrays (int) or ND-array (int) 
            where 0=NO masks; 1,2... are mask labels
        masks_pred: list of ND-arrays (int) or ND-array (int) 
            ND-array (int) where 0=NO masks; 1,2... are mask labels
        Returns
        ------------
        aji : aggregated jaccard index for each set of masks
        """

        aji = np.zeros(len(masks_true))
        for n in range(len(masks_true)):
            iout, preds = self.mask_ious(masks_true[n], masks_pred[n])
            inds = np.arange(0, masks_true[n].max(), 1, int)
            overlap = self._label_overlap(masks_true[n], masks_pred[n])
            union = np.logical_or(masks_true[n] > 0, masks_pred[n] > 0).sum()
            overlap = overlap[inds[preds > 0]+1, preds[preds > 0].astype(int)]
            aji[n] = overlap.sum() / union
        return aji

    def _label_overlap(self, x, y):
        """ fast function to get pixel overlaps between masks in x and y 

        Parameters
        ------------
        x: ND-array, int
            where 0=NO masks; 1,2... are mask labels
        y: ND-array, int
            where 0=NO masks; 1,2... are mask labels
        Returns
        ------------
        overlap: ND-array, int
            matrix of pixel overlaps of size [x.max()+1, y.max()+1]

        """
        x = x.ravel()
        y = y.ravel()
        overlap = np.zeros((1+x.max(), 1+y.max()), dtype=np.uint)
        for i in range(len(x)):
            overlap[x[i], y[i]] += 1
        return overlap

    def mask_ious(self, masks_true, masks_pred):
        """ return best-matched masks """
        iou = self._intersection_over_union(masks_true, masks_pred)[1:, 1:]
        n_min = min(iou.shape[0], iou.shape[1])
        costs = -(iou >= 0.5).astype(float) - iou / (2*n_min)
        true_ind, pred_ind = linear_sum_assignment(costs)
        iout = np.zeros(masks_true.max())
        iout[true_ind] = iou[true_ind, pred_ind]
        preds = np.zeros(masks_true.max(), 'int')
        preds[true_ind] = pred_ind+1
        return iout, preds

    def _intersection_over_union(self, masks_true, masks_pred):
        """ intersection over union of all mask pairs

        Parameters
        ------------

        masks_true: ND-array, int 
            ground truth masks, where 0=NO masks; 1,2... are mask labels
        masks_pred: ND-array, int
            predicted masks, where 0=NO masks; 1,2... are mask labels
        Returns
        ------------
        iou: ND-array, float
            matrix of IOU pairs of size [x.max()+1, y.max()+1]
        """
        overlap = self._label_overlap(masks_true, masks_pred)
        n_pixels_pred = np.sum(overlap, axis=0, keepdims=True)
        n_pixels_true = np.sum(overlap, axis=1, keepdims=True)
        iou = overlap / (n_pixels_pred + n_pixels_true - overlap)
        iou[np.isnan(iou)] = 0.0
        return iou

    def average_precision(self, masks_true, masks_pred, threshold=[0.5, 0.75, 0.9]):
        """ average precision estimation: AP = TP / (TP + FP + FN)
        This function is based heavily on the *fast* stardist matching functions
        (https://github.com/mpicbg-csbd/stardist/blob/master/stardist/matching.py)
        Parameters
        ------------

        masks_true: list of ND-arrays (int) or ND-array (int) 
            where 0=NO masks; 1,2... are mask labels
        masks_pred: list of ND-arrays (int) or ND-array (int) 
            ND-array (int) where 0=NO masks; 1,2... are mask labels
        Returns
        ------------
        ap: array [len(masks_true) x len(threshold)]
            average precision at thresholds
        tp: array [len(masks_true) x len(threshold)]
            number of true positives at thresholds
        fp: array [len(masks_true) x len(threshold)]
            number of false positives at thresholds
        fn: array [len(masks_true) x len(threshold)]
            number of false negatives at thresholds
        """
        not_list = False
        if not isinstance(masks_true, list):
            masks_true = [masks_true]
            masks_pred = [masks_pred]
            not_list = True
        if not isinstance(threshold, list) and not isinstance(threshold, np.ndarray):
            threshold = [threshold]
        ap = np.zeros((len(masks_true), len(threshold)), np.float32)
        tp = np.zeros((len(masks_true), len(threshold)), np.float32)
        fp = np.zeros((len(masks_true), len(threshold)), np.float32)
        fn = np.zeros((len(masks_true), len(threshold)), np.float32)
        n_true = np.array(list(map(np.max, masks_true)))
        n_pred = np.array(list(map(np.max, masks_pred)))
        for n in range(len(masks_true)):
            #  _,mt = np.reshape(np.unique(masks_true[n], return_index=True), masks_pred[n].shape)
            if n_pred[n] > 0:
                iou = self._intersection_over_union(masks_true[n], masks_pred[n])[1:, 1:]
                for k, th in enumerate(threshold):
                    tp[n, k] = self._true_positive(iou, th)
            fp[n] = n_pred[n] - tp[n]
            fn[n] = n_true[n] - tp[n]
            ap[n] = tp[n] / (tp[n] + fp[n] + fn[n])

        if not_list:
            ap, tp, fp, fn = ap[0], tp[0], fp[0], fn[0]
        return ap, tp, fp, fn

    def _true_positive(self, iou, th):
        """ true positive at threshold th

        Parameters
        ------------
        iou: float, ND-array
            array of IOU pairs
        th: float
            threshold on IOU for positive label
        Returns
        ------------
        tp: float
            number of true positives at threshold
        """
        n_min = min(iou.shape[0], iou.shape[1])
        costs = -(iou >= th).astype(float) - iou / (2*n_min)
        true_ind, pred_ind = linear_sum_assignment(costs)
        match_ok = iou[true_ind, pred_ind] >= th
        tp = match_ok.sum()
        return tp


class MetricIOU(MetricABC):
    def compute(self, y_true: np.ndarray, y_pred: np.ndarray):
        y_pred[y_pred > 0] = 1
        if np.sum(y_true) == 0:
            y_true = 1 - y_true
            y_pred = 1 - y_pred
        intersection = np.logical_and(y_true, y_pred)
        union = np.logical_or(y_true, y_pred)
        iou_score = np.sum(intersection) / np.sum(union)
        return iou_score


class MetricJaccard(MetricABC):
    def compute(self, y_true: np.ndarray, y_pred: np.ndarray):
        return jaccard_score(label, pred, average='macro')


class MetricPrecision(MetricABC):
    def compute(self, y_true: np.ndarray, y_pred: np.ndarray):
        y_pred[y_pred > 0] = 1
        pred_1 = y_pred == 1
        pred_0 = y_pred == 0
        label_1 = y_true == 1
        label_0 = y_true == 0

        TP = (pred_1 & label_1).sum()
        FP = (pred_1 & label_0).sum()
        FN = (pred_0 & label_0).sum()

        if TP == 0 and FP == 0 and FN == 0:
            precision = 1.
        elif TP == 0 and (FP > 0 or FN > 0):
            precision = 0.
        else:
            precision = TP / (TP+FP)

        return precision


class MetricRecall(MetricABC):
    def compute(self, y_true: np.ndarray, y_pred: np.ndarray):
        return recall_score(label, pred, average='micro')


class MetricCount(MetricABC):
    def compute(self, y_true: np.ndarray, y_pred: np.ndarray):
        if y_true == 0 and y_pred != 0:
            return 1.
        if y_true == 0 and y_pred == 0:
            return 0.
        if y_pred == 0 and y_true != 0:
            return 1.

        diff_count = abs(y_true - y_pred)
        diff_count = min(y_true, diff_count) / y_true
        return diff_count
