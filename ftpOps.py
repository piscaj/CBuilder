import pysftp
import os

class FtpOperation:

    def __init__(self):
        pass

    def writeFile(self, _host,  _username, _password, _path, _file):
        print("[SFTP]Attempting connection to:",_host)
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None  
            with pysftp.Connection(_host, username=_username, password=_password, cnopts=cnopts) as sftp:
                print("[SFTP]Client conencted...")
                with sftp.cd(_path):
                    app_folder = os.path.dirname(os.path.abspath(__file__))         
                    sftp.put(app_folder+'/'+_file)
                    print("[SFTP]File sent...")
                    
        except pysftp.ConnectionException as err:
            print("[SFTP]ERROR]",err)
        except pysftp.CredentialException as err:
            print("[SFTP]ERROR]",err)
        except pysftp.SSHException as err:
            print("[SFTP]ERROR]",err)
        except pysftp.AuthenticationException as err:
            print("[SFTP]ERROR]",err)
        except pysftp.PasswordRequiredException as err:
            print("[SFTP]ERROR]",err)
        except pysftp.HostKeysException as err:
            print("[SFTP]ERROR]",err)
        except :
            print("[SFTP]ERROR]")
        
      
    def getFile(self, host, username, password, path, file):
        with pysftp.Connection(host, username=username, password=password) as sftp:

            with sftp.cd(path):           # temporarily chdir to allcode
                #sftp.put('/pycode/filename')  	# upload file to allcode/pycode on remote
                sftp.get(file)         # get a remote file
    