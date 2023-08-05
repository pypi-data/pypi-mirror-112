from cartesio.model.ea.genome import GenomeMetadata
from cartesio.applications.CGPIS import CGPIP
from cartesio.callbacks import CallbackVerbose, CallbackSave
from cartesio.dataset.dataset import DatasetFactory
from cartesio.utils.viewer import GenomeViewer, plot_contours


class DefaultTraining(object):
    def __init__(self, dataset, mutation_rate=0.15, workdir=None, endpoint=None):
        metadata = GenomeMetadata(3, 10, 1, 2, 2)
        self.dataset = DatasetFactory.create(dataset, True, True)
        self.model = CGPIP(metadata, mutation_rate)
        self.callbacks = []
        self.callbacks.append(CallbackVerbose(frequence=10))
        self.viewer = GenomeViewer(metadata, self.model.decoder.function_set)
        if workdir:
            self.callbacks.append(CallbackSave(self.model.decoder, workdir, dataset, frequence=10))

    def run(self, generations, populations, individuals):
        train_x = self.dataset.get_train_x()
        train_y = self.dataset.get_train_y()
        return self.model.fit(train_x, train_y, generations, populations, individuals, callbacks=self.callbacks)

    def display_genome(self, individual, only_active=False, jupyter=False):
        return self.viewer.get_graph(individual, only_active, jupyter)

    def predict_on_train_x(self, individual):
        p = self.model.predict(self.dataset.get_train_x(), individual)
        for one_p, img in zip(p, self.dataset.get_training_set().preview_images):
            self.model.overlay(one_p, img)
        return p

    def contours_on_test_x(self, individual):
        test_x = self.dataset.get_test_x()
        originals = self.dataset.get_testing_set().preview_images
        p = self.model.predict(test_x, individual)
        for i in range(len(originals)):
            plot_contours(originals[i], p[i][0])

    def evaluate_on_test_x(self, individual, plot_predictions=False):
        test_x = self.dataset.get_test_x()
        test_y = self.dataset.get_test_y()

        p = self.model.predict(test_x, individual)
        f = self.model.evaluate(test_y, [p])

        if plot_predictions:
            originals = self.dataset.get_testing_set().preview_images
            for i in range(len(originals)):
                plot_contours(originals[i], p[i][0])
        return f

    '''def evaluate_on_train_x(self, individual):
        return self.model.evaluate(self.dataset.get_train_x(), self.dataset.get_train_y(), individual)

    def evaluate_on_test_x(self, individual):
        return self.model.evaluate(self.dataset.get_test_x(), self.dataset.get_test_y(), individual)

    def get_dataset_name(self):
        return self.dataset.get_name()

    def save(self, genome, dataset_location):
        filename = str(self.workdir.location / 'elite.json')
        self.genome_saver.save(genome, self.model.decoder, filename, dataset_location)
    '''