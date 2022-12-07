""" day 7

"""

from pathlib import Path
from typing import Dict, List, Set


class Directory:
    def __init__(self, name: str):
        self.name = name
        self.files: Dict[str, File] = {}
        self.parent: Directory = None
        self.children: List[Directory] = []

    def total_size(self):
        return sum([file.size for file in self.files.values()])


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Device:
    def __init__(self):
        self.directories: Dict[str, Directory] = dict()
        self.pwd = Directory("/")
        self.old_pwd = None
        self.cmd = "cd"

    def determine_line(self, s: str):
        if s[0] == "$":
            return "command"
        elif s[:2] == "ls":
            return "ls"
        elif s[0] == "d":
            return "dir"
        elif s[0].isdigit():
            return "file"

    def cddotdot(self, s: str):
        if self.pwd.name == "/":
            print("at / already")
            return 0
        self.old_pwd = self.pwd
        self.pwd = self.pwd.parent
        return 0

    def cd(self, s: str):
        if s[-2:] == "..":
            return self.cddotdot(s)
        else:
            directory_name = s.split(" ")[-1]
            self.old_pwd = self.pwd
            self.pwd = directories.get(directory_name, Directory(directory_name))
        print(f"problem with {s}")
        return 1

    def ls(self, s: str):
        line = self.determine_line(s)
        if line == "dir":
            self.directories.add(Directory(s.split(' ')[-1]))
        elif line == "file":
            filename = s.split(" ")[1]
            size = int(s.split(" "))[0]
            self.pwd.files.update({filename: File(filename, size)})


directories = [
    Directory(x)
    for x in Path("./data/day7.sample").read_text().split("\n")
    if x[:3] == "dir"
]

for directory in directories:
    # for each directory, parse input again and find all lines between `cd directory` and cd anything else
    for line in Path("./data/day7.sample").read_text().split("\n"):
        if line == f"$ cd {directory.name}":

