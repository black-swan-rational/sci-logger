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
    -a [file]: add file to list of tracked files        
    -r [file]: remove file from list of tracked files
    -A [file]: add file to list of tracked output files (will be copied)
    -R [file]: remove file from list of tracked output files 
    -x [code]: run given code (like "python experimet.py") Care for aphostrophs. save output (standard output to file code_out, posibly Error) and other tracked output files, commit tracked files
    -s : Show list of tries
    -l : show List of tracked files
    -e [name] [code]: run [code] (bash scriptu) on all results in list (numbers), effectively it will peform code < name on each file
    -n [name]: print newline separated list of output files with given name (like code_out)
    -Q : reset .snaps (empty list of experiments, tracked files and so on) #todo option for commits
    """
    

def main(argv):
       
    execute = ''
    params = ''
    #print argv
    try:
        opts, args = getopt.getopt(argv,"p:arARxXe:n:lhsQ") #todo message
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
            show()
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
            #run experiment
            #print "Write comment to this experiment"
            #msg = sys.stdin.readline()
            msg = ""
            runExperiment(msg," ".join(args))
            return
        
        elif opt in ('-h', '--help'):
            #manpage
            man()
            return
        

if __name__ == "__main__":
   main(sys.argv[1:])
