import unittest
from workflow import WorkFlow

class Test_TestWorkFlow(unittest.TestCase):

    def test_worfkflow_test(self):
        self.assertTrue(True)
        
    
    def test_worflow_add_task(self):

        onboarding = WorkFlow()
        
        tasks = ["Sign Up", "Verify Email"]
        
        onboarding.add_task(tasks[0])
        onboarding.add_task(tasks[1])
        
        self.assertEqual(onboarding._tasks, tasks)
        
        
