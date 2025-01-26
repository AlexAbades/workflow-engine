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
    # - What happens if all of them are completed except one which is pending, should be in progress
    def on_task_state_changed(self):
        if all(task.state == StateStatus.COMPLETED for task in self._tasks):
            self._state = StateStatus.COMPLETED
        elif any(task.state == StateStatus.IN_PROGRESS for task in self._tasks):
            self._state = StateStatus.IN_PROGRESS
        elif all(task.state == StateStatus.PENDING for task in self._tasks):
            self._state = StateStatus.PENDING
        else:
            self._state = StateStatus.IN_PROGRESS


class Task:

    def __init__(self, name: str, workflow_parent: WorkFlow):
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

    def change_task_state(self, new_state: StateStatus):
        self._state = new_state
        if self.workflow_parent:
            self.workflow_parent.on_task_state_changed()

        if self.link:
            self.link.on_source_state_changed()


class Link:

    def __init__(
        self,
        source_task: Task,
        trigger_state: StateStatus,
        target_task: Task,
        update_state: StateStatus,
    ):
        self.source_task = source_task
        self.trigger_state = trigger_state
        self.target_task = target_task
        self.update_state = update_state

    def on_source_state_changed(self):
        if self.source_task.state == self.trigger_state:
            self.target_task.change_task_state(self.update_state)
