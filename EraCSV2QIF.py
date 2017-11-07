#!/usr/bin/env python3

import re
import csv
import codecs
import fileinput
import sys

#Make sure stdin is in binary mode
sys.stdin = sys.stdin.buffer


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
                out.append("^");
                return "\n".join(out);



qifitems=[];
with fileinput.FileInput(mode="rb") as fb:
        f = codecs.iterdecode(fb, 'cp1250'); #Era always uses CP1250
        next(f) # skip the heading
        next(f)
        csvreader = csv.DictReader(f, delimiter=';', quotechar='"');
        for row in csvreader:
                it = {
                    "date": row["datum zaúčtování"],
                    "memo": row["poznámka"],
                    "amount": row["částka"].translate(str.maketrans(",","."," \xa0")),
                    "payee": row["název účtu protiúčtu"],
                }
                qifitems.append(QifItem(it))



outfile = '/dev/stdout'
with open(outfile,'w') as f:
        f.write("!Type:Bank\n");
        f.write("\n".join(item.toQif() for item in reversed(qifitems)));

