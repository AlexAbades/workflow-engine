import unittest
from workflow import Link, WorkFlow, Task, StateStatus


class Test_TestWorkFlow(unittest.TestCase):

    def test_worfkflow_test(self):
        self.assertTrue(True)

    def test_worflow_add_task(self):

        onboarding = WorkFlow()

        tasks = ["Sign Up", "Verify Email"]

        onboarding.add_task(tasks[0])
        onboarding.add_task(tasks[1])

        self.assertEqual(onboarding._tasks, tasks)

    def test_worfkflow_state_changes_on_changed_task_state(self):
        onboarding = WorkFlow()

        onboarding.add_task(Task("Sign Up", onboarding))
        onboarding.add_task(Task("Verify Email", onboarding))

        onboarding.tasks[0].change_task_state(StateStatus.IN_PROGRESS)

        self.assertEqual(onboarding.state, StateStatus.IN_PROGRESS)

    def test_workflow_state_is_completed_when_all_tasks_are_completed(self):
        onboarding = WorkFlow()

        onboarding.add_task(Task("Sign Up", onboarding))
        onboarding.add_task(Task("Verify Email", onboarding))

        onboarding.tasks[0].change_task_state(StateStatus.COMPLETED)
        onboarding.tasks[1].change_task_state(StateStatus.COMPLETED)

        self.assertEqual(onboarding.state, StateStatus.COMPLETED)

    def test_workflow_state_is_pending_when_all_tasks_are_pending(self):
        onboarding = WorkFlow()

        onboarding.add_task(Task("Sign Up", onboarding))
        onboarding.add_task(Task("Verify Email", onboarding))

        self.assertEqual(onboarding.state, StateStatus.PENDING)

    def test_workflow_state_is_in_progress_when_one_task_is_in_progress(self):
        onboarding = WorkFlow()

        onboarding.add_task(Task("Sign Up", onboarding))
        onboarding.add_task(Task("Verify Email", onboarding))

        onboarding.tasks[0].change_task_state(StateStatus.IN_PROGRESS)

        self.assertEqual(onboarding.state, StateStatus.IN_PROGRESS)

    def test_workflow_state_is_in_progress_when_all_tasks_are_completed_except_one(
        self,
    ):
        onboarding = WorkFlow()

        onboarding.add_task(Task("Sign Up", onboarding))
        onboarding.add_task(Task("Verify Email", onboarding))

        onboarding.tasks[0].change_task_state(StateStatus.COMPLETED)

        self.assertEqual(onboarding.state, StateStatus.IN_PROGRESS)

    def test_target_task_state_changes_on_source_task_change_state(self):
        onboarding = WorkFlow()

        sign_up = Task("sign Up", onboarding)
        verify_email = Task("Verify Email", onboarding)

        sign_up.add_link(
            Link(sign_up, StateStatus.COMPLETED, verify_email, StateStatus.IN_PROGRESS)
        )

        onboarding.add_task(sign_up)
        onboarding.add_task(verify_email)

        sign_up.change_task_state(StateStatus.COMPLETED)

        self.assertEqual(verify_email.state, StateStatus.IN_PROGRESS)
