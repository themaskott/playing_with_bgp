import json
import typing
from get_AS_PATH import load_json_file
from netaddr import IPAdress


def get_annouced_IP( AS_file:str, source:str ):
    AS = {}

    AS = load_json_file(AS_file)

    for l in open(source, "r"):
        annoucer = l.split('|')[6].split(' ')[-1]
        annoucer = "AS" + annoucer
        p = l.split('|')[5]
        ip = p.split('/')[0]
        if IPAdress(ip).version == 4:
            annouced = p
            if annoucer in AS:
                AS[annoucer].update({"annouced_IP":annouced})

        with open("AS.json", "w") as out:
            json.dump(AS, out)
