from cartesio.model.function import FunctionNode

import cv2
import numpy as np
from typing import List


class FunctionAdd(FunctionNode):
    def __init__(self):
        super().__init__('add', 2, 0)

    def __call__(self, inputs: List, p: List):
        return cv2.add(inputs[0], inputs[1])


def main():
    function_node = FunctionAdd()
    input_1 = np.random.randint(2, size=(224, 224))
    input_2 = np.random.randint(2, size=(224, 224))

    inputs = [input_1, input_2]
    p = []  # no parameters

    output = function_node(inputs, p)


if __name__ == "__main__":
    main()
