import json
import typing
from get_AS_PATH import load_json_file
from netaddr import IPAddress


def get_annouced_IP( AS_file:str, source:str ):
    AS = {}

    AS = load_json_file(AS_file)

    for l in open(source, "r"):
        annoucer = l.split('|')[6].split(' ')[-1]
        annoucer = "AS" + annoucer
        p = l.split('|')[5]
        ip = p.split('/')[0]
        if IPAddress(ip).version == 4:
            annouced = p
            if annoucer in AS:
                if "annouced_IP" in AS[annoucer]:
                    AS[annoucer]["annouced_IP"].append(annouced)
                else:
                    AS[annoucer].update({"annouced_IP":[annouced]})

        with open("AS.json", "w") as out:
            json.dump(AS, out)
