import cartesio.cv.morphology as morph
import cartesio.cv.arithmetic as arith
import cartesio.cv.filters as filters
import cartesio.cv.misc as misc
from cartesio.helpers.decorators import catalog_decorator


@catalog_decorator
class FunctionCatalog(object):

    functions = dict()

    @classmethod
    def add_function(cls, function):
        cls.functions[function.name] = function

    @classmethod
    def get(cls, function_name):
        return cls.functions[function_name]

    @classmethod
    def fill_catalog(cls):
        cls.add_function(morph.Erode())
        cls.add_function(morph.Dilate())
        cls.add_function(morph.Open())
        cls.add_function(morph.Close())
        cls.add_function(morph.MorphGradient())
        cls.add_function(morph.MorphTopHat())
        cls.add_function(morph.MorphBlackHat())
        cls.add_function(morph.FillHoles())
        cls.add_function(morph.RemoveSmallHoles())
        cls.add_function(morph.RemoveSmallObjects())
        cls.add_function(morph.Thin())
        cls.add_function(filters.MedianBlur())
        cls.add_function(filters.GaussianBlur())
        cls.add_function(filters.Laplacian())
        cls.add_function(filters.SobelX())
        cls.add_function(filters.SobelY())
        cls.add_function(filters.Canny())
        cls.add_function(filters.Sharpen())
        cls.add_function(misc.DistanceTransform())
        cls.add_function(misc.DistanceTransformAndThresh())
        cls.add_function(misc.Threshold())
        cls.add_function(misc.ThresholdAt1())
        cls.add_function(misc.BinaryInRange())
        cls.add_function(misc.InRange())
        cls.add_function(arith.BitwiseAnd())
        cls.add_function(arith.BitwiseAndMask())
        cls.add_function(arith.BitwiseNot())
        cls.add_function(arith.BitwiseOr())
        cls.add_function(arith.BitwiseXor())
        cls.add_function(arith.Add())
        cls.add_function(arith.Subtract())
