import subprocess
import sys

def run_jlink_commands(commands, jlink_path="JLinkExe"):
    """
    Automates the execution of commands in the J-Link Commander tool.

    :param commands: List of commands to execute in J-Link Commander.
    :param jlink_path: Path to the J-Link Commander executable (default: "JLinkExe").
    """
    # Prepare to track TDO values
    tdo_values = []

    # Prepare the command string to be passed to J-Link Commander
    command_string = ""
    for command in commands:
        if "read TDO" in command:
            # Prompt the user for TDO value
            while True:
                user_input = input("Enter TDO value (1 or 0) based on hardware: ")
                if user_input in {"1", "0"}:
                    tdo_values.append(user_input)
                    break
                else:
                    print("Invalid input. Please enter 1 or 0.")
        else:
            command_string += command + "\n"

    command_string += "exit\n"

    try:
        # Run the J-Link Commander process
        process = subprocess.run(
            [jlink_path],
            input=command_string,
            text=True,
            capture_output=True
        )

        # Print the output from J-Link Commander
        print("J-Link Commander Output:")
        print(process.stdout)

        # Check for errors
        if process.returncode != 0:
            print("Error occurred:")
            print(process.stderr)

    except FileNotFoundError:
        print(f"Error: J-Link Commander executable not found at '{jlink_path}'")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Print the TDO values entered by the user
    print("\nTDO Values Entered:")
    print(", ".join(tdo_values))


def read_commands_from_file(file_path):
    """
    Reads J-Link commands from a file.

    :param file_path: Path to the file containing J-Link commands.
    :return: List of commands.
    """
    try:
        with open(file_path, "r") as file:
            commands = [line.split("#")[0].strip() for line in file if line.strip() and not line.strip().startswith("#")]
        return commands
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Check if the user provided a file path as an argument
    if len(sys.argv) != 2:
        print("Usage: python connect.py <commands_file>")
        sys.exit(1)

    # Get the file path from the command-line arguments
    commands_file_path = sys.argv[1]

    # Read commands from the file
    jlink_commands = read_commands_from_file(commands_file_path)

    print(jlink_commands)

    # Path to the J-Link Commander executable (update this if necessary)
    jlink_executable_path = "/Applications/SEGGER/JLink/JLinkExe"

    # Run the commands
    run_jlink_commands(jlink_commands, jlink_executable_path)