"""
Regrouping some tools to manipulate BGP annoucements and AS properties
Under build so not much to expect

@Maskott
28/04/2022

"""

# import from python
import argparse

# custom import
import check_datas
import get_AS
import get_AS_PATH
import parse_hijack
import get_IP
import search_announces
# globals

DATAS_DIR = ""
RESULTS_DIR = ""

def getArgParser():
    """
    Manage command line arguments
    """

    argparser = argparse.ArgumentParser( add_help=True, description="""Some tools to play with BGP and ASes""" )

    group_action = argparser.add_mutually_exclusive_group()
    group_action.add_argument( "--ases", action="store_true", help="Extract and computes ASes from sources")
    group_action.add_argument( "--path", action="store_true", help="Extract and computes path anoucements from sources")
    group_action.add_argument( "--hijack", action="store_true", help="Parse all.hijack.json for bgp hijacks")
    group_action.add_argument( "--ip", action="store_true", help="Complete an AS.json file with annouced prefixes")


    group_as = argparser.add_argument_group("AS")
    group_as.add_argument( "--web", action="store_true", help="Retrieve AS numbers and name from web or local file")
    group_as.add_argument( "--format", action="store", default="json", help="Output format json or csv, default json" )
    group_as.add_argument( "--only-fr", action="store_true", default=False, help="Extract only french ASes, default all" )


    argparser.add_argument( "--version", action="version", version="%(prog)s beta")

    return argparser


if __name__ == "__main__":

    args = getArgParser().parse_args()

    DATAS_DIR, RESULTS_DIR = check_datas.check_directories()
    AS_ok, AS_FR_ok, dump_ok, autnums_ok, hijack_ok, links_ok = check_datas.check_sources()

    if args.ases:
        if args.web:
            get_AS.extract_AS( get_AS.update_AS(), args.format, args.only_fr, RESULTS_DIR )
        else:
            if autnums_ok:
                get_AS.extract_AS( open(  ).read(), args.format, args.only_fr, RESULTS_DIR )
            else:
                print(f"[-] datas/autnums.html not present")

    if args.path:
        if not AS_ok: print("[-] AS.json not present in results, please generate it using --ases")
        if not AS_FR_ok: print("[-] AS_FR.json not present in results, please generate it using --ases")
        if not dump_ok: print("[-] dump.txt not present in datas")

        if AS_ok and AS_FR_ok and dump_ok:
            get_AS_PATH.get_path( "results/AS_FR.json", "results/AS.json", "datas/dump.txt", RESULTS_DIR )


    if args.hijack:
        if not hijack_ok: print("[-] all.hijack.json not present in datas")
        if not AS_ok: print("[-] AS.json not present in results, please generate it using --ases")

        if AS_ok and hijack_ok:
            parse_hijack.search_hijacker(DATAS_DIR, RESULTS_DIR)
            search_announces.search_inconsistancies( "results/AS.json" )


    if args.ip:
        if not dump_ok: print("[-] dump.txt not present in datas")
        if not AS_ok: print("[-] AS.json not present in results, please generate it using --ases")
        if not AS_FR_ok: print("[-] AS_FR.json not present in results, please generate it using --ases --only-fr")

        if AS_ok and dump_ok:
            get_IP.get_annouced_IP( "results/AS.json", "datas/dump.txt" )
            get_IP.get_annouced_IP( "results/AS_FR.json", "datas/dump.txt" )
