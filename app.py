from wakeonlan import send_magic_packet
from pexpect import pxssh
from flask import Flask, request
from time import sleep
#import requests
import os

app = Flask(__name__)
@app.route('/wol', methods=['POST'])
def wol():
    # send magic packet to wake up the server [WORKING]
    wol_address = request.args.get('mac')
    send_magic_packet(wol_address)
    # wait for the computer to turn on before trying to unlock it
    timeout = int(request.args.get('timeout'))
    sleep(timeout)
    # unlock the disk on the server
    s = pxssh.pxssh()
    ssh_hostname = request.args.get('ip')
    ssh_username = "theredcyclops"
    # set the location of the ssh key file
    ssh_key = os.environ['SSH_KEY_FILE']
    # read the disk password from secret
    disk_password_file_name = os.environ['DISK_PASSWORD_FILE']
    disk_password_file = open(disk_password_file_name, "r")
    disk_password = disk_password_file.readline()
    disk_password_file.close()
#
    # Log in to the server
    if not s.login (server=ssh_hostname, username=ssh_username, ssh_key=ssh_key):
        print("SSH session failed on login :(")
        print(str(s))
        return "Failed"
    else:
        print("SSH session login successful")
    # Send the disk password to unlock the disk
        s.sendline (disk_password)
        s.prompt()         # match the prompt
        s.logout()
        return "Unlocked"
    #    # Check the server is running
    #sleep(10)
    #if not requests.get('http://localhost:8000'):
    #    print("Server is down after WOL :(")
    #else:
    #    print(":)")
#if __name__ == 'app':
#    app.run(host="0.0.0.0", port=8000, debug=True)