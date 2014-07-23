import sqlite3 as sql
import os, sys
import getopt
import datetime

base = os.getcwd()
workbase = base+"/snaps/" 

def routinecheck():
    """kukni ci mas pozadovanu strukturu, ak nie tak vytvor"""
    print "i am at: "+base
        
    """filova struktura"""
    try:
        os.stat(workbase)
    except:
        print "creating snaps"
        os.mkdir(workbase)
    
    """zoznam suborov + databaz"""
    f = open(workbase+"list","a")
    f.close()
    
    f = open(workbase+"runs","a")
    f.close()
    


def add(fil):
    """klasicka rutina + adnutie filu"""
    routinecheck()
    realfile = base+"/"+fil
    if os.path.isfile(realfile) and os.path.exists(realfile):
        """adni ho"""
        #checkni zoznam filov, ci je validny
        f = open(workbase+"list","a")
        """kukni, ci tam este nie je"""
        #todo
        f.write(fil+" "+fil.split('/')[-1]+"\n")
        f.close()
        print fil+" added succesfully"
        sys.exit(0)
    else:
        """neni to validne, hod hlasku"""
        print "Ivalid (nonexisting) file to add: "+ realfile
        sys.exit(0)
    pass


def delete(fil):
    """mazanie pribudne casom asi"""
    pass

def save(params, code):
    routinecheck()
    """asi najlepsie bude, ked sa forkne, lebo to moze trochu trvat""" #todo
    
    """pustime kod"""
    
    """posavujeme dokumenty"""
    f = open(workbase+"list","r")
    zoznam = f.read()
    f.close()
    
    for line in zoznam:
        if( len(line.split(" ")) != 2):
            print "Bad list format" #neni dobry zoznam suborov. pokracovat aj tak?
            sys.exit(0)
        else:
            


def main(argv):
       
    execute = ''
    params = ''
   
    try:
        opts, args = getopt.getopt(argv,"a:p:")
    except getopt.GetoptError:
        print 'bad format'
        sys.exit(0)
    for opt, arg in opts:
        if opt == '-a':
            print "wana add",
            print arg
            add(arg)
            """som poadoval"""
         
        elif opt in ("-p"):
            print "params",
            print arg
            """tu sa savuje"""
            save(arg, " ".join(args))
            
                
    print "args",
    print args


if __name__ == "__main__":
   main(sys.argv[1:])