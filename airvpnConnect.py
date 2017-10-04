#!/usr/bin/env python3
#Script to connect to Airvpn Servers and update DNS accordingly.
#By: Manuel A. Chavez M.

#Imports
import sys, getopt, shutil, socket, fileinput
from subprocess import call, Popen
from colorama import Fore, Back, init

#Autoreset colorama color
init(autoreset=True)

def header():
  print(Fore.GREEN + "*********************************")
  print(Fore.GREEN + "*", end="")
  print(Fore.RED + "AIRVPN Python connection script", end="")
  print(Fore.GREEN + "*")
  print(Fore.GREEN + "*********************************")


#To tell how to use the script
def usage():
  return print("Usage: openvpnConnect.py -f/--file <.ovpn file>")

#Function to determine DNS IP
def findDNS(file):
  dns = ""
  if "443" in file and "UDP" in file:
    dns = "10.4.0.1"
  elif "443" in file and "TCP" in file:
    dns = "10.5.0.1"
  elif "80" in file and "UDP" in file:
    dns = "10.6.0.1"
  elif "80" in file and "TCP" in file:
    dns = "10.7.0.1"
  elif "53" in file and "UDP" in file:
    dns = "10.8.0.1"
  elif "53" in file and "TCP" in file:
    dns = "10.9.0.1"
  elif "1194" in file and "UDP" in file:
    dns = "10.30.0.1"
  elif "1194" in file and "TCP" in file:
    dns = "10.50.0.1"
  return dns

#Function to resolv airvpn remote host address to add to .ovpn temp file
def getIP(d):
  try:
    IP = socket.gethostbyname(d)
    return IP
  except Exception:
    return False

def getRemoteHost(file):
  domain = ""
  if "AltEntry" in file:
    domain = "earth2.vpn.airdns.org"
  else:
    domain = "earth.vpn.airdns.org"
  return domain

#Procedure to create temporary .ovpn file as openvpn config file
def createTempFile(file):
  print(Fore.RED + "remote hostname is: {}".format(getRemoteHost(file)))
  print(Fore.RED + "Creating .ovpn temporay file...", end="")
  shutil.copy(file, "/tmp/airvpntmp.ovpn")
  for line in fileinput.input("/tmp/airvpntmp.ovpn", inplace=1):
    if "remote" in line:
      line = line.replace(getRemoteHost(file), getIP(getRemoteHost(file)))
    sys.stdout.write(line)
  print(Fore.GREEN + "Done!") 

#Procedure to modify resolv.conf
def editResolv(file):
  print(Fore.RED + "Editing /etc/resolv.conf file...", end="")
  shutil.move("/etc/resolv.conf", "/etc/resolv.conf.bak")
  f = open("/etc/resolv.conf", "w+")
  f.write("nameserver " + findDNS(file) + '\n' )
  print(Fore.GREEN + "Done!")
  print(Fore.RED + "/etc/resolv.conf content:")
  f.close()
  call(["cat", "/etc/resolv.conf"]) 
  

#Procedure to restore resolv.conf and delete temporary .ovpn file
def clean():
  print(Fore.RED + "Restoring /etc/resolv.conf file...", end="")
  shutil.move("/etc/resolv.conf.bak", "/etc/resolv.conf")
  print(Fore.GREEN + "Done!")
  print(Fore.RED + "Deleting temporary .ovpn file...", end="")
  call(["rm", "/tmp/airvpntmp.ovpn"])
  print(Fore.GREEN + "Done!")
  
#Procedure to perform de connection
def connect(tempfile):
  print(Fore.RED + "Connecting using file: {}".format(tempfile))
  print(Back.RED + "Keep this terminal open. PRESS CTR-C TO DISCONNECT" )
  try:
    Popen(["openvpn " + tempfile], shell=True).communicate()
  except KeyboardInterrupt:
    clean()


def main():
  TEMP_FILE = "/tmp/airvpntmp.ovpn"
  OVPN_FILE = ""
  if len(sys.argv) != 3:
    usage()
    sys.exit(1)
  try:
    opts, args = getopt.getopt(sys.argv[1:], "f:", ["file="])
  except getopt.GetoptError:
    usage()    
    sys.exit(2)
  for opt, arg in opts:
    if opt in ("-f", "--file"):
      OVPN_FILE = arg
  header()
  createTempFile(OVPN_FILE)
  editResolv(OVPN_FILE)
  connect(TEMP_FILE)

if __name__ == "__main__":
  main()
  sys.exit(0)
