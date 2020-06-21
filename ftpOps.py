import pysftp
import paramiko

class FtpOperation:

    def __init__(self):
        pass

    def createConnection(self, host, username, password):
        with pysftp.Connection('hostname', username='me', password='secret') as sftp:

            with sftp.cd('/allcode'):           # temporarily chdir to allcode
                sftp.put('/pycode/filename')  	# upload file to allcode/pycode on remote
                sftp.get('remote_file')         # get a remote file
      
