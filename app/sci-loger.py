import sqlite3 as sql
import os, sys
import getopt
import datetime
import subprocess
import csv

#global todo
"""
rozhodit do viac suborov, 
porobit csv nacitavanie

"""

base = os.getcwd()
gitbase = subprocess.check_output('git rev-parse --show-toplevel', shell= True).strip('\n')
end = "/snaps/" 
gitwork = gitbase+end

def getfile(name,opt):
    f = open(name,opt)
    pom  =f.read()
    f.close()
    return filter(lambda q: q!=[''], [x.split(' ') for x in pom.rstrip(' \n ').split('\n')])


def routinecheck():
    """kukni ci mas pozadovanu strukturu, ak nie tak vytvor"""
    #print "i am at: "+base
    #print "git is: "+ gitbase
    """filova struktura"""
    try:
        os.stat(gitwork)
    except:
        print "creating snaps (first run)"
        os.mkdir(gitwork)
    
    """zoznam suborov + databaz"""
    f = open(gitwork+"list","a")
    f.close()
    
    f = open(gitwork+"runs","a")
    f.close()
    


def add(fil): #ked je git tak zoznam suborov na ktore ma ist git add
    """klasicka rutina + adnutie filu"""
    routinecheck()
    realfile = base+"/"+fil
    if os.path.isfile(realfile) and os.path.exists(realfile):
        """adni ho"""
        #checkni zoznam filov, ci je validny
        f = open(gitwork+"list","r")
        """kukni, ci tam este nie je"""
        #todo
        zoznam = f.read().strip(' \n ').split('\n')
        novy = not realfile in [x.split(' ')[0] for x in zoznam]  #kukni, ci som taky subor uz nepridal
        f.close()
        if novy:
            f = open(gitwork+"list","a")
            f.write(realfile+" "+fil.split('/')[-1]+"\n")
            f.close()
            print fil+" added succesfully"
        else:
            print "File "+fil+" is already in list"
        sys.exit(0)
    else:
        """neni to validne, hod hlasku"""
        print "Ivalid (nonexisting) file to add: "+ realfile
        sys.exit(0)
    pass


def delete(fil):
    """mazanie pribudne casom asi"""
    routinecheck()
    realfile = base+"/"+fil
    
    """adni ho"""
    #checkni zoznam filov, ci je validny
    
    f = open(gitwork+"list","r")
    """kukni, ci tam este nie je"""
    #todo
    zoznam = f.read().strip(' \n ').split('\n')
    isin = realfile in [x.split(' ')[0] for x in zoznam]  #kukni, ci som taky subor uz nepridal
    f.close()
    if isin:
        f = open(gitwork+"list","w")
        f.write('\n'.join(filter( lambda x: x.split(' ')[0]!=realfile , zoznam)))
        f.close()
        print fil+" removed succesfully"
    else:
        print "File "+fil+" was not in list"
    sys.exit(0)
    

def save(params, code):
    #todo: kukni ci sa vobec nieco zmenilo (parametre alebo subor, alebo vysledky)
    routinecheck()
    
    if not os.path.exists(os.getcwd()+'/'+params):
        
        print "bad param file " + os.getcwd()+params
        sys.exit(10)
    
    """asi najlepsie bude, ked sa forkne, lebo to moze trochu trvat""" #todo
    time = datetime.datetime.now()
    timetag = str(time).replace(" ","_")
    
    """pustim kodik a ulozim output"""
            
    print "Code is running"
    os.chdir(base)
    output = subprocess.check_output(code, shell=True)
    os.chdir(gitwork)
    out = open ("out_"+timetag, 'w')
    out.write(output)
    out.close()
    
    """savne parametre"""
    par = open("par_"+timetag,'w')
    os.chdir(base)
    par.write(open(params,'r').read())
    par.close()
    
    """pusnem"""
    os.chdir(gitwork)
    fil = open("list",'r')
    lis = fil.read().rstrip(' \n ').split('\n')
    fil.close()
    os.chdir(gitbase)
    if len(lis)==0 or lis==['']:
        print "no file to track"
    else:
        for l in lis:
            x = l.split(' ')
            if len(x)!=2:
                print "daco sa pokazilo, asi nieco neexistuje"
                print lis
                sys.exit()
            else:
                pom = os.system('git add '+ x[0].lstrip(gitbase))
                print "added "+x[0]
            
        
    
    
    message = " 'Loger commit: "+ timetag + "'"
    commitid = ""
    try:
        subprocess.check_output('git commit -m'+ message, shell=True)
        commitid = subprocess.check_output("git rev-parse HEAD", shell=True).strip('\n')
        print "Committed"
    
    except:
        print "nothing to commit, codes are same"
        os.chdir(gitwork)
        runs = open('runs','r')
        commitid = runs.read().rstrip('\n').split('\n')[-1].split(' ')[0] #vyhodi commitid posledneho uspesneho comitu, ktoreho vysledky sa ukladali
        runs.close()
    if commitid=='':
        commitid = subprocess.check_output("git rev-parse HEAD", shell=True).strip('\n')
        
        #sem treba dat posledny commit, nie nutne posledny iny
    """savnem potrebne"""
    os.chdir(gitbase+end)
    runy = open("runs",'a')
    runy.write(commitid+" "+timetag + " " + params+"\n")
    runy.close()
    print "saved"
    print "time:"+ timetag,
    print "id: "+commitid, 
    print "params: " + params
    
    
def man():
    #urobit zoznam prikazov a tomu len narubat funkcie
    print "MAN PAGE"
    print "-h help"
    print "-a [file]: adne file ktory potom aduje do gitu"
    print "-r [file]: removne file ktory potom aduje do gitu"
    print """-p [file] [code]: zoberie code a spusti pricom ulozi jeho vystup a ulozi file ako parametre. potom zobere zoznam naadovanych suborov a commitne to."""
    print "-s : ukaze zoznam runov"
    print "-d : difne dva commity"
    print "-l : list trackovanych suborov"
    
    

def show():
    routinecheck()
    os.chdir(gitwork)
    zoznam = getfile('runs','r')    
    count=0
    if zoznam == [['']]:
        print "empty"
        return
    for run in zoznam:
        count+=1
        timetag = run[2]
        print str(count)+" "+run[1][5:-7]+" "+ run[2].split(' ')[0] + ' ' + run[0][:6] + ' '
    
def showtracked():
    routinecheck()
    os.chdir(gitwork)
    zoznam = getfile('list','r')
    count = 0
    for x in zoznam:
        count+=1
        print str(count)+" ..."+x[0].lstrip(gitbase)

def executeall

def main(argv):
       
    execute = ''
    params = ''
   
    try:
        opts, args = getopt.getopt(argv,"a:r:p:lhs") #dorobit message
    except getopt.GetoptError:
        print 'bad argument format'
        sys.exit(0)
    for opt, arg in opts:
        if opt == '-a':
            print "wana add",
            print arg
            add(arg)
            """som poadoval"""
        elif opt == '-r':
            print "wana remove",
            print arg
            delete(arg)
            """som poadoval"""
        elif opt==('-s'):
            show()
        
        elif opt==('-l'):
            showtracked()
            
        elif opt in ("-p"):
            print "saved",
            print arg
            """tu sa savuje"""
            save(arg, " ".join(args))
        
        elif opt in ('-h', '--help', 'help'):
            man()
        
    
    pass


if __name__ == "__main__":
   main(sys.argv[1:])