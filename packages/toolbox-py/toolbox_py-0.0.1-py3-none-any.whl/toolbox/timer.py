import threading
import time
from typing import Callable, Union



class Timer(threading.Thread):
    """
    A basic timer that works like setInterval in JavaScript
    To start a timer, run the `start()` method on the class
    This subclasses from `threading.Thread`

    Parameter
    ---------
    callback : `Callable`
        The function that should be executed
    interval : `int` | `float`
        Wait time between each function call
    event : `Event`
        The threading event
    """
    def __init__(self, callback: Callable, interval: Union[int, float], event: threading.Event = threading.Event()) -> None:
        self.callback = callback
        self.interval = interval
        super(Timer, self).__init__()

    
    def run(self, *args, **kwargs) -> None:
        while True:
            self.callback(*args, **kwargs)
            time.sleep(self.interval)