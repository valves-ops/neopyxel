
from abc import ABC, abstractmethod


class Effect(ABC):
    def __init__(self, relay, StartTransition=None,
                 StopTransition=None, **kwargs):
        self.relay = relay
        if StartTransition is not None:
            self.start_transition = StartTransition(relay, **kwargs)
        if StopTransition is not None:
            self.stop_transition = StopTransition(relay, **kwargs)

    def start(self):
        self.start_transition.execute()
        self.effect_main()

    def stop(self):
        self.stop_transition.execute()

    # @abstractmethod
    # def start_transition(self):
    #     pass

    @abstractmethod
    def effect_main(self):
        pass

    # @abstractmethod
    # def stop_transition(self):
    #     pass


class Transition(ABC):
    def __init__(self, relay, **kwargs):
        self.relay = relay

    @abstractmethod
    def execute(self):
        pass
