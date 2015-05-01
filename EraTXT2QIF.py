#!/usr/bin/env python3

import re
import fileinput

class QifItem(dict):
    """
        A dictionary-like object representing one QIF item.
    """

    def __init__(self, values=None):
        if values is not None:
            self.update(values);

    def toQif(self):
        """ Returns QIF-style representation of given Item. """
        out=list();
        if 'date' in self:
            out.append("D{}".format(self['date']));
        if 'amount' in self:
            out.append("T{}".format(self['amount']));
        if 'memo' in self and len(self['memo'])>3:
            out.append("M{}".format(self['memo']));
        if 'payee' in self and len(self['payee'])>3:
            out.append("P{}".format(self['payee']));
        if 'desc' in self and len(self['desc'])>3:
            out.append("XS{}".format(self['desc']));
        out.append("^");
        return "\n".join(out);


headers_map = {
        'date': re.compile('datum zaúčtování: *(.*)$'),
        'amount': re.compile('částka: *(.*)$'),
        'memo': re.compile('poznámka: *(.*)$'),
        'desc': re.compile('označení operace: *(.*)$'),
        }

qifitems=list();
with fileinput.FileInput(mode="r") as fb:
    item = QifItem()
    line = []
    for row in (l.rstrip() for l in fb):
        if len(row)>0 and row[0]==' ':
            line.append(row.strip())
        else:
            for hdr,rex in headers_map.items():
                m = rex.match(" ".join(line))
                if m:
                    item[hdr]=m.group(1).strip()
            line = [row,]
        if row == "" and len(item)>0:
            qifitems.append(item)
            item = QifItem()


outfile = '/dev/stdout'
with open(outfile,'w') as f:
    f.write("!Type:Bank\n")
    f.write("\n".join(item.toQif() for item in qifitems))

