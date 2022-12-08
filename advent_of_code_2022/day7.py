""" day 7

"""

from pathlib import Path
from typing import Dict, List


def get_commands() -> List[List[str]]:
    raw = Path("./data/day7.data").read_text()
    raw = Path("./data/day7.sample").read_text()
    commands = [x for x in raw.split("$") if x]
    return [c.strip() for c in commands]


# class Node:
#     def __init__(
#         self, name: str, parent: Node, is_file: bool, size: Optional[int] = None
#     ):
#         self.name = name
#         self.parent = parent
#         self.is_file = is_file
#         self.size = size
#         self.children: List[Node] = []

#     @property
#     def is_root(self):
#         return self.name == "/"


class Directory:
    def __init__(self, name: str):
        self.name = name
        self.files: Dict[str, File] = {}
        self.parent: Directory = None
        self.children: Dict[str, Directory] = dict()

    @property
    def size(self):
        return self.size_of_files + self.size_of_directories

    @property
    def size_of_files(self):
        return sum([f.size for f in self.files.values()])

    @property
    def size_of_directories(self):
        return sum([d.size for d in self.children.values()])


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Device:
    def __init__(self):
        self.pwd = None
        self.directories: Dict[str, Directory] = {}
        self.old_pwd = None
        self.initialized = False
        self.disk_space_available = 70_000_000
        self.disk_space_required = 30_000_000

    @property
    def disk_space_used(self):
        return self.directories["/"].size

    @property
    def disk_space_used_by_directories_smaller_than_100_001(self):
        total = 0
        for directory in self.directories.values():
            if directory.size <= 100_000:
                total += directory.size
        return total

    @property
    def disk_space_free(self):
        return self.disk_space_available - self.disk_space_used

    def cddotdot(self, s: str):
        self.old_pwd = self.pwd
        self.pwd = self.pwd.parent
        return 0

    def get_file_name(self, s: str):
        """Need to keep full path in mind since directories with different
        parents can have same names"""
        if self.pwd.name == "/":
            return "/" + s.split(" ")[-1]
        return self.pwd.name + "/" + s.split(" ")[-1]

    def get_directory_name(self, s: str):
        """Need to keep full path in mind since directories with different
        parents can have same names"""
        if self.pwd.name == "/":
            return "/" + s.split(" ")[-1]
        return self.pwd.name + "/" + s.split(" ")[-1]

    def cd(self, s: str):

        if s == "/" and not self.initialized:
            self.directories["/"] = Directory("/")
            self.pwd = self.directories.get("/")
            self.old_pwd = self.pwd
            self.pwd.parent = None
            self.initialized = True
            return 0
        if s == "/":
            directory_name = "/"
        else:
            directory_name = self.get_directory_name(s)

        if s[-2:] == "..":
            return self.cddotdot(s)
        else:
            self.old_pwd = self.pwd
            self.pwd = self.directories.get(directory_name, Directory(directory_name))
            self.pwd.parent = (
                self.old_pwd if self.pwd.parent is None else self.pwd.parent
            )
            self.old_pwd.children.update({self.pwd.name: self.pwd})
            return 0
        return 1

    def ls(self, elements: List[str]):
        for element in elements:
            dtype = "directory" if element.split(" ")[0] == "dir" else "file"
            # TODO: I think this is broken for files where below I do File(name)... gotta look into this
            if dtype == "directory":
                name = self.get_directory_name(element.split(" ")[1])
                if name not in [k for k in self.directories.keys()]:
                    self.directories[name] = Directory(name)
            elif dtype == "file":
                name = self.get_file_name(element.split(" ")[1])
                size = int(element.split(" ")[0])
                self.pwd.files.update({name: File(name, size)})


def setup_device():

    device = Device()

    for cmd in get_commands():
        if "cd" in cmd.split("\n")[0]:
            target = cmd.split(" ")[-1]
            device.cd(target)
            print(
                f"cd-ing to {target} from {device.old_pwd.name}. Directory: {device.pwd.name} "
            )
        if "ls" in cmd.split("\n")[0]:
            output = cmd.split("\n")[1:]
            device.ls(output)
            print(f"ls {output=}")

    return device


def main():
    device = setup_device()
    print(f"{device.disk_space_used_by_directories_smaller_than_100_001=}")

    spaces = []
    directory: Direcctory
    space_needed = device.disk_space_required - device.disk_space_used
    # breakpoint()
    for directory in device.directories.values():
        if directory.size >= space_needed:
            spaces.append(directory.size)
    print(f"Smallest directory size = {min(spaces)}")
    return device
