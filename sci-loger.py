import sqlite3 as sql
import os, sys
import getopt

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
    
    """robime si databazu"""
    con = None
    
    try:
        con = sql.connect(workbase+"example.db")
        cur = con.cursor()    
        dbstructure="(Id INTEGER PRIMARY KEY, files TEXT, params TEXT, date STRING, filelist TEXT, porn TEXT, outcome TEXT)"
        cur.execute("CREATE TABLE IF NOT EXISTS Logs"+dbstructure)
        con.commit()
    except sql.Error, e:
        if con:
            con.rollback()
        
        print "Error %s:" % e.args[0]
        sys.exit(1)
        

def add(fil):
    """klasicka rutina + adnutie filu"""
    routinecheck()
    realfile = base+"/"+fil
    if os.path.isfile(realfile) and os.path.exists(realfile):
        """adni ho"""
        #checkni zoznam filov, ci je validny
        f = open(workbase+"list","a")
        f.write(fil+"\n")
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

def save():
    """asi najlepsie bude, ked sa forkne, lebo to moze trochu trvat"""


def main(argv):
       
    execute = ''
    params = ''
   
    try:
        opts, args = getopt.getopt(argv,"a:p:e")
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
            """tu bude treba savnut"""
            
                
    print "args",
    print args


if __name__ == "__main__":
   main(sys.argv[1:])