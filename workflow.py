from enum import Enum


class StateStatus(Enum):
    PENDING = 0
    IN_PROGRESS = 1
    COMPLETED = 2


class WorkFlow:

    def __init__(self):
        self._state = StateStatus.PENDING
        self._tasks = []

    def add_task(self, task):
        self._tasks.append(task)

    @property
    def state(self):
        return self._state
    
    @property
    def tasks(self):
        return self._tasks
