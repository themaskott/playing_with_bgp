import json
import typing
from get_AS_PATH import load_json_file
from netaddr import IPAddress


def get_annouced_IP( AS_file:str, source:str ):
    """
    Update an AS.json file with announced prefixes per AS
    Announces are extracted out of a dump.txt file (ie bview)
    """
    AS = {}

    AS = load_json_file(AS_file)

    for l in open(source, "r"):
        announcer = l.split('|')[6].split(' ')[-1]
        announcer = "AS" + announcer
        p = l.split('|')[5]
        ip = p.split('/')[0]
        if IPAddress(ip).version == 4:
            announced = p
            if announcer in AS:
                if "announced_IP" in AS[announcer] and announced not in AS[announcer]["announced_IP"]:
                    AS[announcer]["announced_IP"].append(announced)
                else:
                    AS[announcer].update({"announced_IP":[announced]})

    with open("results/AS.json", "w") as out:
        json.dump(AS, out)
