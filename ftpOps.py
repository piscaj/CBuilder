import pysftp
import paramiko

class FtpOperation:

    def __init__(self):
        pass

    def writeFile(self, host, username, password, path,):
        with pysftp.Connection('hostname', username='me', password='secret') as sftp:

            with sftp.cd(path):           # temporarily chdir to allcode
                sftp.put('/pycode/filename')  	# upload file to allcode/pycode on remote
                #sftp.get('remote_file')         # get a remote file
      
    def getFile(self, host, username, password, path, file):
        with pysftp.Connection('hostname', username='me', password='secret') as sftp:

            with sftp.cd(path):           # temporarily chdir to allcode
                #sftp.put('/pycode/filename')  	# upload file to allcode/pycode on remote
                sftp.get(file)         # get a remote file
    