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
    group_as.add_argument( "--source_as", action="store", default="web", help="Source file, default from web" )
    group_as.add_argument( "--format", action="store", default="json", help="Output format json or csv, default json" )
    group_as.add_argument( "--only-fr", action="store_true", default=False, help="Extract only french ASes, default all" )

    group_path = argparser.add_argument_group("PATH")
    group_path.add_argument( "--fr", action="store", default="results/AS_FR.json", help="French ASes file, default AS_FR.json" )
    group_path.add_argument( "--all", action="store", default="results/AS.json", help="All ASes file, default AS.json" )
    group_path.add_argument( "--dump", action="store", default="datas/dump.txt", help="Bview dump file, default dump.txt" )


    group_hjk = argparser.add_argument_group("HIJACK")
    group_hjk.add_argument( "--source_hjk", action="store", default="datas/all.hijacks.json", help="Source file, all.hijacks.json" )
    group_hjk.add_argument( "--all_as", action="store", default="results/AS.json", help="All ASes file, default AS.json" )

    group_ip = argparser.add_argument_group("IP")
    group_ip.add_argument( "--source_ip", action="store", default="datas/dump.txt", help="Bview dump file, default dump.txt" )

    argparser.add_argument( "--version", action="version", version="%(prog)s beta")

    return argparser


if __name__ == "__main__":

    args = getArgParser().parse_args()

    DATAS_DIR, RESULTS_DIR = check_datas.check_directories()


    if args.ases:
        if args.source_as == "web":
            get_AS.extract_AS( get_AS.update_AS(), args.format, args.only_fr, RESULTS_DIR )
        else:
            if check_datas.check_sources_ases( args.source ):
                get_AS.extract_AS( open(args.source).read(), args.format, args.only_fr, RESULTS_DIR )
            else:
                print(f"[-] {args.source} not present")

    if args.path:
        AS_ok, AS_FR_ok, dump_ok, = check_datas.check_sources_path( args.fr, args.all, args.dump )
        if not AS_ok: print("[-] AS.json not present in results")
        if not AS_FR_ok: print("[-] AS_FR.json not present in results")
        if not dump_ok: print("[-] dump.txt not present in datas")

        if AS_ok and AS_FR_ok and dump_ok:
            get_AS_PATH.get_path( RESULTS_DIR + args.fr, RESULTS_DIR + args.all, DATAS_DIR + args.dump, RESULTS_DIR )


    if args.hijack:
        hijack_ok, AS_ok = check_datas.check_sources_hijack( args.source_hjk, args.all_as )
        if not hijack_ok: print("[-] all.hijack.json not present in datas")
        if not AS_ok: print("[-] AS.json not present in datas")

        if AS_ok and hijack_ok:
            parse_hijack.search_hijacker(DATAS_DIR, RESULTS_DIR)


    if args.ip:
        get_IP.get_annouced_IP( "results/AS.json", args.source_ip )
