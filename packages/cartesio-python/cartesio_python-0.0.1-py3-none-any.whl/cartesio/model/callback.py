from cartesio.helpers.observer import Observer

from abc import ABC, abstractmethod
from cartesio.utils.saving import GenomeSaver
from cania_utils.disk import Disk
from cania_utils.stamp import eventid


class Callback(Observer, ABC):

    @abstractmethod
    def call(self, e_name, e_content):
        pass

    def update(self, event):
        self.call(event['name'], event['content'])


class CallbackVerbose(Callback):
    def __init__(self, frequence=1):
        self.frequence = frequence

    def update(self, event):
        event_name = event._state['event']
        if event_name != 'on_evaluation_end':
            return
        generation = event._state['generation']
        if generation.n % self.frequence == 0:
            individual = generation.get_best()
            n = generation.n
            fitness = individual.fitness["fitness"]
            time = individual.fitness["time"]
            fps = 1./time
            print(f'[G {n:04}] {fitness:.4f} {time:.6f}s {int(round(fps))}fps')


class CallbackSave(Callback):
    def __init__(self, decoder, workdir, dataset, frequence=1):
        self.decoder = decoder
        self.workdir = Disk(workdir).next(eventid())
        self.dataset = dataset
        self.saver = GenomeSaver()
        self.frequence = frequence

    def update(self, event):
        event_name = event._state['event']
        if event_name == 'on_evaluation_end':
            generation = event._state['generation']
            if generation.n % self.frequence == 0:
                generation_dir = self.workdir.next(f'G{generation.n}').location
                for p_idx, p in generation.get_populations():
                    for i_idx, i in p.get_individuals():
                        name = str(generation_dir / f'P{p_idx}_I{i_idx}.json')
                        self.saver.save(i, self.decoder, name, self.dataset)


'''
class CallbackSaveGeneration(Observer):
    def __init__(self, workdir, saver, dataset):
        self.decoder = None
        self.workdir = workdir
        self.dataset = dataset
        self.saver = saver

    def update(self, event):
        event_name = event._state['event']
        if event_name == 'on_evaluation_end':
            generation = event._state['generation']
            generation_dir = self.workdir.next(f'G{generation.n}').location
            for p_idx, p in generation.get_populations():
                for i_idx, i in p.get_individuals():
                    name = str(generation_dir / f'P{p_idx}_I{i_idx}.json')
                    self.saver.save(i, self.decoder, name, self.dataset)
'''
