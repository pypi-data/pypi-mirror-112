import cv2
from cartesio.model.function import FunctionNodeWritable


class Add(FunctionNodeWritable):
    def __init__(self):
        super(Add, self).__init__('add', 2, 0)

    def __call__(self, inputs, p):
        return cv2.add(inputs[0], inputs[1])

    def to_python(self, input_names, p, output_name):
        return f'{output_name} = cv2.add({input_names[0]}, {input_names[1]})'

    def to_cpp(self, input_names, p, output_name):
        return f'cv::add({input_names[0]}, {input_names[1]}, {output_name});'


class Subtract(FunctionNodeWritable):
    def __init__(self):
        super(Subtract, self).__init__('subtract', 2, 0)

    def __call__(self, inputs, p):
        return cv2.subtract(inputs[0], inputs[1])

    def to_python(self, input_names, p, output_name):
        return f'{output_name} = cv2.subtract({input_names[0]}, {input_names[1]})'

    def to_cpp(self, input_names, p, output_name):
        return f'cv::subtract({input_names[0]}, {input_names[1]}, {output_name});'


class BitwiseNot(FunctionNodeWritable):
    def __init__(self):
        super(BitwiseNot, self).__init__('bitwise_not', 1, 0)

    def __call__(self, inputs, p):
        return cv2.bitwise_not(inputs[0])

    def to_python(self, input_names, p, output_name):
        return f'{output_name} = cv2.bitwise_not({input_names[0]})'

    def to_cpp(self, input_names, p, output_name):
        return f'cv::bitwise_not({input_names[0]}, {output_name});'


class BitwiseOr(FunctionNodeWritable):
    def __init__(self):
        super(BitwiseOr, self).__init__('bitwise_or', 2, 0)

    def __call__(self, inputs, p):
        return cv2.bitwise_or(inputs[0], inputs[1])

    def to_python(self, input_names, p, output_name):
        return f'{output_name} = cv2.bitwise_or({input_names[0]}, {input_names[1]})'

    def to_cpp(self, input_names, p, output_name):
        return f'cv::bitwise_or({input_names[0]}, {input_names[1]}, {output_name});'


class BitwiseAnd(FunctionNodeWritable):
    def __init__(self):
        super(BitwiseAnd, self).__init__('bitwise_and', 2, 0)

    def __call__(self, inputs, p):
        return cv2.bitwise_and(inputs[0], inputs[1])

    def to_python(self, input_names, p, output_name):
        return f'{output_name} = cv2.bitwise_and({input_names[0]}, {input_names[1]})'

    def to_cpp(self, input_names, p, output_name):
        return f'cv::bitwise_and({input_names[0]}, {input_names[1]}, {output_name});'


class BitwiseAndMask(FunctionNodeWritable):
    def __init__(self):
        super(BitwiseAndMask, self).__init__('bitwise_and_mask', 2, 0)

    def __call__(self, inputs, p):
        return cv2.bitwise_and(inputs[0], inputs[0], mask=inputs[1])

    def to_python(self, input_names, p, output_name):
        return f'{output_name} = cv2.bitwise_and({input_names[0]}, {input_names[0]}, mask={input_names[1]})'

    def to_cpp(self, input_names, p, output_name):
        return f'cv::bitwise_and({input_names[0]}, {input_names[0]}, {output_name}, {input_names[1]});'


class BitwiseXor(FunctionNodeWritable):
    def __init__(self):
        super(BitwiseXor, self).__init__('bitwise_xor', 2, 0)

    def __call__(self, inputs, p):
        return cv2.bitwise_xor(inputs[0], inputs[1])

    def to_python(self, input_names, p, output_name):
        return f'{output_name} = cv2.bitwise_xor({input_names[0]}, {input_names[1]})'

    def to_cpp(self, input_names, p, output_name):
        return f'cv::bitwise_xor({input_names[0]}, {input_names[1]}, {output_name});'
