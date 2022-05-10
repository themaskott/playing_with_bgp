# PLAYING WITH BGP


<p align="center">
  <img src="img/meme.jpg" />
</p>


Regroup some tools and scripts to manipulate extracted datas from the Internet and BGP annoucement.
Main goal is to generate formated outputs to be used elsewhere.

For now still in progress so do not expect much.


## Files used as inputs (ie datas/)

#### 1 - `dump.txt`

Human readable output of a parsed bview thanks to bgpdump (https://github.com/RIPE-NCC/bgpdump)

bview : https://data.ris.ripe.net/rrc01/


```
./tools/bgpdump/bgpdump -M -O dump.txt datas/bview.20220406.0800.gz

tail dump.txt
TABLE_DUMP2|04/06/22 08:00:00|B|5.57.80.210|8218|223.255.254.0/24|8218 6461 7473 3758 55415|IGP
TABLE_DUMP2|04/06/22 08:00:00|B|5.57.81.186|6894|223.255.254.0/24|6894 4637 4657 55415 55415 55415 55415 55415 55415 55415|IGP
TABLE_DUMP2|04/06/22 08:00:00|B|5.57.81.21|6908|223.255.254.0/24|6908 7473 3758 55415|IGP
TABLE_DUMP2|04/06/22 08:00:00|B|5.57.81.210|31742|223.255.254.0/24|31742 4657 55415 55415 55415 55415 55415 55415 55415|IGP
TABLE_DUMP2|04/06/22 08:00:00|B|5.57.81.216|35266|223.255.254.0/24|35266 6939 4657 55415 55415 55415 55415 55415 55415 55415|IGP
TABLE_DUMP2|04/06/22 08:00:00|B|5.57.81.76|36924|223.255.254.0/24|36924 35280 6461 7473 3758 55415|IGP
TABLE_DUMP2|04/06/22 08:00:00|B|2001:7f8:4::f2d7:1|62167|fd00:ada:2345:b0ba::/126|62167 3356|IGP
TABLE_DUMP2|04/06/22 08:00:00|B|2001:7f8:4::f2d7:1|62167|fd00:2804:ad4:1::/125|62167 3356|IGP
TABLE_DUMP2|04/06/22 08:00:00|B|2001:7f8:4::f2d7:1|62167|fd00:2804:ad4:1::10/125|62167 3356|IGP
TABLE_DUMP2|04/06/22 08:00:00|B|2001:7f8:4::3:2be1:1|207841|fddd:1194:1194:1194::/64|207841|INCOMPLETE

```

#### 2 -`autnums.html`

List of AS numbers associated with organisation and originated country.
Can be obtain at :https://www.cidr-report.org/as2.0/autnums.html
The script can also get that page from himself.


#### 3 - `all.hijacks.json`

Json file produced by the tool TaBi (see bottom links).


## Output files (ie results/)

#### 1 - `AS.json` and `AS_FR.json`

A json formated file generated from the fromer `autnums.html`. Can be generated in a `csv` format too.
`AS_FR.json` is the same one but containing only French ASes.

```
cat AS.json | jq | head -n 21
{
  "AS0": {
    "organisation": "-Reserved AS-",
    "country": "ZZ"
  },
  "AS1": {
    "organisation": "LVLT-1",
    "country": "US"
  },
  "AS2": {
    "organisation": "UDEL-DCN",
    "country": "US"
  },
  "AS3": {
    "organisation": "MIT-GATEWAYS",
    "country": "US"
  },
  "AS4": {
    "organisation": "ISI-AS",
    "country": "US"
  },
  ```

#### 2 - `links_AS_fr.csv`

Links between French ASes and other ASes.

## Some features

```
usage: playing_with_bgp.py [-h] [--ases | --path | --hijack | --ip] [--source_as SOURCE_AS] [--format FORMAT] [--only-fr] [--fr FR] [--all ALL] [--dump DUMP] [--source_hjk SOURCE_HJK] [--all_as ALL_AS]
               [--source_ip SOURCE_IP] [--version]

Some tools to play with BGP and ASes

optional arguments:
  -h, --help            show this help message and exit
  --ases                Extract and computes ASes from sources
  --path                Extract and computes path anoucements from sources
  --hijack              Parse all.hijack.json for bgp hijacks
  --ip                  Complete an AS.json file with annouced prefixes
  --version             show program's version number and exit

AS:
  --source_as SOURCE_AS
                        Source file, default from web
  --format FORMAT       Output format json or csv, default json
  --only-fr             Extract only french ASes, default all

PATH:
  --fr FR               French ASes file, default AS_FR.json
  --all ALL             All ASes file, default AS.json
  --dump DUMP           Bview dump file, default dump.txt

HIJACK:
  --source_hjk SOURCE_HJK
                        Source file, all.hijacks.json
  --all_as ALL_AS       All ASes file, default AS.json

IP:
  --source_ip SOURCE_IP
                        Bview dump file, default dump.txt
  ```

  `--ases` : produce `AS[_FR].json` files (or csv if asked)

  `--path` : parse AS path in `dump.txt` and produce `links_AS_fr.csv`, both previous json files are needed.

  `--hijack` : parse all.hijacks.json and try to reduce false positive hijack detections

  `--ip` : update existing AS.json with IPv4 prefixes announced in a bview dump file (dump.txt)


## Work Flow

#### 1 - Collecting datas

- Download BGP full view ( `bview.YYYYMMDD.hhmm.gz` ) from the deisred colector, and needed updates
- Download AS list from https://www.cidr-report.org/as2.0/autnums.html (or the script can retrieve it from itself)

#### 2 - Extract datas

- With `tabi` :

`tabi -j 8 rrc01 datas/ bview.20160101.0000.gz updates.20160101.0000.gz`

Will produce following files into the datas directory :

    - all.defaults.json.gz that contains all default routes seen by TaBi
    - all.routes.json.gz that contains all routes monitored
    - all.hijacks.json.gz that contains all BGP prefix conflicts

Trick for running `tabi` :
```bash
#!/usr/bin/sh
TABI="/full/path/to/taby/inside/python2env/tabi_env/bin/tabi"
export MABO_PATH="/full/path/to/mabo/mabo"
```
`mabi` takes around 25 minutes with 6 cores to parse bview.

At the end of the parsing, `tabi` crashes, but output files are OK.


- With `bgpdump`

`bgpdump -M -O datas/dump.txt datas/bview.20220406.0800.gz`

Will produce the `dump.txt` file into the right format.

Can also be obtain thanks to `mabo`, using the`--legacy` output, but so far tests were slowers.


#### 3 - Generate needed files

- `AS.json` and `AS_FR.json`

`playing_with_bgp.py --ases`

Will take `autnums.html` as an input to generate `AS.json`

`playing_with_bgp.py --ases --only-fr`

Will take `autnums.html` as an input to generate `AS_FR.json`


- `links_AS_fr.csv`

`playing_with_bgp.py --path`

Will take `AS.json`, `AS_FR.json` and `dump.txt` to generate csv file of links between any French AS and foreign AS.

- Complete `AS.json`

`playing_with_bgp.py --ip`

Will take dump.txt and AS.json, to produce a new AS.json including annouced prefixes per AS.

**Caution** : those prefixes are from a bview dump, so it reveals real annoucements and no who is the legitimate owner of a prefix.



## Useful tools and links

  `ANSSI - mabo` : https://github.com/ANSSI-FR/mabo

  `ANSSI - tabi` : https://github.com/ANSSI-FR/tabi

  `bgpdump` : https://github.com/RIPE-NCC/bgpdump

  BGP full view and update from RRC01 colectors : https://data.ris.ripe.net/rrc01/

  ASes registration names : https://www.cidr-report.org/as2.0/autnums.html

  Hurricane Toolkit : https://bgp.he.net/
