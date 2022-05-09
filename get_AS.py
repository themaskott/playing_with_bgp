import sys, requests, json
from html.parser import HTMLParser
import typing

class MyHTMLParser(HTMLParser):
    """
    HTML parser for https://www.cidr-report.org/as2.0/autnums.html
    Feeds AS dictionnary with {AS number : AS full name}
    """
    extract_only_fr = False
    isASNum = False
    isASName = False
    ASNum = ""
    ASName = ""
    ASCountry = ""
    AS = {}

    def handle_starttag(self, tag, attrs):
        if tag == "a": self.isASNum = True

    def handle_endtag(self, tag):
        if tag == "a": self.isASName = True

    def handle_data(self, data):
        if self.isASNum:
            self.ASNum = data.strip()
            self.isASNum = False
        elif self.isASName:
            l = data.replace("\n","").strip()
            self.ASName = " ".join(l.split(",")[0:-1])
            self.ASCountry = l.split(",")[-1].strip()
            if self.extract_only_fr:
                if self.ASCountry == "FR":
                    self.AS.update({self.ASNum : {"organisation" : self.ASName, "country" : self.ASCountry}})
            else:
                self.AS.update({self.ASNum : {"organisation" : self.ASName, "country" : self.ASCountry}})
            self.isASName = False

def update_AS()->str:
    """
    Get last update of AS number - AS names
    """
    url = "https://www.cidr-report.org/as2.0/autnums.html"
    r = requests.get(url, verify=False)
    return r.content.decode()


def extract_AS(source:str, output_format:str, extract_only_fr:bool, out_dir:str):
    """
    Apply parser to input
    Output is a json or cvs
    """
    parser = MyHTMLParser()
    parser.extract_only_fr = extract_only_fr
    parser.feed(source)

    # named according desired parameters
    out_name = out_dir + "AS_FR."  + output_format if extract_only_fr else out_dir + "AS." + output_format

    if output_format == "csv":
        with open(out_name, "w") as out:
            for l in parser.AS:
                out.write(";".join( _ for _ in [l, parser.AS[l]['organisation'], parser.AS[l]['country']]))
                out.write("\n")
    else:
        with open(out_name, "w") as out:
            json.dump(parser.AS, out)
