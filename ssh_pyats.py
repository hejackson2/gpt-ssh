from genie.testbed import load
from concurrent.futures import ThreadPoolExecutor
import os

max_workers = 100

# Load the testbed file
testbed = load('testbed.yaml')

# Read the list of commands from the file
def read_commands(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to connect to a device, execute commands, and write output to files
def run_commands_on_device(device_name, commands):
    # Find the device in the testbed
    device = testbed.devices[device_name]
    
    # Connect to the device
    device.connect()

    for command in commands:
        # Execute the command
        output = device.execute(command)

        # Replace spaces with dashes for the filename
        command_filename = command.replace(' ', '-')
        filename = f"{device_name}__{command_filename}.txt"

        # Save the output to a file
        with open(filename, 'w') as file:
            file.write(output)
            print(f"Output written to {filename}")

    # Disconnect from the device
    device.disconnect()

def main():
    # Read commands from the file
    commands = read_commands('commands.txt')

    # Use ThreadPoolExecutor to run tasks in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_commands_on_device, device_name, commands)
                   for device_name in testbed.devices]

if __name__ == '__main__':
    main()
