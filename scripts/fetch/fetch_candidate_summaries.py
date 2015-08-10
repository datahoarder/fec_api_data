"""
run:
    $ python3 -m scripts.fetch.fetch_candidate_summaries

Fetches from http://www.fec.gov/finance/disclosure/ftpsum.shtml
Converts pipe delimited files to CSVs
"""
from scripts.settings import setup_space
from scripts.settings import FETCHED_DIR, FETCHED_CANDSUMS_DIR
from contextlib import closing
# the Requests library doesn't do FTP, thus, urlopen
from urllib.request import urlopen, Request
from os.path import basename, join, splitext, join
from io import BytesIO
from zipfile import ZipFile
import csv


YEARS = list(range(1996, 2018, 2)) # 2018 is excluded
HEADERS_URL = 'http://www.fec.gov/finance/disclosure/metadata/webl_header_file.csv'


# Note that this script only returns files from the House and Senate Candidate
# Financial Summaries. You can modify the output of this helper function to get
# the other types of zip files
def url_for_year(year):
    """e.g. year=2014, result: 'ftp://ftp.fec.gov/FEC/2014/webl14.zip'"""
    y = str(year)
    return 'ftp://ftp.fec.gov/FEC/%s/webl%s.zip' % (y, y[2:])


if __name__ == '__main__':
    setup_space()
    ##
    # get the headers
    # the FEC site returns a 406 unless minimal headers are provided
    hreq = Request(HEADERS_URL,  headers = {'Accept':'text/html'})
    htxt = urlopen(hreq).read().decode().strip()
    # save for record keeping
    with open(join(FETCHED_DIR, 'fec-cand-webl_header_file.csv'), 'w') as f:
        f.write(htxt)
    headers = htxt.split(',')
    # we'll add a "cycle" column to the top
    headers.insert(0, 'cycle')

    ## Download and write the data
    # Iterate through YEARS to fetch all the FTP files
    for yr in YEARS:
        zip_url = url_for_year(yr)
        tname = splitext(basename(zip_url))[0]
        # Set up the output file
        oname = join(FETCHED_CANDSUMS_DIR, tname + '.csv')
        output_csv = csv.writer(open(oname, 'w'))
        output_csv.writerow(headers)

        with closing(urlopen(zip_url)) as r:
            print("Fetched:", zip_url)
            z = ZipFile(BytesIO(r.read()))
            rows = z.read(tname + '.txt').decode().splitlines()
            for row in csv.reader(rows, delimiter = '|'):
                # insert cycle number, e.g. 2015-2016
                row.insert(0, "%s-%s" % (yr - 1, yr))
                # write to output file
                output_csv.writerow(row)
