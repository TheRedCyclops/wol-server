from wakeonlan import send_magic_packet
from pexpect import pxssh
from flask import Flask, request
from time import sleep
import paramiko
#import requests
import os

app = Flask(__name__)
@app.route('/wol', methods=['POST'])
def wol():
    # send magic packet to wake up the server [WORKING]
    wol_address = request.args.get('mac')
    send_magic_packet(wol_address)
    # set the hostname
    ssh_hostname = request.args.get('ip')
    # set the username
    ssh_username = request.args.get('username')
    if ssh_username is None:
        ssh_username = 'root'
    # set the location of the ssh key file
    ssh_key = os.environ['SSH_KEY_FILE']
    # read the disk password from secret
    disk_password_file_name = os.environ['DISK_PASSWORD_FILE']
    disk_password_file = open(disk_password_file_name, "r")
    disk_password = disk_password_file.readline()
    disk_password_file.close()
    # Init the ssh session
    ssh = paramiko.SSHClient()
    # Set the known hosts file
    ssh.load_system_host_keys(os.environ['KNOWN_HOSTS_FILE'])
    # Log in to the server
    # wait for the specified time before trying to connect to the computer
    try:
        wait = int(request.args.get('wait'))
    except TypeError:
        wait=None
    if wait:
        sleep(wait)
    # set the max amount of tries to connect to the computer before giving up
    try:
        max_tries = int(request.args.get('max_tries'))
    except TypeError:
        max_tries = None
    # unlock the disk on the server
    if max_tries:
        tries=0
        while True: 
            try:
                if tries == max_tries:
                    return "Failed to connect to the server", 504
                    break
                ssh.connect(hostname=ssh_hostname, username=ssh_username, key_filename=ssh_key)
                tries += 1
            except:
                print("Failed to connect on attempt " + str(tries) + ", trying again..")
            else:
                print("Established SSH connection")
                break
    else:
        return "Malformed request.", 400
    # Send the disk password to unlock the disk
    ssh.exec_command(disk_password)
    return "Unlocked", 200
    try
        ssh.close()
    except:
        pass
    #    # Check the server is running
    #sleep(10)
    #if not requests.get('http://localhost:8000'):
    #    print("Server is down after WOL :(")
    #else:
    #    print(":)")

#app.run(host="0.0.0.0", port=8000, debug=True)