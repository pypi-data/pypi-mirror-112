import cv2
import numpy as np
from skimage.morphology import remove_small_objects, remove_small_holes, thin

from cartesio.model.function import FunctionNode, FunctionNodeWritable
from cartesio.cv.kernels import kernel_from_parameters
from cania_utils.image import imfill


class Erode(FunctionNodeWritable):
    def __init__(self):
        super(Erode, self).__init__('erode', 1, 2)

    def __call__(self, inputs, p):
        kernel = kernel_from_parameters(p)
        return cv2.erode(inputs[0], kernel)

    def to_python(self, input_names, p, output_name):
        return f'{output_name} = cv2.erode({input_names[0]}, kernel_from_parameters({p[0]}))'

    def to_cpp(self, input_names, p, output_name):
        return f'cv::erode({input_names[0]}, {output_name}, kernel_from_parameters({p[0]}));'


class Dilate(FunctionNodeWritable):
    def __init__(self):
        super(Dilate, self).__init__('dilate', 1, 2)

    def __call__(self, inputs, p):
        kernel = kernel_from_parameters(p)
        return cv2.dilate(inputs[0], kernel)

    def to_python(self, input_names, p, output_name):
        return f'{output_name} = cv2.dilate({input_names[0]}, kernel_from_parameters({p[0]}))'

    def to_cpp(self, input_names, p, output_name):
        return f'cv::dilate({input_names[0]}, {output_name}, kernel_from_parameters({p[0]}));'


class Open(FunctionNodeWritable):
    def __init__(self):
        super(Open, self).__init__('open', 1, 2)

    def __call__(self, inputs, p):
        kernel = kernel_from_parameters(p)
        return cv2.morphologyEx(inputs[0], cv2.MORPH_OPEN, kernel)

    def to_python(self, input_names, p, output_name):
        return f'{output_name} = cv2.morphologyEx({input_names[0]}, cv2.MORPH_OPEN, kernel_from_parameters({p[0]}))'

    def to_cpp(self, input_names, p, output_name):
        return f'cv::morphologyEx({input_names[0]}, {output_name}, MORPH_OPEN, kernel_from_parameters({p[0]}));'


class Close(FunctionNodeWritable):
    def __init__(self):
        super(Close, self).__init__('close', 1, 2)

    def __call__(self, inputs, p):
        kernel = kernel_from_parameters(p)
        return cv2.morphologyEx(inputs[0], cv2.MORPH_CLOSE, kernel)

    def to_python(self, input_names, p, output_name):
        return f'{output_name} = cv2.morphologyEx({input_names[0]}, cv2.MORPH_CLOSE, kernel_from_parameters({p[0]}))'

    def to_cpp(self, input_names, p, output_name):
        return f'cv::morphologyEx({input_names[0]}, {output_name}, MORPH_CLOSE, kernel_from_parameters({p[0]}));'


class MorphGradient(FunctionNodeWritable):
    def __init__(self):
        super(MorphGradient, self).__init__('morph_gradient', 1, 2)

    def __call__(self, inputs, p):
        kernel = kernel_from_parameters(p)
        return cv2.morphologyEx(inputs[0], cv2.MORPH_GRADIENT, kernel)

    def to_python(self, input_names, p, output_name):
        return f'{output_name} = cv2.morphologyEx({input_names[0]}, cv2.MORPH_GRADIENT, kernel_from_parameters({p[0]}))'

    def to_cpp(self, input_names, p, output_name):
        return f'cv::morphologyEx({input_names[0]}, {output_name}, MORPH_GRADIENT, kernel_from_parameters({p[0]}));'


class MorphTopHat(FunctionNodeWritable):
    def __init__(self):
        super(MorphTopHat, self).__init__('morph_tophat', 1, 2)

    def __call__(self, inputs, p):
        kernel = kernel_from_parameters(p)
        return cv2.morphologyEx(inputs[0], cv2.MORPH_TOPHAT, kernel)

    def to_python(self, input_names, p, output_name):
        return f'{output_name} = cv2.morphologyEx({input_names[0]}, cv2.MORPH_TOPHAT, kernel_from_parameters({p[0]}))'

    def to_cpp(self, input_names, p, output_name):
        return f'cv::morphologyEx({input_names[0]}, {output_name}, MORPH_TOPHAT, kernel_from_parameters({p[0]}));'


class MorphBlackHat(FunctionNodeWritable):
    def __init__(self):
        super(MorphBlackHat, self).__init__('morph_blackhat', 1, 2)

    def __call__(self, inputs, p):
        kernel = kernel_from_parameters(p)
        return cv2.morphologyEx(inputs[0], cv2.MORPH_BLACKHAT, kernel)

    def to_python(self, input_names, p, output_name):
        return f'{output_name} = cv2.morphologyEx({input_names[0]}, cv2.MORPH_BLACKHAT, kernel_from_parameters({p[0]}))'

    def to_cpp(self, input_names, p, output_name):
        return f'cv::morphologyEx({input_names[0]}, {output_name}, MORPH_BLACKHAT, kernel_from_parameters({p[0]}));'


class FillHoles(FunctionNodeWritable):
    def __init__(self):
        super(FillHoles, self).__init__('fill_holes', 1, 0)

    def __call__(self, inputs, p):
        return imfill(inputs[0])

    def to_python(self, input_names, p, output_name):
        return f'{output_name} = imfill({input_names[0]})'

    def to_cpp(self, input_names, p, output_name):
        return f'imfill({input_names[0]}, {output_name});'


class RemoveSmallObjects(FunctionNode):
    def __init__(self):
        super(RemoveSmallObjects, self).__init__('remove_small_objects', 1, 1)

    def __call__(self, inputs, p):
        return remove_small_objects(inputs[0] > 0, p[0]).astype(np.uint8)


class RemoveSmallHoles(FunctionNode):
    def __init__(self):
        super(RemoveSmallHoles, self).__init__('remove_small_holes', 1, 1)

    def __call__(self, inputs, p):
        return remove_small_holes(inputs[0] > 0, p[0]).astype(np.uint8)


class Thin(FunctionNode):
    def __init__(self):
        super(Thin, self).__init__('thin', 1, 0)

    def __call__(self, inputs, p):
        return thin(inputs[0]).astype(np.uint8)
