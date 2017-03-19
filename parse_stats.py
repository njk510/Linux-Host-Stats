from optparse import OptionParser
import sys
import re

parser = OptionParser()
parser.add_option("-t", "--time", dest="daytime", help= "specify a date and time for the query in the format \"YYYY-MM-DD HH:MM\"",metavar="DAYTIME")
parser.add_option("-i", "--ip", dest="hostip", help= "specify a host IP address to query",metavar="HOSTIP")
parser.add_option("-s", "--stats", dest="stats", help= "allows specifying the csv file for output",metavar="STATS")
(options, args) = parser.parse_args()

pattern1 = None
pattern2 = None

if options.daytime:
	pattern1 = re.compile(options.daytime)

if options.hostip:
	pattern2 = re.compile(options.hostip)

if pattern1 == None and pattern2 == None:
	print "Please enter a valid query"
	sys.exit()
f = open(options.stats)
count = 0
for i, line in enumerate(f):
	if pattern1 and pattern2 == None:
		if re.search(pattern1,line):
			print line
			count += 1
	elif pattern2 and pattern1 == None:
		if re.search(pattern2,line):
			print line
			count += 1
	elif pattern1 and pattern2:
		if re.search(pattern1,line) and re.search(pattern2,line):
			print line
			count += 1

f.close()

if count == 0:
	print "Query does not exist"




	



