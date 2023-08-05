from cartesio.model.endpoint import EndpointABC

import cv2
from typing import List


class EndpointBinarize(EndpointABC):
    def __init__(self, threshold: int):
        super().__init__('binarize')
        self.threshold = threshold

    def execute(self, entries: List):
        img = entries[0]
        img = cv2.threshold(img, self.threshold, 255, cv2.THRESH_BINARY)[1]
        return img


def main():
    threshold = 128
    endpoint = EndpointBinarize(threshold)


if __name__ == "__main__":
    main()
