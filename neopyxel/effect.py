
from abc import ABC, abstractmethod


class Effect(ABC):
    def __init__(self, relay):
        self.relay = relay

    def start(self):
        self.start_transition()
        self.effect_main()

    def stop(self):
        self.stop_transition()

    @abstractmethod
    def start_transition(self):
        pass

    @abstractmethod
    def effect_main(self):
        pass

    @abstractmethod
    def stop_transition(self):
        pass
