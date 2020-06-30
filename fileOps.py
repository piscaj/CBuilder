import json
import os
import sys
import uuid

class FileOperation:

    def __init__(self):
        pass

    def numberOfItems(self):
        with open("config.json", "r") as read_file:
            obj = json.load(read_file)
            objNum = len(obj["Config"])
            return objNum

    def deleteFromFile(self, _key, _value):
        with open("config.json", "r") as read_file:
            obj = json.load(read_file)
            #print("Searching", _key, _value)
            for i in range(len(obj["Config"])):
                #print(i)
                if obj["Config"][i][_key] == int(_value):
                    #print("Found the entry!!!!!!")
                    obj["Config"].pop(i)
                    break

        with open("config.json", "w") as file_write:
            file_write.write(json.dumps(obj, sort_keys=True,
                                        indent=4, separators=(',', ': ')))

    def addToFile(self):
        with open("config.json", "r") as read_file:
            obj = json.load(read_file)
            #objNum = len(obj["Config"])
            #objNum = objNum = len(obj["Config"])
            objNum = int(str(uuid.uuid4().int)[-16:])
            obj["Config"].append({
                'Command': 'No device command',
                'Description': 'No description',
                'Number': objNum,
                'Name': 'My new command'
            })

        with open("config.json", "w") as file_write:
            file_write.write(json.dumps(obj, sort_keys=True,
                                        indent=4, separators=(',', ': ')))
            #print("New item added to file...")
            return objNum

    def makeFile(self):
        data = {}
        data['Connect'] = []
        data['Connect'].append({
            'Host': '',
            'User': 'crestron',
            'Pass': '',
            'Directory': '/user'
        })
        data['Config'] = []
        data['Config'].append({
            'Command': 'No device command',
            'Description': 'No local config file was found, so this file was created',
            'Number': int(str(uuid.uuid4().int)[-16:]),
            'Name': 'My new command'
        })
        app_folder = os.path.dirname(os.path.abspath(__file__))
        with open(app_folder+'/config.json', 'w') as write_file:
            json.dump(data, write_file)
            #print("New file added...")
            return True

    def readFile(self):
        try:
            #print("Trying Reading JSON file")
            with open("config.json", "r") as read_file:
                #print("Converting JSON encoded data into Python dictionary")
                file_data = json.load(read_file)

                #print("Decoded JSON Data From File")
                # for key, value in file_data.items():
                #print(key, ":", value)
                #print("Done reading json file")
        except FileNotFoundError:
            #print("File not found...")
            succsess = self.makeFile()
            if succsess:
                file_data = self.readFile()
        return file_data
