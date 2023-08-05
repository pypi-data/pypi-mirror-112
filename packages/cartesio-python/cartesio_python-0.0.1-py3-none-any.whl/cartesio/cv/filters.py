import cv2
import numpy as np

from cartesio.model.function import FunctionNode
from cartesio.cv.kernels import correct_ksize, SHARPEN_KERNEL


class MedianBlur(FunctionNode):
    def __init__(self):
        super(MedianBlur, self).__init__('median_blur', 1, 1)

    def __call__(self, connections, parameters):
        ksize = correct_ksize(parameters[0])
        return cv2.medianBlur(connections[0], ksize)


class GaussianBlur(FunctionNode):
    def __init__(self):
        super(GaussianBlur, self).__init__('gaussian_blur', 1, 1)

    def __call__(self, connections, parameters):
        ksize = correct_ksize(parameters[0])
        return cv2.GaussianBlur(connections[0], (ksize, ksize), 0)


class Laplacian(FunctionNode):
    def __init__(self):
        super(Laplacian, self).__init__('laplacian', 1, 0)

    def __call__(self, connections, parameters):
        return cv2.Laplacian(connections[0], cv2.CV_64F).astype(np.uint8)


class SobelX(FunctionNode):
    def __init__(self):
        super(SobelX, self).__init__('sobel_x', 1, 1)

    def __call__(self, connections, parameters):
        ksize = correct_ksize(parameters[0])
        return cv2.Sobel(connections[0], cv2.CV_64F, 1, 0, ksize=ksize).astype(np.uint8)


class SobelY(FunctionNode):
    def __init__(self):
        super(SobelY, self).__init__('sobel_y', 1, 1)

    def __call__(self, connections, parameters):
        ksize = correct_ksize(parameters[0])
        return cv2.Sobel(connections[0], cv2.CV_64F, 0, 1, ksize=ksize).astype(np.uint8)


class Canny(FunctionNode):
    def __init__(self):
        super(Canny, self).__init__('canny', 1, 2)

    def __call__(self, connections, parameters):
        return cv2.Canny(connections[0], parameters[0], parameters[1])


class Sharpen(FunctionNode):
    def __init__(self):
        super(Sharpen, self).__init__('sharpen', 1, 0)

    def __call__(self, connections, parameters):
        return cv2.filter2D(connections[0], -1, SHARPEN_KERNEL)
