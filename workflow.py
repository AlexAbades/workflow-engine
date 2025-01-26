from enum import Enum


class StateStatus(Enum):
    PENDING = 0
    IN_PROGRESS = 1
    COMPLETED = 2


class WorkFlow:

    def __init__(self, name: str = ""):
        self._state = StateStatus.PENDING
        self._tasks = []
        # We should add Links to the workflow, so we can trigger tasks or other workflow
        self.name = name
        self._link = None

    def add_task(self, task):
        self._tasks.append(task)

    @property
    def state(self):
        return self._state

    @property
    def tasks(self):
        return self._tasks

    # Still can only be linked to one workflow, maybe it can be changed to be a list of links so it can modify multiple workflows or links.
    def add_link(self, link):
        self._link = link

    def on_task_state_changed(self):

        if all(task.state == StateStatus.COMPLETED for task in self._tasks):
            new_state = StateStatus.COMPLETED
        elif any(task.state == StateStatus.IN_PROGRESS for task in self._tasks):
            new_state = StateStatus.IN_PROGRESS
        elif all(task.state == StateStatus.PENDING for task in self._tasks):
            new_state = StateStatus.PENDING
        else:
            new_state = StateStatus.IN_PROGRESS

        self.change_state(new_state)

    def change_state(self, new_state: StateStatus):
        self._state = new_state
        if self._link:
            self._link.on_source_state_changed()


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

    def change_state(self, new_state: StateStatus):
        self._state = new_state
        if self.workflow_parent:
            self.workflow_parent.on_task_state_changed()

        if self.link:
            self.link.on_source_state_changed()


class Link:

    def __init__(
        self,
        source: Task | WorkFlow,
        trigger_state: StateStatus,
        target: Task | WorkFlow,
        update_state: StateStatus,
    ):
        self.source_task = source
        self.trigger_state = trigger_state
        self.target_task = target
        self.update_state = update_state

    def on_source_state_changed(self):
        if self.source_task.state == self.trigger_state:
            self.target_task.change_state(self.update_state)
