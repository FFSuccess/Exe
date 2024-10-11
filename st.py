import win32com.client


def create_scheduled_task_powershell(powershell_command, task_name="MyPSTask"):
    scheduler = win32com.client.Dispatch("Schedule.Service")
    scheduler.Connect()

    root_folder = scheduler.GetFolder("\\")

    # Create a new task definition
    task_def = scheduler.NewTask(0)

    # Set task registration info (author)
    reg_info = task_def.RegistrationInfo
    reg_info.Description = "Run PowerShell command after login"
    reg_info.Author = "Your Name"

    # Set the task to trigger after logon
    trigger_collection = task_def.Triggers
    trigger = trigger_collection.Create(1)  # 1 means logon trigger
    trigger.Id = "LogonTrigger"

    # Set the action for the task (running the PowerShell command)
    action_collection = task_def.Actions
    action = action_collection.Create(0)  # 0 means action to execute something
    action.Path = "powershell.exe"  # Path to PowerShell executable
    action.Arguments = f'-Command "{powershell_command}"'

    # Set task settings
    settings = task_def.Settings
    settings.Enabled = True
    settings.StartWhenAvailable = True
    settings.Hidden = False

    # Register the task
    root_folder.RegisterTaskDefinition(
        task_name,  # Task name
        task_def,
        6,  # Create or update the task (TASK_CREATE_OR_UPDATE)
        None,  # User
        None,  # Password
        3,  # Logon type (TASK_LOGON_INTERACTIVE_TOKEN)
        None  # No additional settings
    )

    print(f"Scheduled task '{task_name}' created successfully.")


if __name__ == "__main__":
    # PowerShell command you want to run after login
    powershell_command = "Write-Host 'Task Scheduled!'"

    create_scheduled_task_powershell(powershell_command)
