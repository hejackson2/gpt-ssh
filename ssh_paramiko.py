import paramiko
import concurrent.futures
import os

# Ensure you have paramiko installed: pip install paramiko

# Configuration variables
username = 'user'  # Replace with your SSH username
password = 'cisco'  # Replace with your SSH password or use key authentication
max_workers = 100

# SSH function to connect to a device and execute commands
def ssh_connect_run_commands(device, commands):
    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # run through commands, each command requires a unique ssh session
    for command in commands:
        # Connect to the device
        try:
            ssh_client.connect(hostname=device, username=username, \
                    password=password, look_for_keys=False,\
                    allow_agent=False)
            print(f"Connected to {device}")

            stdin, stdout, stderr = ssh_client.exec_command(command)
            output = stdout.read().decode()

            # Replace spaces with dashes and remove newline characters
            # for the filename
            command_filename = command.replace(' ', '-').replace('\n', '')
            filename = f"{device}__{command_filename}.txt"

            # Save the output to a file
            with open(filename, 'w') as file:
                file.write(output)
                print(f"Output written to {filename}")

        except paramiko.AuthenticationException:
            print(f"Authentication failed when connecting to {device}")
        except paramiko.SSHException as sshException:
            print(f"Could not establish SSH connection: {sshException}")
        except Exception as e:
            print(f"Failed to connect to {device}, due to {e}")
        finally:
            ssh_client.close()
            print(f"Connection closed for {device}")


# Read the list of devices and commands
def read_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Main function
def main():
    # Read devices and commands from files
    devices = read_file('devices.txt')
    commands = read_file('commands.txt')

    # Use ThreadPoolExecutor to run SSH sessions in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) \
            as executor:
        futures = {executor.submit(ssh_connect_run_commands, device, \
                commands): device for device in devices}
        for future in concurrent.futures.as_completed(futures):
            device = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Device {device} generated an exception: {e}")

if __name__ == '__main__':
    main()

