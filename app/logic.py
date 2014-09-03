import sqlite3 as sql
import os, sys
import datetime
import subprocess
import csv

#global todo
"""
rozhodit do viac suborov, 
porobit csv nacitavanie
rozumnejsie handlovanie argumentov
poriadny man
menej vypisov

functions:
loading old codes/experiments with given parameters file
"""

base = os.getcwd()
gitbase = subprocess.check_output('git rev-parse --show-toplevel', shell= True).strip('\n')
end = "/.snaps/" 
gitwork = gitbase+end

def nothing(*args, **kwargs):
    pass

def getfile(name,opt='r'):
    f = open(name,opt)
    pom  =f.read()
    f.close()
    return filter(lambda q: q!=[''], [x.split(' ') for x in pom.rstrip(' \n ').split('\n')])


def routinecheck():
    """check for file structure and create it if needed"""
    """file structure"""
    try:
        os.stat(gitwork)
    except:
        print "creating folder structure (first run)"
        os.mkdir(gitwork)
    
    """list of tracked files + list of tries/experiments (commits)"""
    f = open(gitwork+"list","a")
    f.close()
    
    f = open(gitwork+"runs","a")
    f.close()
    
    f = open(gitwork+"outputs","a")
    f.close()
    
    


def add(fil):
    """classic rutine + add file to list of tracked files (will be always commited)"""
    #todo: check for ./../.s 
    routinecheck()
    realfile = base+"/"+fil
    if os.path.isfile(realfile) and os.path.exists(realfile): #if it is real file
        """add it"""
        f = open(gitwork+"list","r")
        #check whether list of tracked files is valid #todo
        """check for duplicates"""
        zoznam = f.read().strip(' \n ').split('\n')
        novy = not realfile in [x.split(' ')[0] for x in zoznam]
        f.close()
        if novy:
            f = open(gitwork+"list","a")
            f.write(realfile+" "+fil.split('/')[-1]+"\n")
            f.close()
            print fil+" added succesfully"
        else:
            print "File "+fil+" is already in list"
        
    else:
        """it is not valid file"""
        print "Ivalid (nonexisting) file to add: "+ realfile
        
    pass

def addOutput(fil):
    """classic rutine + add file to list of tracked OUTPUT files (will be always saved)"""
    #todo: check for ./../.s 
    routinecheck()
    realfile = base+"/"+fil
    if not (os.path.isfile(realfile) and os.path.exists(realfile)): #if it is not a real file, display warning
        what = ''
        while what.lower() not in 'ynz' or len(what)!=1:
            print "File "+ realfile + " does not exists. Add anyway? (y/n)"
            what = raw_input()
        if what== 'n':
            sys.exit(0)
        
    """add it"""
    f = open(gitwork+"outputs","r")
    """check for duplicates"""
    zoznam = f.read().strip(' \n ').split('\n')
    novy = not realfile in [x.split(' ')[0] for x in zoznam]
    f.close()
    if novy:
        f = open(gitwork+"outputs","a")
        f.write(realfile+" "+fil.split('/')[-1]+"\n")
        f.close()
        print fil+" added succesfully (outputs)"
    else:
        print "File "+fil+" is already in outputs"
    
    pass


def deleteTracked(fil):
    """remove file from list of tracked files (will not be added in experimental commits)"""
    #todo: check for ./../.s 
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
    

def deleteOutput(fil):
    """remove file from list of tracked files (will not be added in experimental commits)"""
    #todo: check for ./../.s 
    routinecheck()
    realfile = base+"/"+fil
    
    """adni ho"""
    #checkni zoznam filov, ci je validny
    
    f = open(gitwork+"outputs","r")
    """kukni, ci tam este nie je"""
    #todo
    zoznam = f.read().strip(' \n ').split('\n')
    isin = realfile in [x.split(' ')[0] for x in zoznam]  #kukni, ci som taky subor uz nepridal
    f.close()
    if isin:
        f = open(gitwork+"outputs","w")
        f.write('\n'.join(filter( lambda x: x.split(' ')[0]!=realfile , zoznam)))
        f.close()
        print fil+" removed succesfully"
    else:
        print "File "+fil+" was not in list"
    
    

def runExperiment(code):
    """ will save current state of code with its outputs and parameters"""
    #todo: kukni ci sa vobec nieco zmenilo (parametre alebo subor, alebo vysledky)
    #todo: code davat ako bashscript (meno suboru), nechat usera napisat malu spravu (donutit ho k nej) 
    routinecheck()
    
    time = datetime.datetime.now()
    timetag = str(time).replace(" ","_")
    
    """add tracked files"""
    os.chdir(gitwork)
    lis=getfile("list")
    os.chdir(gitbase)
    if len(lis)==0 or lis==['']:
        print "no file to track"
    else:
        for l in lis:
            x = l
            if len(x)!=2:
                print "something is wrong, bad file list format: ",
                print lis
                sys.exit()
            else:
                #todo: error handling
                pom = os.system('git add '+ x[0].lstrip(gitbase))
                print "added "+x[0]
            
    """commit"""
    message = " 'Loger commit: "+ timetag + "'"
    commitid = ""
    try:
        subprocess.check_output('git commit -m'+ message, shell=True)
        commitid = subprocess.check_output("git rev-parse HEAD", shell=True).strip('\n')
        print "Committed"
    
    except:
        """todo> execept exactly this error (error number)"""
        print "nothing to commit, codes are same"
        os.chdir(gitwork)
        runs = open('runs','r')
        commitid = runs.read().rstrip('\n').split('\n')[-1].split(' ')[0] #vyhodi commitid posledneho uspesneho comitu, ktoreho vysledky sa ukladali
        runs.close()
    if commitid=='':
        commitid = subprocess.check_output("git rev-parse HEAD", shell=True).strip('\n')
    
    
    print "Code is running"
    os.chdir(base)
    #todo fork code execution
    
    dobehlo = True
    output = "Error"
    try:
        output = subprocess.check_output(code, shell=True)
    except:
        dobehlo=False
    
    os.chdir(gitwork)
    os.mkdir(timetag)
    os.chdir(timetag)
    os.mkdir('outputs')
    out = open ("code_out", 'w')
    out.write(output)
    out.close()
    
    """save parameters"""
    
    os.chdir(gitwork)
    trackedoutputs = getfile('outputs')
    for line in trackedoutputs:
        realfile = line[0]
        if os.path.isfile(realfile) and os.path.exists(realfile):
            subprocess.check_output("cp " + realfile + " " + gitwork + timetag+'/outputs/'+line[0].split('/')[-1], shell=True)
        else:
            print realfile+ " Does no exist"
        
    """run code and save output from standar output""" #todo: save some output files
    """save everythink needed"""
    os.chdir(gitbase+end)
    runy = open("runs",'a')
    runy.write(commitid+" "+timetag + " " + str(dobehlo) + " "+ code +"\n")
    runy.close()
    print "time:"+ timetag,
    print "id: "+commitid[:6],
    print "fin: "+ str(dobehlo)
    print "code: " + code

def show():
    """ print  """
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
    """showe list of tracked files"""
    routinecheck()
    print "tracked:"     
    os.chdir(gitwork)
    zoznam = getfile('list','r')
    count = 0
    for x in zoznam:
        count+=1
        print str(count)+" .../"+x[0].lstrip(gitbase)
    
    print "outputs:"
    zoznam = getfile('outputs','r')
    count = 0
    for x in zoznam:
        count+=1
        print str(count)+" .../"+x[0].lstrip(gitbase)        
    

def executeall(nakom, script): #todo
    """execute script on specific output files (default-all)"""
    os.chdir(gitwork)
    zoznam = listfiles(nakom)
    
    for x in zoznam:
        output=subprocess.check_output(script + ' < ' + x, shell=True)
        print x
        print output,
    


def listfiles(nakom, prin=False): #todo
    """return list of scecific output files"""
    if nakom == 'code_out':
        nakom = '../'+nakom
    os.chdir(gitwork)
    zoznam = getfile('runs')
    namelist = []
    for x in zoznam:
        tag = x[1]
        outfilename = gitwork+tag+"/outputs/"+nakom
        if os.path.exists(outfilename) and os.path.isfile(outfilename):
            namelist.append(outfilename)
            if prin:
                print outfilename
        
    
    return namelist
