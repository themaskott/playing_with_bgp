# import from python
from os import path, mkdir
import typing


def check_directories() -> str:
    if not path.isdir("datas"): mkdir("datas", 0o755)
    if not path.isdir("results"): mkdir("results", 0o755)
    return "datas/", "results/"

def check_sources(datas:str, results:str) -> bool:
    return path.isfile( results + "AS.json"), path.isfile( results + "AS_FR.json"), path.isfile(datas + "dump.txt"), path.isfile(datas + "all.hijacks.json")

def check_sources_ases(source:str)->bool:
    return path.isfile( source )


def check_sources_path(fr:str, all:str, dump:str) -> bool:
    return path.isfile( fr ), path.isfile( all ), path.isfile( dump )

def check_sources_hijack(source:str, all:str ) -> bool:
    return path.isfile( source ), path.isfile( all )

def check_sources_ip( dump:str) -> bool:
    return path.isfile( results + "AS.json"), path.isfile( dump )
