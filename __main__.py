from wakeonlan import send_magic_packet
from pexpect import pxssh
from flask import Flask, request
#import requests
import os

app = Flask(__name__)
@app.route('/wol', methods=['POST'])
def wol():
    p = request.get_json()
    # send magic packet to wake up the server [WORKING]
    wol_address = p['mac']
    send_magic_packet(wol_address)
    
    # unlock the disk on the server
    s = pxssh.pxssh()
    ssh_hostname = p['ip']
    ssh_username = "root"
    # using a key instead of password for ssh, read from default .ssh/
    # read the disk password from secret
    disk_password_file_name = os.environ['DISK_PASSWORD_FILE']
    disk_password_file = open(disk_password_file_name, "r")
    disk_password = disk_password_file.readline()
    disk_password_file.close()

    return disk_password
    ## Log in to the server
    #if not s.login (ssh_hostname, ssh_username):
    #    print("SSH session failed on login :(")
    #    print(str(s))
    #else:
    #    print("SSH session login successful")
    ## Send the disk password to unlock the disk
    #    s.sendline (disk_password)
    #    s.prompt()         # match the prompt
    #    s.logout()
    ##    # Check the server is running
    ##sleep(10)
    ##if not requests.get('http://localhost:8000'):
    ##    print("Server is down after WOL :(")
    ##else:
    ##    print(":)")
        
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)