import sys, json

AS_fr = {}
AS = {}
neighbor = {}

def test_inconsistency(source):
    annoucedAS = set()
    annoucerAS = set()
    for line in open(source, "r"):
        AS = line.split("|")[4]
        ASpath = line.split("|")[6]
        if AS != ASpath.split(" ")[0]:
            print("Wrong annouce : ",AS, ASpath)
        annoucedAS.update( _ for _ in ASpath.split(" "))
        annoucerAS.update(AS)

    for a in annoucerAS:
        if a not in annoucedAS:
            print("Alone : ",a)

def load_french_AS(source):
    with open(source, "r") as jf:
        return json.load(jf)

def load_all_AS(source):
    with open(source, "r") as jf:
        return json.load(jf)

def check_neighbor(l):
    AS1, AS2 = l.split(' ')
    if AS1 in AS_fr and AS2 not in AS_fr:
        country = AS[AS2].split(',')[-1].strip()
        if country in neighbor:
            neighbor[country] += 1
        else:
            neighbor.update({country:1})
    elif AS2 in AS_fr and AS1 not in AS_fr:
        country = AS[AS1].split(',')[-1].strip()
        if country in neighbor:
            neighbor[country] += 1
        else:
            neighbor.update({country:1})

def get_path(source):
    nodes = set()
    links = set()

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

    # neighbor nationality and save links to cvs
    with open("datas/links_AS_fr.csv","w") as csv_out:
        for l in links:
            check_neighbor(l)
            csv_out.write(l.replace(" ", ",")  +"\n")

    print("Nodes : ", len(nodes))
    print("Links : ", len(links))

    sorted_tuples = sorted(neighbor.items(), key=lambda item: item[1])
    sorted_dict = {k: v for k, v in sorted_tuples}
    print("FR neighbor :\n", sorted_dict)
