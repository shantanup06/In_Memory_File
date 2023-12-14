import os
import re

class InMemoryFileSystem:
    def __init__(self):
        self.current_directory = "/"
        self.file_system = {"/": {"type": "directory", "contents": {}}}

    def execute_command(self, command):
        command_parts = command.split()

        if command_parts[0] == "mkdir":
            self.mkdir(command_parts[1])
        elif command_parts[0] == "cd":
            self.cd(command_parts[1])
        elif command_parts[0] == "ls":
            self.ls(command_parts[1] if len(command_parts) > 1 else None)
        elif command_parts[0] == "grep":
            self.grep(command_parts[1], command_parts[2])
        elif command_parts[0] == "cat":
            self.cat(command_parts[1])
        elif command_parts[0] == "touch":
            self.touch(command_parts[1])
        elif command_parts[0] == "echo":
            self.echo(command_parts[1], ' '.join(command_parts[2:]))
        elif command_parts[0] == "mv":
            self.mv(command_parts[1], command_parts[2])
        elif command_parts[0] == "cp":
            self.cp(command_parts[1], command_parts[2])
        elif command_parts[0] == "rm":
            self.rm(command_parts[1])
        else:
            print("Invalid command")

    def mkdir(self, directory_name):
        new_directory_path = os.path.join(self.current_directory, directory_name)
        if new_directory_path not in self.file_system:
            self.file_system[new_directory_path] = {"type": "directory", "contents": {}}
        else:
            print("Directory already exists")

    def cd(self, path):
        if path == "/":
            self.current_directory = "/"
        elif path == "..":
            self.current_directory = os.path.dirname(self.current_directory)
        elif path.startswith("/"):
            # Absolute path
            if path in self.file_system and self.file_system[path]["type"] == "directory":
                self.current_directory = path
            else:
                print("Directory not found")
        else:
            # Relative path
            target_path = os.path.join(self.current_directory, path)
            if target_path in self.file_system and self.file_system[target_path]["type"] == "directory":
                self.current_directory = target_path
            else:
                print("Directory not found")

    def ls(self, path=None):
        target_path = path if path else self.current_directory
        if target_path in self.file_system and self.file_system[target_path]["type"] == "directory":
            contents = self.file_system[target_path]["contents"]
            relative_paths = [os.path.relpath(item, self.current_directory) for item in contents.keys()]
            print("Contents of {}: {}".format(target_path, relative_paths))
        else:
            print("Directory not found")

    def grep(self, pattern, file_path):
        if file_path in self.file_system and self.file_system[file_path]["type"] == "file":
            file_contents = self.file_system[file_path]["contents"]
            matches = re.findall(pattern, file_contents)
            print("Matches for '{}': {}".format(pattern, matches))
        else:
            print("File not found")

    def cat(self, file_path, return_contents=False):
        if file_path in self.file_system and self.file_system[file_path]["type"] == "file":
            file_contents = self.file_system[file_path]["contents"]
            if return_contents:
                return file_contents
            else:
                print(file_contents)
        else:
            print("File not found")

    def touch(self, file_name):
        new_file_path = os.path.join(self.current_directory, file_name)
        if new_file_path not in self.file_system:
            self.file_system[new_file_path] = {"type": "file", "contents": ""}
        else:
            print("File already exists")

    def echo(self, file_path, text):
        if file_path in self.file_system and self.file_system[file_path]["type"] == "file":
            self.file_system[file_path]["contents"] = text
        else:
            print("File not found")

    def mv(self, source_path, destination_path):
        if source_path in self.file_system:
            item = self.file_system.pop(source_path)
            destination_path = os.path.join(destination_path, os.path.basename(source_path))
            self.file_system[destination_path] = item
        else:
            print("Source path not found")

    def cp(self, source_path, destination_path):
        if source_path in self.file_system:
            item = self.file_system[source_path]
            destination_path = os.path.join(destination_path, os.path.basename(source_path))
            self.file_system[destination_path] = item.copy()
        else:
            print("Source path not found")

    def rm(self, path):
        if path in self.file_system:
            del self.file_system[path]
        else:
            print("Path not found")

# Example usage:
file_system = InMemoryFileSystem()
while True:
    command = input("Enter command: ")
    if command == "exit":
        break
    file_system.execute_command(command)

