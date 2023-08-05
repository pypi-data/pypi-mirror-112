from cgpis.cgp_model.cgpis_model import ModelFactory
from cgpis.dataset import DatasetFactory
from cgpis.saving.chromosome_saver import GenomeSaver
from cgpis.functions.function_set import OPENCV_FUNCTION_SET
from cania_utils.disk import Disk
from cania_utils.stamp import eventid
from cgpis.callbacks import CallbackSaveGeneration

import argparse


class TrainingProcess(object):
    def __init__(self, dataset_location, n_functions, mu, endpoint, workdir):
        if endpoint is None or endpoint == 'SD':
            self.dataset = DatasetFactory.create(dataset_location, counting=False, preview=True)
        if endpoint == 'C':
            self.dataset = DatasetFactory.create(dataset_location, counting=True, preview=True, gt_scale=0.9)
        else:
            self.dataset = DatasetFactory.create(dataset_location, counting=True, preview=True)

        function_set = OPENCV_FUNCTION_SET
        n_parameters = function_set.max_parameters
        n_connexions = function_set.max_arity
        self.model = ModelFactory.create(self.dataset.n_inputs, n_functions, self.dataset.n_outputs, n_parameters, n_connexions, function_set, mu, endpoint)
        self.workdir = workdir
        self.genome_saver = GenomeSaver()
        self.model.add_callback(CallbackSaveGeneration(self.workdir, self.genome_saver, dataset_location))

    def run(self, n_populations, n_individuals, max_generations):
        return self.model.fit(self.dataset.get_train_x(), self.dataset.get_train_y(), n_populations, n_individuals, max_generations)

    def predict_on_train_x(self, individual):
        p = self.model.predict(self.dataset.get_train_x(), individual)
        for one_p, img in zip(p, self.dataset.get_training_set().preview_images):
            self.model.overlay(one_p, img)
        return p

    def predict_on_test_x(self, individual):
        p = self.model.predict(self.dataset.get_test_x(), individual)
        for one_p, img in zip(p, self.dataset.get_testing_set().preview_images):
            self.model.overlay(one_p, img)
        return p

    def evaluate_on_train_x(self, individual):
        return self.model.evaluate(self.dataset.get_train_x(), self.dataset.get_train_y(), individual)

    def evaluate_on_test_x(self, individual):
        return self.model.evaluate(self.dataset.get_test_x(), self.dataset.get_test_y(), individual)

    def get_dataset_name(self):
        return self.dataset.get_name()

    def save(self, genome, dataset_location):
        filename = str(self.workdir.location / 'elite.json')
        self.genome_saver.save(genome, self.model.decoder, filename, dataset_location)


def main(dataset_location, endpoint, max_generations, n_functions, mu, n_populations, n_individuals, workdir):
    training_process = TrainingProcess(dataset_location, n_functions, mu, endpoint, workdir.next(eventid()))
    individual, history = training_process.run(n_populations, n_individuals, max_generations)

    training_process.save(individual, dataset_location)

    training_process.predict_on_train_x(individual)  # will show prediction
    training_score = training_process.evaluate_on_train_x(individual)
    print(f'training score  \t{training_score:.4f}')

    training_process.predict_on_test_x(individual)  # will show prediction
    evaluation_score = training_process.evaluate_on_test_x(individual)
    print(f'evaluation score \t{evaluation_score:.4f}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", help="path to the dataset folder")
    parser.add_argument("--endpoint", choices=['W', 'HCT', 'SD', 'FE'], type=str, default=None)
    parser.add_argument("--generations", type=int, default=20)
    parser.add_argument("--populations", type=int, default=20)
    parser.add_argument("--individuals", type=int, default=20)
    parser.add_argument("--functions", type=int, default=20)
    parser.add_argument("--mu", type=float, default=0.2)
    args = parser.parse_args()
    dataset_location = args.dataset
    endpoint = args.endpoint
    max_generations = args.generations
    mu = args.mu
    n_populations = args.populations
    n_individuals = args.individuals
    n_functions = args.functions
    scale = args.scale
    workdir = Disk(dataset_location)
    main(dataset_location, endpoint, max_generations, n_functions, mu, n_populations, n_individuals, workdir, scale)
