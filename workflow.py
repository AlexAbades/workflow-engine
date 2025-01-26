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

    # If a task state is changed, the workflow should be notified:
    # - All tasks are pending: Worflow is pending
    # - At least one task is in progress: Workflow is in progress
    # - All tasks are completed: Workflow is completed
    def on_task_state_changed(self):
        if all(task._state == StateStatus.COMPLETED for task in self._tasks):
            self._state = StateStatus.COMPLETED
        if any(task._state == StateStatus.IN_PROGRESS for task in self._tasks):
            self._state = StateStatus.IN_PROGRESS
        else:
            self._status = StateStatus.PENDING


class Task:

    def __init__(self, name:str, workflow_parent: WorkFlow):
        self.name = name
        self.workflow_parent = workflow_parent
        self.link = None
        self._state = StateStatus.PENDING

    @property
    def state(self):
        return self._state

    # Just ads one link to a task, maybe could be more than one link if this tasks triggers multiple tasks
    def add_link(self, link):
        self.link = link
    
    def change_state(self, new_state: StateStatus):
        self._state = new_state
        if self.workflow_parent:
            self.workflow_parent.on_task_state_changed()
            
