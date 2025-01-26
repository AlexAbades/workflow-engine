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

        onboarding.tasks[0].change_state(StateStatus.IN_PROGRESS)

        self.assertEqual(onboarding.state, StateStatus.IN_PROGRESS)

    def test_workflow_state_is_completed_when_all_tasks_are_completed(self):
        onboarding = WorkFlow()

        onboarding.add_task(Task("Sign Up", onboarding))
        onboarding.add_task(Task("Verify Email", onboarding))

        onboarding.tasks[0].change_state(StateStatus.COMPLETED)
        onboarding.tasks[1].change_state(StateStatus.COMPLETED)

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

        onboarding.tasks[0].change_state(StateStatus.IN_PROGRESS)

        self.assertEqual(onboarding.state, StateStatus.IN_PROGRESS)

    def test_workflow_state_is_in_progress_when_all_tasks_are_completed_except_one(
        self,
    ):
        onboarding = WorkFlow()

        onboarding.add_task(Task("Sign Up", onboarding))
        onboarding.add_task(Task("Verify Email", onboarding))

        onboarding.tasks[0].change_state(StateStatus.COMPLETED)

        self.assertEqual(onboarding.state, StateStatus.IN_PROGRESS)

    def test_target_task_state_updates_when_source_task_state_is_completed(self):
        onboarding = WorkFlow()

        sign_up = Task("sign Up", onboarding)
        verify_email = Task("Verify Email", onboarding)

        sign_up.add_link(
            Link(sign_up, StateStatus.COMPLETED, verify_email, StateStatus.IN_PROGRESS)
        )

        onboarding.add_task(sign_up)
        onboarding.add_task(verify_email)

        sign_up.change_state(StateStatus.COMPLETED)

        self.assertEqual(verify_email.state, StateStatus.IN_PROGRESS)

    def test_target_worflow_state_updates_when_source_workflow_state_is_completed(self):
        onboarding = WorkFlow(name="Onboarding")
        update_profile = WorkFlow(name="Update Profile")

        onboarding_sign_up = Task("Sign Up", onboarding)
        onboarding_verify_email = Task("Verify Email", onboarding)
        onboarding_sign_up.add_link(
            Link(
                onboarding_sign_up,
                StateStatus.COMPLETED,
                onboarding_verify_email,
                StateStatus.IN_PROGRESS,
            )
        )
        onboarding.add_task(onboarding_sign_up)
        onboarding.add_task(onboarding_verify_email)

        # In order to have 100% completed th profile both must be completed, if not the profile is in progress
        update_profile_update_name = Task("Update Name", update_profile)
        update_profile_update_profile_picture = Task(
            "Update Profile Picture", update_profile
        )
        update_profile.add_task(update_profile_update_name)
        update_profile.add_task(update_profile_update_profile_picture)

        onboarding.add_link(
            Link(
                onboarding,
                StateStatus.COMPLETED,
                update_profile,
                StateStatus.IN_PROGRESS,
            )
        )

        onboarding_sign_up.change_state(StateStatus.COMPLETED)
        onboarding_verify_email.change_state(StateStatus.COMPLETED)

        self.assertEqual(update_profile.state, StateStatus.IN_PROGRESS)

    def test_task_target_workflow_updates_when_source_worflow_is_complete(self):
        onboarding = WorkFlow(name="Onboarding")

        update_profile = WorkFlow(name="Update Profile")

        onboarding_sign_up = Task("Sign Up", onboarding)
        onboarding_verify_email = Task("Verify Email", onboarding)
        onboarding_sign_up.add_link(
            Link(
                onboarding_sign_up,
                StateStatus.COMPLETED,
                onboarding_verify_email,
                StateStatus.IN_PROGRESS,
            )
        )
        onboarding.add_task(onboarding_sign_up)
        onboarding.add_task(onboarding_verify_email)

        # In order to have 100% completed the profile both must be completed, if not the profile is in progress
        update_profile_update_name = Task("Update Name", update_profile)
        update_profile_update_profile_picture = Task(
            "Update Profile Picture", update_profile
        )
        update_profile.add_task(update_profile_update_name)
        update_profile.add_task(update_profile_update_profile_picture)

        onboarding.add_link(
            Link(
                onboarding,
                StateStatus.COMPLETED,
                update_profile_update_name,
                StateStatus.IN_PROGRESS,
            )
        )

        onboarding_sign_up.change_state(StateStatus.COMPLETED)
        onboarding_verify_email.change_state(StateStatus.COMPLETED)
        
        self.assertEqual(update_profile.state, StateStatus.IN_PROGRESS)
