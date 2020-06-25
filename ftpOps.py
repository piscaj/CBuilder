import pysftp
import os


class FtpOperation:

    def __init__(self):
        pass

    def writeFile(self, _host,  _username, _password, _path, _file):
        print("[SFTP]Attempting connection to:", _host)
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            with pysftp.Connection(_host, username=_username, password=_password, cnopts=cnopts) as sftp:
                print("[SFTP]Client conencted...")
                with sftp.cd(_path):
                    app_folder = os.path.dirname(os.path.abspath(__file__))
                    sftp.put(app_folder+'/'+_file)
                    print("[SFTP]File sent...")
                    return "Success"

        except pysftp.ConnectionException as err:
            print("[SFTP]ERROR]", err)
            return err
        except pysftp.CredentialException as err:
            print("[SFTP]ERROR]", err)
            return err
        except pysftp.SSHException as err:
            print("[SFTP]ERROR]", err)
            return err
        except pysftp.AuthenticationException as err:
            print("[SFTP]ERROR]", err)
            return err
        except pysftp.PasswordRequiredException as err:
            print("[SFTP]ERROR]", err)
            return err
        except pysftp.HostKeysException as err:
            print("[SFTP]ERROR]", err)
            return err
        except:
            err = "Unknown ERROR has occured..."
            print("[SFTP]ERROR]")
            return err

    def getFile(self, _host, _username, _password, _path, _file):
        print("[SFTP]Attempting connection to:", _host)
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            with pysftp.Connection(_host, username=_username, password=_password, cnopts=cnopts) as sftp:
                print("[SFTP]Client conencted...")
                with sftp.cd(_path):
                    app_folder = os.path.dirname(os.path.abspath(__file__))
                    sftp.get(_file, localpath=app_folder+"/"+_file)
                    print("[SFTP]File retrieved...")
                    return "Success"
        except pysftp.ConnectionException as err:
            print("[SFTP]ERROR]", err)
            return err
        except pysftp.CredentialException as err:
            print("[SFTP]ERROR]", err)
            return err
        except pysftp.SSHException as err:
            print("[SFTP]ERROR]", err)
            return err
        except pysftp.AuthenticationException as err:
            print("[SFTP]ERROR]", err)
            return err
        except pysftp.PasswordRequiredException as err:
            print("[SFTP]ERROR]", err)
            return err
        except pysftp.HostKeysException as err:
            print("[SFTP]ERROR]", err)
            return err
        except:
            err = "Unknown ERROR has occured..."
            print("[SFTP]ERROR]")
            return err
