import base64
import paramiko
import time
from datetime import datetime
from optparse import OptionParser


def get_info_from_host(my_key,ip_addr,usr,pwd):
	IDLE_PERCENT_POSITION = 12
	DISK_PERCENT_POSITION = 4
	key = paramiko.RSAKey(data=base64.b64decode(my_key))
	client = paramiko.SSHClient()
	client.get_host_keys().add('ssh.example.com', 'ssh-rsa', key)
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(ip_addr, username=usr , password=pwd)
	#stdin, stdout, stderr = client.exec_command('sar  -r | tail -n1')

	# grab CPU usage
	stdin, stdout, stderr = client.exec_command('mpstat | tail -n1')
	# this will give the following output idle
	# 05:27:44 AM  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %
	line = stdout.readline()	
	#extract the 3rd value
	output = line.split()
	cpu_usage = 100 - float(output[IDLE_PERCENT_POSITION])	

	# grab disk usage
	stdin1, stdout1, stderr1 = client.exec_command('df | head -n2 | tail -n1')
	# this will give the following output	
	#Filesystem     1K-blocks    Used Available Use% Mounted open
	#/dev/sda1      473868440 3343452 446430732   1% /
	line1 = stdout1.readline()
	#extract percentage usage from the 5h position
	output1 = line1.split()
	disk_usage = output1[DISK_PERCENT_POSITION]

	# grab number of logged in users
	stdin2, stdout2, stderr2 = client.exec_command('who | wc -l')
	# this will give the following output	
	#Filesystem     1K-blocks    Used Available Use% Mounted open
	#/dev/sda1      473868440 3343452 446430732   1% /
	line2 = stdout2.readline()
	#extract percentage usage from the 5h position
	users = line2
	client.close()
	return (cpu_usage, disk_usage, users)

parser = OptionParser()
parser.add_option("-p", "--pubkey", dest="pubkey", help= "allows passing a file with public key",metavar="PUBKEY")
parser.add_option("-i", "--host", dest="hostinfo", help= "allows passing a file with IP address, username and password",metavar="HOSTINFO")
parser.add_option("-s", "--stats", dest="stats", help= "allows specifying the csv file for output",metavar="STATS")
(options, args) = parser.parse_args()

f = open(options.pubkey, 'r')
my_key = f.read()
f.close()

host_info = {}
f1 = open(options.hostinfo, 'r')
for line in f1:
	split_line = line.split()
	host_info[split_line[0]] = split_line[1:3]
f1.close()

outfile = open(options.stats, 'w')
outfile.write("ip, timestamp, cpu usage, disk usage, users \n")
try:
	while True:
		for k,v in host_info.items():
			host_stats = get_info_from_host(my_key,k,v[0],v[1])
			print "Running get info on host " + k
			outfile.write(k + "," +  str(datetime.today()) + "," + str(host_stats[0]) + "," + str(host_stats[1])+ "," + str(host_stats[2]) + "\n")
			outfile.flush()
		time.sleep(60)
except KeyboardInterrupt:
	pass
outfile.close()