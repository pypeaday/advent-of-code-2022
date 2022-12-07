""" day 7

"""

from pathlib import Path
from typing import Dict, List


def get_commands() -> List[List[str]]:
    # raw = Path("./data/day7.sample").read_text()
    raw = Path("./data/day7.data").read_text()
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


#     def total_size_of_children(self, total: int = 0):
#         if not self.children:
#             return total
#         else:
#             for child in self.children:
#                 total += child.total_size_of_children(total)
#             return total

#     def total_size_with_children(self):
#         total = self.total_size()
#         children_total = self.total_size_of_children()
#         return total + children_total


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Device:
    def __init__(self):
        self.pwd = Directory("/")
        self.directories: Dict[str, Directory] = {r"/": self.pwd}
        self.old_pwd = None

    def cddotdot(self, s: str):
        if self.pwd.name == "/":
            print(f"at / already, but old_pwd was {self.old_pwd.name}")
            return 0
        print(f"changing directory from {self.pwd.name} to {self.pwd.parent.name}")
        self.old_pwd = self.pwd
        self.pwd = self.pwd.parent
        return 0

    def cd(self, s: str):
        if s[-2:] == "..":
            return self.cddotdot(s)
        else:
            directory_name = s.split(" ")[-1]
            self.old_pwd = self.pwd
            self.pwd = self.directories.get(directory_name, Directory(directory_name))
            self.pwd.parent = (
                self.old_pwd if self.pwd.parent is None else self.pwd.parent
            )
            self.old_pwd.children.update({self.pwd.name: self.pwd})
            print(f"changing directory from {self.old_pwd.name} to {self.pwd.name}")
            return 0
        breakpoint()
        return 1

    def ls(self, elements: List[str]):
        for element in elements:
            dtype = "directory" if element.split(" ")[0] == "dir" else "file"
            name = element.split(" ")[1]
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
            target = cmd.split("\n")[-1]
            device.cd(target)
        if "ls" in cmd.split("\n")[0]:
            output = cmd.split("\n")[1:]
            device.ls(output)

    return device


def main():
    device = setup_device()

    total = 0
    for directory in device.directories.values():
        if directory.total_contents_size() <= 100_000:
            total += directory.total_contents_size()

    print(f"{total=}")
