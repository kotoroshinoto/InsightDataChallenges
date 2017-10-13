import csv
import re
import sys
import pandas as pd
from pandas.tseries.offsets import DateOffset


def fix_date_time(filepath, outpath):
    #2015-04-10 19:01:20
    date_regex = re.compile("^([0-9]{4}[-][0-9]{2}[-][0-9]{2}[ ][0-9]{2}[:])([0-9]{2})[:]([0-9]{2})$")
    minoff = DateOffset(minutes=1)
    secoff = DateOffset(seconds=1)
    with open(filepath, 'r') as f:
        rdr = csv.DictReader(f)
        sysoutcsv = csv.DictWriter(sys.stdout, fieldnames=rdr.fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        with open(outpath, 'w') as of:
            wtr = csv.DictWriter(of, fieldnames=rdr.fieldnames, quoting=csv.QUOTE_NONNUMERIC)
            wtr.writeheader()
            for entry in rdr:
                entry['user_id'] = int(entry['user_id'])
                entry['test'] = int(entry['test'])
                entry['price'] = int(entry['price'])
                entry['converted'] = int(entry['converted'])
                # if not((entry['test'] and entry['price'] == 59) or (not entry['test'] and entry['price'] == 39)):
                #     print("WARNING, detected mismatch between price and test group: test: %d; price: %d" % (entry['test'], entry['price']))
                mo = date_regex.match(entry['timestamp'])
                if not mo:
                    print("PROBLEM ENTRY:")
                    sysoutcsv.writerow(entry)
                    raise RuntimeError("entry did not match")
                #fix minutes
                if mo.group(2) == '60':
                    mins = '59'
                    add_min = True
                else:
                    mins = mo.group(2)
                    add_min = False
                #fix seconds
                if mo.group(3) == '60':
                    secs = '59'
                    add_sec = True
                else:
                    secs = mo.group(3)
                    add_sec = False

                timestmp_str = "%s%s:%s" % (mo.group(1), mins, secs)
                tstamp = pd.to_datetime(timestmp_str)
                if add_sec:
                    tstamp += secoff
                if add_min:
                    tstamp += minoff
                entry['timestamp'] = tstamp
                wtr.writerow(entry)

