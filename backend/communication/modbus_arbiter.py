import logging
import threading
from contextlib import contextmanager


logger = logging.getLogger(__name__)


class ModbusBusArbiter:
    """Serialize requests on one bus and let control jump ahead of polling."""

    def __init__(self, bus_name: str):
        self.bus_name = bus_name
        self._condition = threading.Condition()
        self._active_request = False
        self._waiting_control = 0
        self._thread_state = threading.local()

    @contextmanager
    def operation(self, mode: str):
        previous = getattr(self._thread_state, "mode", "polling")
        self._thread_state.mode = mode
        try:
            yield
        finally:
            self._thread_state.mode = previous

    def current_mode(self) -> str:
        return getattr(self._thread_state, "mode", "polling")

    def acquire(self):
        mode = self.current_mode()
        with self._condition:
            if mode == "control":
                self._waiting_control += 1
                try:
                    while self._active_request:
                        self._condition.wait()
                    self._active_request = True
                finally:
                    self._waiting_control -= 1
            else:
                while self._active_request or self._waiting_control > 0:
                    if self._waiting_control > 0:
                        logger.debug(
                            "[ModbusArbiter] Polling is yielding to control on %s",
                            self.bus_name,
                        )
                    self._condition.wait()
                self._active_request = True

    def release(self):
        with self._condition:
            self._active_request = False
            self._condition.notify_all()
