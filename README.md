# gpt-ssh

## Initial prompt to GPT-4
This is an attempt to modify the output from a request to gpt-4 to the following prompts:

_Please write a python3 program that will read a list of IOS device names from one file and a list of IOS commands from another file.  Have then ssh into each device, issue those commands and capture the output from those commands into a separate file for each device - command tuple.  For example, if one device name is rtr3 and one command is 'show interface description' the file create from running that command on that device would be "rtr3__show-interface-description.txt"    Please write the program so that it can send commands to multiple devices at the same time.  That is to ask, use async.io or threads to allow multiprocessing_

This resulting program it provided did not fully work at first and had to be modified.  The issue was that the programs stopped after the first command.  This was because paramkio was closing the ssh connection after the command was issued.

## pexpect
I modified the ask to include a different method:

_can you re-write this program to use the pexpect module rather than the paramiko module?_

This resulted in a different, but similar, program that worked.   I modified this to use a single SSH connection for all programs to improve the efficiency.

## pyATS / genie
I next asked the system to use pyATS as well.

_can you rewrite this script to use pyATS rather than pexpect?_

This program worked out of the box, so to speak.

## asyncssh
I finally asked it to re-write the program using asyncssh:

_Can you rewrite the initial script with using asyncssh instead of paramiko?_

Unfortunately, this doesn't seem to work as of the time this was written.  I have not been able to correct this.


## Timing
Of the three working methods, the use of pexpect is by far the quickest.  I believe this is because I modified it to use a single connection for all commands given to a device.  The paramiko and pyATS seem to use a different connection for each command.

