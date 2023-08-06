import json


class JsonStorage:
    def __init__(self, project_root, json_directory_under_root):
        self.project_root = str(project_root)
        self.folder_location_specified = str(json_directory_under_root)
        self.json_directory = (self.project_root + self.folder_location_specified)

    def read_json_file(self, file_name):
        try:
            with open(self.json_directory + "/" + file_name) as json_file:
                data = json.load(json_file)
                return data
        except FileNotFoundError:
            print("File was not found!")
        except TypeError as _error:
            print(f"Type Error: {_error}")
            print(f"File name: {file_name}")

    def write_json_file(self, data, file_name):
        try:
            with open(self.json_directory + "/" + file_name, "w") as file:
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            print("File was not found!")
        except TypeError as _error:
            print(f"Type Error: {_error}")
            print(f"File name: {file_name}")

    def read_json_file_table(self, file_name, table: str):
        try:
            return self.read_json_file(file_name)[table]
        except KeyError:
            print("Table wasn't found!")
        except TypeError as _error:
            print(f"Type Error: {_error}")
            print(f"File name: {file_name}, Table name: {table}")

    def write_json_file_table(self, file_name, table: str, input_data):
        data = {table: input_data}
        try:
            self.write_json_file(data, file_name)
        except KeyError:
            print("Table wasn't found!")
        except TypeError as _error:
            print(f"Type Error: {_error}")
            print(f"File name: {file_name}, Table name: {table}")
