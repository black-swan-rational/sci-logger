import sqlite3 as sql
import os, sys
import datetime, time
import subprocess
import csv
import pickle
import shutil
#global todo
"""
rozhodit do viac suborov, 
porobit csv nacitavanie
rozumnejsie handlovanie argumentov
poriadny man
menej vypisov

functions:
loading old codes/experiments with given parameters file
test, ci nieco trackujem
okaslat commit spravu bez messagu
"""

base = os.getcwd()
try:
    gitbase = subprocess.check_output('git rev-parse --show-toplevel', shell= True).strip('\n')
except:
    print "git is not inicialized"
    print "please inicialize git repozitory in this directory (git init)"
    sys.exit(0)
end = "/.snaps/" 
gitwork = gitbase+end

def nothing(*args, **kwargs):
    pass

def getfile(name,opt='r'):
    f = open(name,opt)
    pom  =f.read()
    f.close()
    return filter(lambda q: q!=[''], [x.split(' ') for x in pom.rstrip(' \n ').split('\n')])

def getruns():
    f = open(gitwork+"runs",'r')
    pom  =f.read()
    f.close()
    if pom =="":
        return []
    else:
        return pickle.loads(pom)
    pass


def routinecheck(reseting=False):
    """check for file structure and create it if needed"""
    """file structure"""
    try:
        os.stat(gitwork)
    except:
        if(not reseting):
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
    os.path.abspath(realfile)
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
    os.path.abspath(realfile)
    
    if not (os.path.isfile(realfile) and os.path.exists(realfile)): #if it is not a real file, display warning
        what = ''
        while what.lower() not in 'ynz' or len(what)!=1:
            print "File "+ realfile + " does not exists. Add anyway? (y/n)"
            what = raw_input()
        if what== 'n':
            return
        
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
    os.path.abspath(realfile)
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
    os.path.abspath(realfile)
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
    
    

def runExperiment(msq,code):
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
                return
            else:
                #todo: error handling
                pom = os.system('git add '+ x[0].lstrip(gitbase))
                #print "added "+x[0]
            
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
        
    if commitid=='':
        commitid = subprocess.check_output("git rev-parse HEAD", shell=True).strip('\n')
    
    
    print "Code is running"
    
    os.chdir(gitwork)
    os.mkdir(timetag)
    os.chdir(timetag)
    os.mkdir('outputs')
    out = open ("code_out", 'w')
    out.close()
    
    os.chdir(base)
    #todo fork code execution
    dobehlo = True
    exitcode = 0
    try:
        #run code and wirte down times
        exitcode = subprocess.call("echo $(date +%s%N)> .begintime; stdbuf -oL "+code+"|tee "+gitwork+timetag+"/code_out ; echo $(date +%s%N) > .endtime; ", shell=True)
        
    except:
        dobehlo=False
    
    #compute program runetime
    begintime = -1;
    endtime = -2;
    if os.path.isfile(base+"/.begintime"):
        begintime = int(open(".begintime").read())/1000000
    
    if os.path.isfile(base+"/.endtime"):
        endtime = int(open(".endtime").read())/1000000
    runtime = -1
    if( endtime>0 and begintime >0):
        runtime = endtime-begintime
    
    """save outputs and list of outpusts"""
    
    os.chdir(gitwork)
    subprocess.call("cp " + 'outputs' + " " + gitwork + timetag+'outputs', shell=True)
    subprocess.call("cp " + 'list' + " " + gitwork + timetag+'list', shell=True)
    
    trackedoutputs = getfile('outputs')
    for line in trackedoutputs:
        realfile = line[0]
        if os.path.isfile(realfile) and os.path.exists(realfile):
            subprocess.call("cp " + realfile + " " + gitwork + timetag+'/outputs/'+line[0].split('/')[-1], shell=True)
        else:
            print realfile+ " Does no exist"
        
    """run code and save output from standar output""" #todo: save some output files
    """save everythink needed"""
    os.chdir(gitbase+end)
    
    runobject = {"commit":commitid, "timetag":timetag, "message":msq, "code":code, "runtime":runtime}
    runs = getruns()
    runs.append(runobject)
    runy = open("runs",'w')
    runy.write(pickle.dumps(runs))
    runy.close()
    print timetag+ " " +commitid[:6] + " " + str(runtime)+"ns"

def showtries():
    """ print  """
    routinecheck()
    os.chdir(gitwork)
    zoznam = getruns()
    count=0
    if zoznam == None:
        return
    for run in zoznam:
        count+=1
        print str(count),
        print str(run["timetag"]).split('.')[0]+" ",
        print run["commit"][:6]+" ",
        print str(run["runtime"])+" ",
        print run["message"].rstrip('\n')
    
def showtracked():
    """showe list of tracked files"""
    routinecheck()
    os.chdir(gitwork)
    zoznam = getfile('list','r')
    if len(zoznam)!=0:
        print "tracked:"     
    count = 0
    for x in zoznam:
        count+=1
        print str(count)+" .../"+x[0].lstrip(gitbase)
    
    zoznam = getfile('outputs','r')
    if len(zoznam)!=0:
        print "outputs:"
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
    

def reset():
    routinecheck(True)
    shutil.rmtree(gitwork,True)
    routinecheck(True)
    print "Reset done"

def listfiles(nakom, prin=False): #todo
    """return list of scecific output files"""
    if nakom == 'code_out':
        nakom = '../'+nakom
    os.chdir(gitwork)
    zoznam = getruns()
    namelist = []
    for x in zoznam:
        tag = x["timetag"]
        outfilename = gitwork+tag+"/outputs/"+nakom
        if os.path.exists(outfilename) and os.path.isfile(outfilename):
            outfilename= os.path.abspath(outfilename)
            namelist.append(outfilename)
            if prin:
                print outfilename
        
    
    return namelist

def rollback(kam,kto):
    """todo fakt rollbacknut, len enviem ci na tvrdo alebo dat outputy dade inde"""
    routinecheck()
    os.chdir(gitwork)
    zoznam = getruns()
    count=0
    if len(zoznam) < kam:
        print "Invalid id. ("+str(len(zoznam))+" tries)"
        return
    run = zoznam[kam-1]
    print str(run["timetag"]).split('.')[0]+" ",
    print run["commit"][:6]+" " ,
    print run["message"]
    for f in kto:
        ff = os.path.abspath(base+"/"+f)
        print ff
        if os.path.exists(ff) and os.path.isfile(ff):
            #dd
            subprocess.call("git checkout "+run["commit"][:6]+" "+ff,shell=True)
            print f+" reseted"
            
        else:
            print f+" does not exist"
        
    return