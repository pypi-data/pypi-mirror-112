from cartesio.cv.function_set import FunctionSet


class FilterSet(FunctionSet):
    def fill(self):
        self.add_function('median_blur')
        self.add_function('gaussian_blur')
        self.add_function('laplacian')
        self.add_function('sobel_x')
        self.add_function('sobel_y')
        self.add_function('canny')
        self.add_function('sharpen')


class MorphologySet(FunctionSet):
    def fill(self):
        self.add_function('erode')
        self.add_function('dilate')
        self.add_function('open')
        self.add_function('close')
        self.add_function('morph_gradient')
        self.add_function('morph_tophat')
        self.add_function('morph_blackhat')
        self.add_function('fill_holes')
        self.add_function('remove_small_objects')
        self.add_function('remove_small_holes')
        # self.add_function('thin')


class MiscSet(FunctionSet):
    def fill(self):
        self.add_function('distance_transform')
        self.add_function('distance_transform_and_thresh')
        self.add_function('threshold')
        self.add_function('threshold_at_1')
        self.add_function('inrange_bin')
        self.add_function('inrange')


class ArithmeticSet(FunctionSet):
    def fill(self):
        self.add_function('bitwise_and')
        self.add_function('bitwise_and_mask')
        self.add_function('bitwise_not')
        self.add_function('bitwise_or')
        self.add_function('bitwise_xor')
        self.add_function('add')
        self.add_function('subtract')


class OpencvSet(FunctionSet):
    def fill(self):
        self.add_function_set(FILTER_SET)
        self.add_function_set(MORPHOLOGY_SET)
        self.add_function_set(ARITHMETIC_SET)
        self.add_function_set(MISC_SET)


FILTER_SET = FilterSet()
MORPHOLOGY_SET = MorphologySet()
ARITHMETIC_SET = ArithmeticSet()
MISC_SET = MiscSet()
OPENCV_SET = OpencvSet()
