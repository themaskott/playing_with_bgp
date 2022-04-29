# import from python
from os import path, mkdir
import typing


def check_directories() -> str:
    if not path.isdir("datas"): mkdir("datas", 0o755)
    if not path.isdir("results"): mkdir("results", 0o755)
    return "datas/", "results/"

def check_sources() -> bool:
    return path.isfile("datas/AS.json"), path.isfile("datas/AS_FR.json"), path.isfile("datas/dump.txt")
