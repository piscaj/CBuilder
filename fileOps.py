import json

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
                print(i)
                if obj["Config"][i][_key] == int(_value):
                    print("Found the entry!!!!!!")
                    obj["Config"].pop(i)
                    break

        with open("config.json", "w") as file_write:
            file_write.write(json.dumps(obj, sort_keys=True,
                                        indent=4, separators=(',', ': ')))

    def addToFile(self):
        with open("config.json", "r") as read_file:
            obj = json.load(read_file)
            objNum = len(obj["Config"])
            obj["Config"].append({
                'Command': 'No device command',
                'Description': 'No description',
                'Number': objNum,
                'RoomName': 'New Room'
            })

        with open("config.json", "w") as file_write:
            file_write.write(json.dumps(obj, sort_keys=True,
                                        indent=4, separators=(',', ': ')))
            print("New item added to file...")
            return True

    def makeFile(self):
        data = {}
        data['Config'] = []
        data['Config'].append({
            'Command': 'No device command',
            'Description': 'No description',
            'Number': 0,
            'RoomName': 'Room Name'
        })
        with open('config.json', 'w') as write_file:
            json.dump(data, write_file)
            print("New file added...")
            return True

    def readFile(self):
        try:
            print("Trying Reading JSON file")
            with open("config.json", "r") as read_file:
                print("Converting JSON encoded data into Python dictionary")
                file_data = json.load(read_file)

                print("Decoded JSON Data From File")
                #for key, value in file_data.items():
                    #print(key, ":", value)
                print("Done reading json file")
        except FileNotFoundError:
            print("File not found...")
            succsess = makeFile()
            if succsess:
                file_data = readFile()
        return file_data
    