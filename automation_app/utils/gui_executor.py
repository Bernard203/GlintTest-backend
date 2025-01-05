import subprocess
import time

# Step 5: 执行 ADB 命令
def execute_adb_commands(operations, delay=10):
    """
    Execute a list of ADB commands with a delay between each command using subprocess.

    :param operations: A string containing multiple ADB commands.
    :param delay: The delay time in seconds between each ADB command execution (default: 2 seconds).
    """
    if operations:
        # Parse the ADB commands from the operations
        commands = operations.splitlines()
        for command in commands:
            if "ADB Command" in command:
                # Extract the adb command from the line
                adb_command = command.split(":")[-1].strip()
                adb_command = adb_command.split("(")[0].strip()
                adb_command = adb_command.strip("`")
                try:
                    print(f"Executing: {adb_command}")
                    result = subprocess.run(adb_command)
                except subprocess.CalledProcessError as e:
                    print(f"Error executing command {adb_command}: {e}")

                time.sleep(delay)
    else:
        print("No valid ADB commands to execute.")