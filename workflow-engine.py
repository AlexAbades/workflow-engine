from workflow import WorkFlow, Task, Link, StateStatus


if __name__ == "__main__":
    print(
        "This script is a use case of a workflow engine. \n"
        "The use State is an oboarding of a new user, as set in the example file.\n\n"
        "The onboarding workflow has 3 tasks: \n"
        "1. Sign Up\n"
        "2. Verify Email\n"
        "3. Add Profile \n"
    )
    
    input("Press Enter to continue...\n\n")
    
    print(
        "We first create a Worflow object, which at the begining it doesn't have any tasks and its initial state is pending."
    )
    onboarding = WorkFlow(name="Onboarding")
    print(
        f"Workflow: {onboarding.name}, State: {onboarding.state}, Tasks: {onboarding.tasks}\n\n"
    )
    
    input("Press Enter to continue...\n\n")
        
    print(
        "Afterwards, we can create Tasks instances, one per each task defined in the workflow.\n"
        "All tasks are created with a PENDING state.\n"
    )

    sign_up = Task("Sign Up", onboarding)
    verify_email = Task("Verify Email", onboarding)
    add_profile = Task("Add Profile", onboarding)
    print(
        "Tasks:\n"
        f"1. {sign_up.name.upper()} state: {sign_up.state}\n"
        f"2. {verify_email.name.upper()} state: {verify_email.state}\n"
        f"3. {add_profile.name.upper()} state: {add_profile.state}\n\n"
    )
    
    input("Press Enter to continue...\n\n")
    
    print(
        "All Tasks can have a link to another task or workflow, by default, no task is linked.\n"
    )
    print(
        "Tasks:\n"
        f"1. {sign_up.name.upper()} link: {sign_up._link}\n"
        f"2. {verify_email.name.upper()} link: {verify_email._link}\n"
        f"3. {add_profile.name.upper()} link: {add_profile._link}\n\n"
        "Predefined links can be applied to the tasks, such as:\n"
        "1. The task Sign Up Completed will trigger the Verify Email task to In Progress\n"
        "2. The task Verify Email Completed will trigger the Add Profile task to In Progress\n"
    )

    sign_up.add_link(
        Link(sign_up, StateStatus.COMPLETED, verify_email, StateStatus.IN_PROGRESS)
    )
    verify_email.add_link(
        Link(verify_email, StateStatus.COMPLETED, add_profile, StateStatus.IN_PROGRESS)
    )
    print(
        f"Sign Up link: {sign_up._link}, which points to an instance of class Link with the following attributes:\n"
    )

    print(
        f"Source: {sign_up._link.source.name}, Trigger State: {sign_up._link.trigger_state}, Target: {sign_up._link.target.name}, Update Target State: {sign_up._link.update_state}\n"
    )

    input("Press Enter to continue...\n\n")
    
    onboarding.add_task(sign_up)
    onboarding.add_task(verify_email)
    onboarding.add_task(add_profile)
    print(
        "We can then add the tasks to the workflow, and the workflow will be able to track the state of the tasks.\n"
        f"Workflow: {onboarding.name}, State: {onboarding.state}, Tasks: {[task.name for task in onboarding.tasks]}\n\n"
    )
    
    input("Press Enter to continue...\n\n")

    print(
        "Finally, we can now start changing the state of the tasks, for example, we can set the Sign Up task to COMPLETED "
        "and the target task will automatically change to IN PROGRESS\n"
    )
    sign_up.change_state(StateStatus.COMPLETED)
    print(
        f"- Task: {sign_up.name}, State: {sign_up.state}\n"
        f"- Task: {verify_email.name}, State: {verify_email.state}\n"
        f"- The onboarging workflow state is then updated to: {onboarding.state}\n\n"
    )
    
    input("Press Enter to continue...\n\n")

    print("Then the same process can be repeated for the Verify Email task:\n")
    verify_email.change_state(StateStatus.COMPLETED)
    print(
        f"- Task: {verify_email.name}, State: {verify_email.state}\n"
        f"- Task: {add_profile.name}, State: {add_profile.state}\n"
        f"- The onboarging workflow state is then updated to: {onboarding.state}\n\n"
        "Once all the tasks are completed, the workflow state will be COMPLETED:\n"
    )
    add_profile.change_state(StateStatus.COMPLETED)
    print(
        f"- Task: {add_profile.name}, State: {add_profile.state}\n"
        f"- The onboarging workflow state is then updated to: {onboarding.state}\n\n"
        "To run the tests, run the following command:\n"
        "python3 test/test_workflow.py\n"
    )
    
    
