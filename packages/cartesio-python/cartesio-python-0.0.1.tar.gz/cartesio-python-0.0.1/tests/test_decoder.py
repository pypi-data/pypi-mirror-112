from cartesio.model.ea.genome import GenomeMetadata
from cartesio.model.ea.decoder import Decoder
from cartesio.cv.opencv_set import OPENCV_SET
from skimage import data
import numpy as np


cells = data.cell()
cells_half = cells/2

coffee = data.coffee()

x1 = [cells, cells_half, cells]
x2 = [coffee[i] for i in range(len(coffee))]
X = [x1, x2]
FSET = OPENCV_SET
METADATA = GenomeMetadata(3, 10, 1, OPENCV_SET.max_arity, OPENCV_SET.max_parameters)


class TestDecoding:
    def test_decoding_empty(self):
        decoder = Decoder(METADATA, FSET)
        genome = METADATA.prototype.clone()  # empty genome, all 0
        Y, ctime = decoder.decode(genome, X)
        y1 = Y[0]
        y2 = Y[1]
        assert np.array_equal(x1[0], y1[0])
        assert np.array_equal(x2[0], y2[0])
        assert not np.array_equal(x1[1], y1[0])
        assert not np.array_equal(x2[1], y2[0])
        assert not np.array_equal(x2[2], y2[0])

    def test_decoding(self):
        decoder = Decoder(METADATA, FSET)
        genome = METADATA.prototype.clone()  # empty genome, all 0
        # handmade changes to create graph
        genome.sequence[-1, 1] = 1  # output now gets second input
        Y, ctime = decoder.decode(genome, X)
        y1 = Y[0]
        y2 = Y[1]
        assert not np.array_equal(x1[0], y1[0])
        assert not np.array_equal(x2[0], y2[0])
        assert np.array_equal(x1[1], y1[0])
        assert np.array_equal(x2[1], y2[0])
