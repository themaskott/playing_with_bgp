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

# globals

INPUT_DIR = ""
OUTPUT_DIR = ""

def getArgParser():
    """
    Manage command line arguments
    """

    argparser = argparse.ArgumentParser( add_help=True, description="""Some tools to play with BGP and ASes""" )

    group_action = argparser.add_mutually_exclusive_group()
    group_action.add_argument( "--as", action="store_true", help="Extract and computes ASes from sources")
    group_action.add_argument( "--path", action="store_true", help="Extract and computes path anoucements from sources")


    group_as = argparser.add_argument_group("AS")
    group_as.add_argument( "--source", action="store", default="autnums.html", help="Source file" )
    group_as.add_argument( "--format", action="store", default="json", help="Output format json or csv" )
    group_as.add_argument( "--only-fr", action="store_true", default=False, help="Extract only french ASes" )

    group_path = argparser.add_argument_group("PATH")
    group_path.add_argument( "--fr", action="store", default="AS_FR.json", help="French ASes file" )
    group_path.add_argument( "--all", action="store", default="AS.json", help="All ASes file" )
    group_path.add_argument( "--dump", action="store", default="dump.txt", help="Bview dump file" )

    argparser.add_argument( "--version", action="version", version="%(prog)s beta")

    return argparser


if __name__ == "__main__":

    args = getArgParser().parse_args()

    INPUT_DIR, OUTPUT_DIR = check_datas.check_directories()
    AS_file, AS_FR_file, dump_file = check_datas.check_sources()
