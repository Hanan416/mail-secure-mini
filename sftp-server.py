import os
import socket
import sys

import paramiko
from paramiko.py3compat import input

# Setting up the client configuration
UseGSSAPI = True
DoGSSAPIKeyExchange = True


userInput = input(str("Enter user in the format <userName>@<hostname>:<port> \n"))

if userInput.find("@") >= 0:
    userName, hostName = userInput.split("@")

else:
    print("user entered in wrong format, exiting ...")
    sys.exit(1)


if hostName.find(":") >= 0:
    hostName, portStr = hostName.split(":")
    port = int(portStr)

else:
    print("user entered in wrong format, exiting ...")
    sys.exit(1)

password = None
hostkeytype = None
hostkey = None

try:
    host_keys = paramiko.util.load_host_keys(os.path.expanduser("~/.ssh/known_hosts"))
except IOError:
    try:
        # try ~/ssh/ too, because windows can't have a folder named ~/.ssh/
        host_keys = paramiko.util.load_host_keys(os.path.expanduser("~/ssh/known_hosts"))
    except IOError:
        print("*** Unable to open host keys file")
        host_keys = {}


if hostName in host_keys:
    hostkeytype = host_keys[hostName].keys()[0]
    hostkey = host_keys[hostName][hostkeytype]
    print("Using host key of type %s" % hostkeytype)


try:
    t = paramiko.Transport((hostName, port))
    t.connect(
        hostkey,
        userName,
        password,
        gss_host=socket.getfqdn(hostName),
        gss_auth=UseGSSAPI,
        gss_kex=DoGSSAPIKeyExchange,
    )
    sftp = paramiko.SFTPClient.from_transport(t)

    # dirlist on remote host
    dirList = sftp.listdir(".")
    print("Dirlist: %s" % dirList)

    # copy this demo onto the server
    try:
        sftp.mkdir("demo_sftp_folder")
    except IOError:
        print("(assuming demo_sftp_folder/ already exists)")
    with sftp.open("demo_sftp_folder/README", "w") as f:
        f.write("This was created by demo_sftp.py.\n")
    with open("demo_sftp.py", "r") as f:
        data = f.read()
    sftp.open("demo_sftp_folder/demo_sftp.py", "w").write(data)
    print("created demo_sftp_folder/ on the server")

    # copy the README back here
    with sftp.open("demo_sftp_folder/README", "r") as f:
        data = f.read()
    with open("README_demo_sftp", "w") as f:
        f.write(data)
    print("copied README back here")

    # BETTER: use the get() and put() methods
    sftp.put("demo_sftp.py", "demo_sftp_folder/demo_sftp.py")
    sftp.get("demo_sftp_folder/README", "README_demo_sftp")

    t.close()

except Exception as e:
    print("*** Caught exception: %s: %s" % (e.__class__, e))
    try:
        t.close()
    except:
        pass
    sys.exit(1)
