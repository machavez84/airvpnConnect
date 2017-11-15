# Python script to connect to Airvpn.

USAGE:

airvpnConnect.py -f/--file <.ovpn file>

RESTRICTIONS:

- Run the script as root
- .ovpn files MUST be the ones generated with the config generation tool in Airvpn site. The script uses information in the filename(string) to identify DNS IPs and remote hostnames. 
- Only works with "earth" config files (for now), including "AltEntry"
- Required libs: colorama,sys,getopt,shutil,socket,fileinput,time
