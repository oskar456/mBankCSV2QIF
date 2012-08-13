#!/usr/bin/env python3

import re
import csv
import codecs
import fileinput
import sys

#Make sure stdin is in bianry mode
sys.stdin = sys.stdin.buffer

def mBankCSVtoCSV(file):
	"""
	mBank uses wierd  CSV file with non-CSV header. 
	This function yields only data lines.
	"""
	datare = re.compile(r'[0-3][0-9]-[01][0-9]-20[0-9][0-9]');
	for line in file:
		if not datare.match(line):
			continue;
		yield line;


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



mBankCSVHeaders = ('date','cleared', 'type', 'memo', 'payee', 'payeeaccount',
                   'ks', 'vs', 'ss', 'amount', 'balance');
qifitems=list();
with fileinput.FileInput(mode="rb") as fb:
	f = codecs.iterdecode(fb, 'cp1250'); #mBank always uses CP1250.
	csvreader = csv.reader(mBankCSVtoCSV(f), delimiter=';', quotechar='"');
	for row in csvreader:
		qifitems.append(QifItem(zip(mBankCSVHeaders, row)));

outfile = '/dev/stdout'
with open(outfile,'w') as f:
	f.write("!Type:Bank\n");
	f.write("\n".join(item.toQif() for item in qifitems));

