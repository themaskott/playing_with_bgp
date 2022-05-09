#/usr/bin/python3

import json, re

def compare_ASnames(AS1:str, AS2:str)->bool:
    """
    Search for common word in two AS names
    Reduce false positives
    """
    list1 = re.split(" |-", AS1)
    list2 = re.split(" |-", AS2)
    for word in list1:
        if len(word) > 2 and word in list2: return True
    return False

def parse_json_hijack(all_hijack_json:str)->set:
    """
    Parse the all.hijacks.json output of mabo tool
    Extract owner AS and annoucer AS (possible hijacker)
    """
    conflicts = set()
    with open(all_hijack_json) as jf:
        for line in jf:
            data = json.loads(line)
            if data["type"] == "F" or data["type"] == "U":
                conflicts.add("AS" + str(data["announce"]["asn"]) + " " + "AS" + str(data["asn"]))
    return conflicts

def search_hijacker(datas:str, results:str):
    """
    Determine hijacks from previously parsed suspicious annoucement
    """

    conflicts = parse_json_hijack(datas + "all.hijacks.json")

    with open(results + "AS.json", "r") as jf:
        AS = json.load(jf)

    for c in conflicts:
        annoucer, owner = c.split(" ")
        try:
            if AS[owner]['organisation'] != AS[annoucer]['organisation'] and not compare_ASnames(AS[owner]['organisation'], AS[annoucer]['organisation']):
                print("{} ({}) has hijacked {} ({})".format(AS[annoucer], annoucer, AS[owner], owner))
        except:
            print("{} undetermined conflict with {}".format(annoucer, owner))
