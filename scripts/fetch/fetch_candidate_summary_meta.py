"""
run:
    $ python3 -m scripts.fetch.fetch_candidate_summary_meta

Fetches from SOURCE_URL
Parses the HTML to get column format of the FEC candidate summaries
"""
from scripts.settings import FETCHED_DIR
from os.path import join
SOURCE_URL = 'http://www.fec.gov/finance/disclosure/metadata/DataDictionaryWEBALL.shtml'
FETCHED_FILE_PATH = join(FETCHED_DIR, 'fec-metadata-DataDictionaryWEBALL.shtml')

def download():
    import requests
    resp = requests.get(SOURCE_URL)
    with open(FETCHED_FILE_PATH, 'w') as o:
        o.write(resp.text)

def parse():
    """
    expects FETCHED_FILE_PATH to exist
    prints YAML formatted schema to screen
    """
    from lxml import html
    from collections import OrderedDict
    from re import search
    import rtyaml
    # open stashed file
    txt = open(FETCHED_FILE_PATH).read()
    doc = html.fromstring(txt)
    schema = OrderedDict()
    for tr in doc.cssselect('table tr')[1:]:
        tds = [t.text_content().strip() for t in tr.xpath('./td')]
        cname = tds[0]
        d = schema[cname] = OrderedDict()
        d['description'] = tds[1]
        d['nullable'] = True if tds[3] == 'Y' else False
        if tds[5]: # optional description field
            d['description'] += ' -- ' + tds[5]
        ctype = tds[4]
        if 'VARCHAR' in ctype:
            d['type'] = 'String'
            d['length'] = int(search(r'(?<=\()\d+', ctype).group())
        elif 'Number' in ctype:
            d['type'] = 'Float'
            d['length'] = [int(_d) for _d in search(r'(\w+),(\w+)', ctype).groups()]
        elif 'DATE(MM/DD/YYYY)' == ctype:
            d['type'] = 'Date'
            d['format'] = '%m/%d/%Y'
        else:
            raise Exception("Unexpected column data type:", ctype)
    # print to screen
    print(rtyaml.dump(schema))


def run():
    download()
    parse()


if __name__ == '__main__':
    print("Downloading into", FETCHED_FILE_PATH)
    run()
