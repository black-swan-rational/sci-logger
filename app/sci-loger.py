from logic import *
import sys, os
import getopt
import argparse

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
def man():
    #urobit zoznam prikazov a tomu len narubat funkcie
    print """MAN PAGE
    -h help
    -a [files]: add files to list of tracked files        
    -r [files]: remove files from list of tracked files
    -A [files]: add files to list of tracked output files (will be copied)
    -R [files]: remove files from list of tracked output files 
    -x [code]: run given code (like "python experimet.py") Care for aphostrophs. Save output (standard output to file code_out, posibly Error) and other tracked output files, commit tracked files
    -s : Show list of tries
    -l : show List of tracked files
    -e [name] [code]: run [code] (bash scriptu) on all results, effectively it will peform code < name on each file
    -n [name]: print newline separated list of output files with given name (like code_out)
    -Q : reset .snaps (empty list of experiments, tracked files and so on) #todo option for commits
    -B [number]: rollback to specific try with id [number]. 
    """
    
def joinfunct(x):
    def pomfun():
        for xx in x:
            xx()
    return pomfun


def main(argv):
       
    execute = ''
    params = ''
    
    """
    print argv
    
    if len(argv)==0:
        man()
        return
    
    control = argv[0]
    
    if argv[0]== 'add':
        print "adujem"
    elif argv[0] == 'rem':
        print "remove"
    elif argv[0] == 'addo':
        print "remove"
    elif argv[0] == 'remo':
        print "remove"
    elif argv[0]== 'run':
        print "runuj"
    elif argv[0]== 'reset':
        print "resetni"
    elif argv[0]== 'help':
        print "ukaz help"
    elif argv[0]== 'list':
        print "list"
    elif argv[0]== 'execute':
        print "execute"
    """
    
    try:
        opts, args = getopt.getopt(argv,"p:arARxXB:e:n:lhsQ") #todo message
    except getopt.GetoptError:
        print 'bad argument format'
        sys.exit(0)
    #print opts
    #print args
    for opt, arg in opts:
        if opt == '-a':
            #adding
            for x in args:
                add(x)
            return
        elif opt == '-r':
            #removing
            for x in args:
                deleteTracked(x)
            return
        elif opt== '-A':
            #add output file to track
            for x in args:
                addOutput(x)
            return
        elif opt == '-R':
            #removing
            for x in args:
                deleteOutput(x)
            return
        elif opt==('-s'):
            #show commits
            showtries()
            return
        elif opt==('-e'):
            #run script on all outputs vith given name
            executeall(arg, ' '.join(args))
            return
        elif opt==('-n'):
            #run script on all outputs vith given name
            listfiles(arg, True)
            return
        
        elif opt==('-l'):
            #list of tracked files
            showtracked()
            return
        
        elif opt==('-Q'):
            #list of tracked files
            reset()
            return
            
        elif opt in ("-x"):
            #run experiment
            print "Write comment to this experiment"
            msg = sys.stdin.readline()
            runExperiment(msg," ".join(args))
            return
        
        elif opt in ("-X"):
            msg = ""
            runExperiment(msg," ".join(args))
            return
        
        elif opt in ("-B"):
            if(arg.isdigit()):
                rollback(int(arg))
            else:
                print "Input number!"
            return
        
        elif opt in ('-h', '--help'):
            #manpage
            man()
            return
        

if __name__ == "__main__":
   main(sys.argv[1:])
