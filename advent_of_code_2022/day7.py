""" day 7

"""

from pathlib import Path
from typing import Dict, List


def get_commands() -> List[List[str]]:
    raw = Path("./data/day7.data").read_text()
    # raw = Path("./data/day7.sample").read_text()
    commands = [x for x in raw.split("$") if x]
    return [c.strip() for c in commands]


class Directory:
    def __init__(self, name: str):
        self.name = name
        self.files: Dict[str, File] = {}
        self.parent: Directory = None
        self.children: Dict[str, Directory] = dict()

    @property
    def contents(self):
        return [*[f for f in self.files.values()], *[d for d in self.children.values()]]

    def total_file_size(self):
        return sum([file.size for file in self.files.values()])

    def total_child_directory_size(self):
        return sum([d.total_file_size() for d in self.children.values()])

    def total_contents_size(self):
        return self.total_file_size() + self.total_child_directory_size()


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
        total = 0
        for directory in self.directories.values():
            total += directory.total_contents_size()
        return total

    @property
    def disk_space_used_by_directories_smaller_than_100_001(self):
        total = 0
        for directory in self.directories.values():
            if directory.total_contents_size() <= 100_000:
                total += directory.total_contents_size()
        return total

    @property
    def disk_space_free(self):
        return self.disk_space_available - self.disk_space_used

    def cddotdot(self, s: str):
        self.old_pwd = self.pwd
        self.pwd = self.pwd.parent
        return 0

    def get_directory_name(self, s: str):
        """Need to keep full path in mind since directories with different
        parents can have same names"""
        return self.pwd.name + s.split(" ")[-1]

    def cd(self, s: str):

        if s == "/" and not self.initialized:
            self.directories["/"] = Directory("/")
            self.pwd = self.directories.get("/")
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
            name = self.get_directory_name(element.split(" ")[1])
            if dtype == "directory":
                if name not in [k for k in self.directories.keys()]:
                    self.directories[name] = Directory(name)
            elif dtype == "file":
                size = int(element.split(" ")[0])
                self.pwd.files.update({name: File(name, size)})


def setup_device():

    device = Device()

    for cmd in get_commands():
        if "cd" in cmd.split("\n")[0]:
            target = cmd.split(" ")[-1]
            device.cd(target)
        if "ls" in cmd.split("\n")[0]:
            output = cmd.split("\n")[1:]
            device.ls(output)

    return device


def main():
    device = setup_device()
    print(f"{device.disk_space_used_by_directories_smaller_than_100_001=}")

    for directory in device.directories:
        space_needed = device.disk_space_required - device.disk_space_used
        if device.disk_space_available == directory:
            ...
