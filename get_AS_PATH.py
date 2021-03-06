import json
import typing

AS_fr = {}
AS = {}
neighbor = {}

def test_inconsistency(source:str):
    """
    Check for errors in dump.txt file
    """
    announcedAS = set()
    announcerAS = set()
    for line in open(source, "r"):
        AS = line.split("|")[4]
        ASpath = line.split("|")[6]
        if AS != ASpath.split(" ")[0]:
            print("Wrong announce : ",AS, ASpath)
        announcedAS.update( _ for _ in ASpath.split(" "))
        announcerAS.update(AS)

    for a in announcerAS:
        if a not in announcedAS:
            print("Alone : ",a)

def load_json_file(source:str)->dict:
    """
    Load a json file into a dict
    """
    with open(source, "r") as jf:
        return json.load(jf)


def check_neighbor(l:str):
    """
    Count nationalities of french ASes
    """
    AS1, AS2 = l.split(' ')
    if AS1 in AS_fr and AS2 not in AS_fr and AS2 in AS:
        country = AS[AS2]['country']
        if country in neighbor:
            neighbor[country] += 1
        else:
            neighbor.update({country:1})
    elif AS2 in AS_fr and AS1 not in AS_fr and AS1 in AS:
        country = AS[AS1]['country']
        if country in neighbor:
            neighbor[country] += 1
        else:
            neighbor.update({country:1})

def get_path(AS_FR_file:str, AS_file:str, source:str, out_dir:str):
    """
    Parse pathes announced in dump.txt files
    Extracted connected ASes if one of the twoe if French
    """
    global AS, AS_fr, neighbor

    nodes = set()
    links = set()

    AS_fr = load_json_file(AS_FR_file)
    AS = load_json_file(AS_file)

    for line in open(source, "r"):
        ASpath = line.split("|")[6].split(" ")
        if len(ASpath) > 1:
            for i in range(len(ASpath) - 1 ):
                # replace { } for AS {21212}
                AS1 = "AS"  + ASpath[i].replace('{','').replace('}','')
                AS2 = "AS"  + ASpath[i+1].replace('{','').replace('}','')
                # link between french AS and another AS (fr or not)
                if AS1 in AS_fr or AS2 in AS_fr:
                    nodes.add(AS1)
                    nodes.add(AS2)
                    links.add(AS1 + " " + AS2)

    # neighbor nationality and save links to csv
    with open( out_dir + "links_AS_fr.csv","w") as csv_out:
        for l in links:
            check_neighbor(l)
            csv_out.write(l.replace(" ", ",")  +"\n")

    print("Nodes : ", len(nodes))
    print("Links : ", len(links))

    # Sorted  and print neighbor dict
    sorted_tuples = sorted(neighbor.items(), key=lambda item: item[1])
    sorted_dict = {k: v for k, v in sorted_tuples}
    print("FR neighbor :\n", sorted_dict)
