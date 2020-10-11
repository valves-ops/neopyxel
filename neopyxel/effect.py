
from abc import ABC, abstractmethod
import threading


class Effect(ABC):
    def __init__(self, relay, StartTransition=None,
                 StopTransition=None, **kwargs):
        self.relay = relay
        self.stop_thread = False
        if StartTransition is not None:
            self.start_transition = StartTransition(relay, **kwargs)
        if StopTransition is not None:
            self.stop_transition = StopTransition(relay, **kwargs)

    def start(self):
        self.start_transition.execute()
        self.effect_main_thread = threading.Thread(target=self.effect_main())
        self.effect_main_thread.start()

    def stop(self):
        self.stop_thread = True
        if self.effect_main_thread.is_alive():
            self.effect_main_thread.join()
        self.stop_transition.execute()

    @abstractmethod
    def effect_main(self):
        pass


class Transition(ABC):
    def __init__(self, relay, **kwargs):
        self.relay = relay

    @abstractmethod
    def execute(self):
        pass
