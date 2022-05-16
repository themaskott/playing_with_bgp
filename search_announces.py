import igraph as ig
import pandas as pd
import numpy as np
import json
import re
import sys
from itertools import combinations
from string import ascii_lowercase

def load_df(source):
    df = pd.read_json(source, orient="index")
    df = df.rename_axis("AS").reset_index(level=0)

    return df


def unmerge_df(df):

    df2 = pd.DataFrame(columns = ['AS','prefix'])
    for i in range(len(df)):
        if isinstance(df.loc[i]["announced_IP"], list):
            for p in df.loc[i]["announced_IP"]:
                df2 = df2.append({'AS':df.loc[i]["AS"], 'prefix':p},ignore_index=True)

    return df2


def draw_graph(df):

    g = ig.Graph.DataFrame(df, directed=False, use_vids=False)

    return g



def scoring(s1: list[str], s2: list[str]) -> float:
    set1, set2 = set(s1), set(s2)
    return len(set1 & set2) / len(set1 | set2)

def compare_org_names(names):
    names = [[_ for _ in re.split(' |-|_', name)] for name in names]
    tagged_names = dict(zip(ascii_lowercase, names))

    scores = {
    (a, b): scoring(tagged_names[a], tagged_names[b])
    for a, b in combinations(tagged_names, 2)
    }

    return scores

def check_scores(scores):
    res = False
    for s in scores.values():
        if s <=  0.1:
            res = True
    return res

def search_inconsistancies(source):

    df = load_df(source)
    df2 = unmerge_df(df)

    g = draw_graph(df2)

    for i in g.vs:
        if len(i.neighbors()) > 1:
            if not i.attributes()['name'].startswith('AS'):
                ases = [ n.attributes()['name'] for n in i.neighbors() ]
                comp = set()
                for a in ases:
                    comp.add(df.loc[df['AS'] == a, "organisation"].values[0])
                if len(comp) > 1:
                    scores = compare_org_names(list(comp))
                    if check_scores(scores):
                        print(i.attributes()['name'], [ (n.attributes()['name'], df.loc[df['AS'] == n.attributes()['name'],'organisation'].values[0]) for n in i.neighbors() ])
