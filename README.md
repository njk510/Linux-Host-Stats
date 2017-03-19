# Linux-Host-Stats
Command line tool which gets information about linux hosts

Requirements:
(1) Paramiko must be running on the machine/host where the script is run 
(2) Sysstat on linux hosts that are being monitored 


stats_daemon.py
Usage: stats_daemon.py [options]

Options:
  -h, --help            show this help message and exit
  -p PUBKEY, --pubkey=PUBKEY
                        allows passing a file with public key
  -i HOSTINFO, --host=HOSTINFO
                        allows passing a file with host information in the
                        format "IPaddress username password"
  -s STATS, --stats=STATS
                        allows specifying the csv file for output
                       
parse_stats.py
Usage: parse_stats.py [options]

Options:
 -h, --help            show this help message and exit
 -t DAYTIME, --time=DAYTIME
                       specify a date and time for the query in the format
                       "YYYY-MM-DD HH"
 -i HOSTIP, --ip=HOSTIP
                       specify a host IP address to query
 -s STATS, --stats=STATS
                       allows specifying the csv file for input


