## PLAYING WITH BGP

Regroup some tools and scripts to manipulate extracted datas from the Internet and BGP annoucement.
Main goal is to generate formated outputs to be used elsewhere.

For now still in progress so do not expect much.


## Files used as inputs (ie datas/)

### 1 - `dump.txt`

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

### 2 -`autnums.html`

List of AS numbers associated with organisation and originated country.
Can be obtain at :https://www.cidr-report.org/as2.0/autnums.html
The script can also get that page from himself.


### 3 - `all.hijacks.json`

Json file produced by the tool TaBi (see bottom links).


## Output files (ie results/)

### 1 - `AS.json` and `AS_FR.json`

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

### 2 - `links_AS_fr.csv`

Links between French ASes and other ASes.

## Some features

```
usage: main.py [-h] [--ases | --path | --hijack] [--source SOURCE] [--format FORMAT] [--only-fr] [--fr FR] [--all ALL] [--dump DUMP] [--version]

Some tools to play with BGP and ASes

optional arguments:
  -h, --help       show this help message and exit
  --ases           Extract and computes ASes from sources
  --path           Extract and computes path anoucements from sources
  --hijack         Parse all.hijack.json for bgp hijacks
  --version        show program's version number and exit

AS:
  --source SOURCE  Source file
  --format FORMAT  Output format json or csv
  --only-fr        Extract only french ASes

PATH:
  --fr FR          French ASes file
  --all ALL        All ASes file
  --dump DUMP      Bview dump file

  ```

  `--ases` : produce `AS[_FR].json` files (or csv if asked)

  `--path` : parse AS path in `dump.txt` and produce `links_AS_fr.csv`, both previous json files are needed.

  `--hijack` : parse all.hijacks.json and try to reduce false positive hijack detections

  ## Useful tools and links

  `ANSSI - mabo` : https://github.com/ANSSI-FR/mabo

  `ANSSI - tabi` : https://github.com/ANSSI-FR/tabi

  BGP full view and update from RRC01 colectors : https://data.ris.ripe.net/rrc01/

  ASes registration names : https://www.cidr-report.org/as2.0/autnums.html

  Hurricane Toolkit : https://bgp.he.net/
