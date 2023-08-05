
from cania_utils.disk import Disk
import simplejson


class GenomeSaver(object):
    def save(self, genome, decoder, filename, dataset):
        sequence_as_json = {
            "dataset": dataset,
            "sequence": simplejson.dumps(genome.sequence.tolist()),
            "fitness": genome.fitness,
            "decoding": decoder.to_json()
        }
        with open(filename, 'w') as outfile:
            simplejson.dump(sequence_as_json, outfile, indent=4)

    def load(self, filename):
        with open(filename, 'rb') as inputfile:
            sequence_as_json = simplejson.load(inputfile)
            genome = IndividualGenome.from_json(sequence_as_json['sequence'])
            decoder = GenomeDecoder.from_json(sequence_as_json['decoding'])

        return genome, decoder
