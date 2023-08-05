import cv2
from cartesio.model.ea.ga import ObservableGeneticAlgorithm
from cartesio.model.ea.decoder import CartesianGenomeDecoder

from abc import ABC, abstractmethod
import numpy as np
from typing import List

i = 0


class AbstractModel(ABC):
    @abstractmethod
    def fit(self,
            train_x: List,
            train_y: List,
            n_populations: int,
            n_individuals: int,
            generations: int,
            callbacks: List = []):
        pass

    @abstractmethod
    def evaluate(self, test_x: List, test_y: List):
        pass

    @abstractmethod
    def predict(self, x: List):
        pass


class AbstractCGP(AbstractModel, ABC):
    def __init__(self, decoder):
        self.decoder = decoder
        self.genetic_algorithm = ObservableGeneticAlgorithm(decoder)
        self._compose_genetic_algorithm()

    def add_callback(self, callback):
        self.genetic_algorithm.attach(callback)

    @abstractmethod
    def _compose_genetic_algorithm(self):
        pass

    def fit(self, x, y, generations, populations, individuals, callbacks=[]):
        self.genetic_algorithm.clear()
        for callback in callbacks:
            self.genetic_algorithm.attach(callback)
        history = self.genetic_algorithm.run(x, y, generations, populations, individuals)
        best_individual = history.get_best(generations-1)
        return best_individual, history

    def evaluate(self, x, y, individual=None):
        if not individual:
            individual = self.best.best_individual
        f, t = self.GA.evaluate_one_individual(individual, x=x, y=y)
        return f

    def predict(self, x, individual=None):
        if not individual:
            individual = self.best.best_individual
        p, t = self.decoder.decode_genome(individual, x)
        return p


class ModelFactory(object):
    @staticmethod
    def create(n_inputs, n_functions, n_outputs, n_parameters, n_connexions, function_set, mu, endpoint=None):

        # Standard CGPIP, can be used for multiple outputs
        if endpoint is None:
            metadata = GenomeMetadata(n_inputs, n_functions, n_outputs, n_parameters, n_connexions)
            return CGPIP(metadata, function_set)
        elif endpoint == 'C':
            metadata = GenomeMetadata(n_inputs, n_functions, 1, n_parameters, n_connexions)
            return CGPC(metadata, function_set)

        elif endpoint == 'L':
            metadata = GenomeMetadata(n_inputs, n_functions, 1, n_parameters, n_connexions)
            return CGPL(metadata, function_set)

        elif endpoint == 'R':
            metadata = GenomeMetadata(n_inputs, n_functions, n_outputs, n_parameters, n_connexions)
            return CGPR(metadata, function_set)

        elif endpoint == 'W':
            n_outputs = 2  # masks and seeds for one class
            metadata = GenomeMetadata(n_inputs, n_functions, n_outputs, n_parameters, n_connexions)
            return CGPIS_W(metadata, function_set)

        elif endpoint == 'HCT':
            n_outputs = 1  # only the mask needed for circles
            # Melanomes: [20, 1, 10, 1, 28]
            # Mastocytes: [125, 1, 10, 50, 80]
            # Cells: [60, 1, 10, 30, 60]
            # DAPI: [30, 1, 10, 5, 15]
            # TRM: [15, 1, 10, 9, 50]
            metadata = GenomeMetadata(n_inputs, n_functions, n_outputs, n_parameters, n_connexions)
            return CGPIS_HCT(metadata, function_set, 50, 30, 110)

        elif endpoint == 'FE':
            n_outputs = 1  # only the mask needed for ellipses
            metadata = GenomeMetadata(n_inputs, n_functions, n_outputs, n_parameters, n_connexions)
            return CGPIS_FE(metadata, mu)

        elif endpoint == 'SD':
            n_outputs = 1  # only the mask needed for corr
            metadata = GenomeMetadata(n_inputs, n_functions, n_outputs, n_parameters, n_connexions)
            return CGPSD(metadata, mu)

        return None

    @staticmethod
    def from_json(jsonfile):
        pass

    @staticmethod
    def from_dict(dictobj):
        pass



# Cartesian Genetic Programming for Counting
class CGPL(EndpointedCGP):
    def __init__(self, metadata, function_set):
        super(CGPL, self).__init__(metadata, function_set, EndpointMaskToLabels())

    def create_genetic_algorithm(self):
        initialization = FullyRandomMutation(self.decoder._m, self.decoder.function_set.n_functions)
        mutation = ClassicalMutation(self.decoder._m, self.decoder.function_set.n_functions, 0.15)
        fitness = FitnessAP05()
        prototype = self.decoder._m.prototype
        decoder = self.decoder
        return ObservableGeneticAlgorithm(initialization, mutation, fitness, prototype, decoder)

    def overlay(self, pred, img):
        global i
        overlayed = img.copy()
        mask_pred = pred[0]
        overlayed = overlay(overlayed, mask_pred, color=[0, 255, 255])
        cv2.imwrite('best_overlay'+str(i)+'.png', rgb2bgr(overlayed))
        i += 1


# Cartesian Genetic Programming for Image Processing
class CGPIP(StandardCGP):
    def __init__(self, metadata, function_set):
        super(CGPIP, self).__init__(metadata, function_set)

    def create_genetic_algorithm(self):
        initialization = FullyRandomMutation(self.decoder._m, self.decoder.function_set.n_functions)
        mutation = ClassicalMutation(self.decoder._m, self.decoder.function_set.n_functions, 0.2)
        fitness = FitnessIOU()
        prototype = self.decoder._m.prototype
        decoder = self.decoder
        return ObservableGeneticAlgorithm(initialization, mutation, fitness, prototype, decoder)

    def overlay(self, pred, img):
        global i
        overlayed = img.copy()
        mask_pred = pred[0]
        overlayed = overlay(overlayed, mask_pred, color=[0, 255, 255])
        cv2.imwrite('best_overlay'+str(i)+'.png', rgb2bgr(overlayed))
        i += 1


# Cartesian Genetic Programming for Instance Segmentation
class CGPIS(EndpointedCGP, ABC):
    pass


# Cartesian Genetic Programming for Instance Segmentation
# Watershed endpoint: Masks and Seeds are required as outputs
class CGPIS_W(CGPIS):
    def __init__(self, metadata, function_set):
        super(CGPIS_W, self).__init__(metadata, function_set, EndpointWatershed())

    def create_genetic_algorithm(self):
        initialization = FullyRandomMutation(self.decoder._m, self.decoder.function_set.n_functions)
        mutation = ClassicalMutation(self.decoder._m, self.decoder.function_set.n_functions, 0.15)
        fitness = FitnessCountAndIOU()
        # fitness = FitnessAP05()
        prototype = self.decoder._m.prototype
        decoder = self.decoder
        return ObservableGeneticAlgorithm(initialization, mutation, fitness, prototype, decoder)

    def preview_graph(self, name):
        if self.use_viewer:
            best_individual = self.save_the_best.best_individual
            self.viewer.save_graph_only_active(best_individual, name + '_masks.png', output_index=0)
            self.viewer.save_graph_only_active(best_individual, name + '_seeds.png', output_index=1)
        else:
            print("Viewer not activated (Pygraphviz not installed)")

    def overlay(self, pred, img):
        global i
        overlayed = img.copy()
        mask_pred, seeds, n_seeds, labels = pred
        # overlayed = overlay(overlayed, mask_pred, color=[0, 255, 255])
        # overlayed = overlay(overlayed, seeds, color=[255, 0, 0])

        for one_label_num in np.unique(labels):
            if one_label_num == 0:
                continue
            one_mask = ((labels == one_label_num)*1).astype(np.uint8)
            overlayed = overlay(overlayed, one_mask, color=[0, 255, 255], alpha=0.6)
            one_mask = ((seeds == one_label_num)*1).astype(np.uint8)
            overlayed = overlay(overlayed, one_mask, color=[255, 0, 0], alpha=0.6)
        cv2.imwrite('best_overlay'+str(i)+'.png', rgb2bgr(overlayed))
        i += 1


# Cartesian Genetic Programming for Instance Processing
# Rescale endpoint
class CGPR(EndpointedCGP):
    def __init__(self, metadata, function_set):
        super(CGPR, self).__init__(metadata, function_set, EndpointRescale(0.5))

    def create_genetic_algorithm(self):
        initialization = FullyRandomMutation(self.decoder._m, self.decoder.function_set.n_functions)
        mutation = ClassicalMutation(self.decoder._m, self.decoder.function_set.n_functions, 0.15)
        fitness = FitnessIOU()
        prototype = self.decoder._m.prototype
        decoder = self.decoder
        return ObservableGeneticAlgorithm(initialization, mutation, fitness, prototype, decoder)

    def overlay(self, pred, img):
        global i
        overlayed = img.copy()
        mask_pred = pred[0]
        overlayed = overlay(overlayed, mask_pred, color=[0, 255, 255])
        cv2.imwrite('best_overlay'+str(i)+'.png', rgb2bgr(overlayed))
        i += 1


# Cartesian Genetic Programming for Instance Segmentation
# Hough Circle Transform endpoint: Masks required to fit circles
class CGPIS_HCT(CGPIS):
    def __init__(self, metadata, function_set, min_dist, min_radius, max_radius):
        super(CGPIS_HCT, self).__init__(metadata, function_set, EndpointHoughCircle(min_dist, min_radius, max_radius))

    def create_genetic_algorithm(self):
        initialization = FullyRandomMutation(self.decoder._m, self.decoder.function_set.n_functions)
        mutation = ClassicalMutation(self.decoder._m, self.decoder.function_set.n_functions, 0.15)
        fitness = FitnessIOU()  # FitnessCountAndIOU()
        prototype = self.decoder._m.prototype
        decoder = self.decoder
        return ObservableGeneticAlgorithm(initialization, mutation, fitness, prototype, decoder)

    def overlay(self, pred, img):
        global i
        overlayed = img.copy()
        mask_pred, seeds, n_seeds, _ = self.ga._fitness.endpoint.execute(pred)
        overlayed = overlay(overlayed, mask_pred, color=[0, 255, 255])
        cv2.imwrite('best_overlay'+str(i)+'.png', rgb2bgr(overlayed))
        i += 1


# Cartesian Genetic Programming for Instance Segmentation
# Fit Ellipse endpoint: Masks required to fit ellipses
class CGPIS_FE(CGPIS):
    def __init__(self, metadata, mu):
        super(CGPIS_FE, self).__init__(metadata, mu)
        # DAPI: [30, 50]
        # cells: [60, 120]
        # Melanomes: [5, 60]
        min_axis = 10
        max_axis = 60
        self.ga.set_fitness(FitnessEllipse(min_axis, max_axis))

    def overlay(self, pred, img):
        global i
        overlayed = img.copy()
        mask_pred, mask_seeds, n, labels = self.ga._fitness.endpoint.execute(pred)

        for ellipse in labels:
            color = np.random.choice(range(256), size=3)
            color = [int(color[0]), int(color[1]), int(color[2])]
            one_mask = imnew(mask_pred.shape)
            cv2.ellipse(one_mask, ellipse, BINARY_FILL_COLOR, thickness=-1)
            overlayed = overlay(overlayed, one_mask, color=color, alpha=0.6)
        cv2.imwrite('best_overlay'+str(i)+'.png', rgb2bgr(overlayed))
        i += 1


# Cartesian Genetic Programming Statistics-Driven
class CGPSD(CGPIS):
    def __init__(self, metadata, mu):
        super(CGPSD, self).__init__(metadata, mu)
        self.ga.set_fitness(FitnessElasticNet())
