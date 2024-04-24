import pexpect
import concurrent.futures
import threading
import os
import sys

# Configuration variables
username = 'user'  # Replace with your SSH username
password = 'cisco'  # Replace with your SSH password
max_workers = 100

# SSH function to connect to a device and execute commands
def ssh_connect_run_commands(device, commands):
    # Start an SSH session
    child = pexpect.spawn(f'ssh {username}@{device}')

    # Uncomment the next line to see the output in real time
    # child.logfile = sys.stdout.buffer

    try:
        child.expect('assword:')
        child.sendline(password)
        child.expect('#')

        child.sendline('term len 0')
        child.expect('#')

        for command in commands:
            # Send the command
            child.sendline(command)
            child.expect('#')

            # Grab the output of the command
            output = child.before.decode()

            # Replace spaces with dashes and remove newline characters 
            # for the filename
            command_filename = command.replace(' ', '-').replace('\n', '')
            filename = f"{device}__{command_filename}.txt"

            # Save the output to a file
            with open(filename, 'w') as file:
                file.write(output)
                print(f"Output written to {filename}")

    except pexpect.EOF:
        print(f"Connection closed for {device}")
    except pexpect.TIMEOUT:
        print(f"Timeout error occurred for {device}")
    except pexpect.exceptions.ExceptionPexpect as e:
        print(f"Failed to connect to {device}, due to {e}")
    finally:
        child.close()


# Read the list of devices and commands
def read_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to handle each device in a separate thread
def handle_device(device, commands):
    print(f"Starting session for {device}")
    ssh_connect_run_commands(device, commands)

# Main function
def main():
    # Read devices and commands from files
    devices = read_file('devices.txt')
    commands = read_file('commands.txt')

    # Use ThreadPoolExecutor to run SSH sessions in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) \
		as executor:
        futures = {executor.submit(handle_device, device, \
			commands): device for device in devices}
        concurrent.futures.wait(futures)

if __name__ == '__main__':
    main()

