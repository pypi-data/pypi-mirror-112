from cartesio.model.ea.fitness import FitnessFunction
from create_metric import MetricIOU
import numpy as np


class FitnessIOU(FitnessFunction):
    def __init__(self):
        self.iou = MetricIOU()

    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        n = len(y_true)
        fitness_score = 0.0
        for i in range(n):
            fitness_score += self.iou.compute(y_true[i], y_pred[i])
        return 1 - (fitness_score / n)


def main():
    fitness = FitnessIOU()

    y_true_1 = np.random.randint(2, size=(224, 224))
    y_true_2 = np.random.randint(2, size=(224, 224))
    y_true = np.array([y_true_1, y_true_2])

    y_pred_1 = np.random.randint(2, size=(224, 224))
    y_pred_2 = np.random.randint(2, size=(224, 224))
    y_pred = np.array([y_pred_1, y_pred_2])

    fitness_score = fitness.evaluate(y_true, y_pred)
    print(fitness_score)


if __name__ == "__main__":
    main()
