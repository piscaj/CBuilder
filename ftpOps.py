import pysftp
import json
class FtpOperation:

    def __init__(self):
        pass

    def writeFile(self, _host, _username, _password, _path, _file):
        print(_username,_password)
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None  
        with pysftp.Connection(_host, username=_username, password=_password, cnopts=cnopts) as sftp:
            with sftp.cd(_path):         
                sftp.put("."+'/'+_file)
      
    def getFile(self, host, username, password, path, file):
        with pysftp.Connection(host, username=username, password=password) as sftp:

            with sftp.cd(path):           # temporarily chdir to allcode
                #sftp.put('/pycode/filename')  	# upload file to allcode/pycode on remote
                sftp.get(file)         # get a remote file
    