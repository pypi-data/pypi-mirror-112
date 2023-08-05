import cv2
from cartesio.model.function import FunctionNode
from cania_utils.image import BINARY_FILL_COLOR


class Threshold(FunctionNode):
    def __init__(self):
        super(Threshold, self).__init__('threshold', 1, 2)

    def __call__(self, connections, parameters):
        if parameters[0] > 127:
            return cv2.threshold(connections[0], parameters[1], BINARY_FILL_COLOR, cv2.THRESH_BINARY)[1]
        return cv2.threshold(connections[0], parameters[1], BINARY_FILL_COLOR, cv2.THRESH_TOZERO)[1]


class ThresholdAt1(FunctionNode):
    def __init__(self):
        super(ThresholdAt1, self).__init__('threshold_at_1', 1, 1)

    def __call__(self, connections, parameters):
        if parameters[0] > 127:
            return cv2.threshold(connections[0], 1, BINARY_FILL_COLOR, cv2.THRESH_BINARY)[1]
        return cv2.threshold(connections[0], 1, BINARY_FILL_COLOR, cv2.THRESH_TOZERO)[1]


class DistanceTransform(FunctionNode):
    def __init__(self):
        super(DistanceTransform, self).__init__('distance_transform', 1, 1)

    def __call__(self, connections, parameters):
        return cv2.normalize(cv2.distanceTransform(connections[0].copy(), cv2.DIST_L2, 3), None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)


class DistanceTransformAndThresh(FunctionNode):
    def __init__(self):
        super(DistanceTransformAndThresh, self).__init__('distance_transform_and_thresh', 1, 2)

    def __call__(self, connections, parameters):
        d = cv2.normalize(cv2.distanceTransform(connections[0].copy(), cv2.DIST_L2, 3), None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        return cv2.threshold(d, parameters[0], BINARY_FILL_COLOR, cv2.THRESH_BINARY)[1]


class BinaryInRange(FunctionNode):
    def __init__(self):
        super(BinaryInRange, self).__init__('inrange_bin', 1, 2)

    def __call__(self, connections, parameters):
        lower = int(min(parameters[0], parameters[1]))
        upper = int(max(parameters[0], parameters[1]))
        return cv2.inRange(connections[0], lower, upper)


class InRange(FunctionNode):
    def __init__(self):
        super(InRange, self).__init__('inrange', 1, 2)

    def __call__(self, connections, parameters):
        lower = int(min(parameters[0], parameters[1]))
        upper = int(max(parameters[0], parameters[1]))
        return cv2.bitwise_and(connections[0], connections[0], mask=cv2.inRange(connections[0], lower, upper))