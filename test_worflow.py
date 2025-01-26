import unittest
from workflow import WorkFlow, Task, StateStatus

class Test_TestWorkFlow(unittest.TestCase):

    def test_worfkflow_test(self):
        self.assertTrue(True)
        
    
    def test_worflow_add_task(self):

        onboarding = WorkFlow()
        
        tasks = ["Sign Up", "Verify Email"]
        
        onboarding.add_task(tasks[0])
        onboarding.add_task(tasks[1])
        
        self.assertEqual(onboarding._tasks, tasks)
        
        
    def test_worfkflow_state_on_changed_task_state(self):
        onboarding = WorkFlow() 
        
        onboarding.add_task(Task("Sign Up", onboarding))
        onboarding.add_task(Task("Verify Email", onboarding))
        
        onboarding.tasks[0].change_state(StateStatus.IN_PROGRESS)
        
        self.assertEqual(onboarding.state, StateStatus.IN_PROGRESS)
        