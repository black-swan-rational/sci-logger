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
    print "MAN PAGE"
    print "-h help"
    print "-a [file]: add file to list of tracked files"
    print "-r [file]: remove file from list of tracked files"
    print """-x [file] [code]: run given code (bashscript). save output (standard output), save param file and commit tracked files"""
    print "-s : Show list of commits"
    print "-d : dif two commits (states of experiment)" #todo
    print "-l : show List of tracked files"
    print "-o [file]: add file to list of tracked output files"
    #print "-e [code] [zoznam]: run [code] (bash scriptu) on all results in list (numbers)" #todo: names or tags
    print "-E [code] [file]: run [code] (bash script) on [file] from every commit"


def main(argv):
       
    execute = ''
    params = ''
   
    try:
        opts, args = getopt.getopt(argv,"a:r:x:e:E:o:lhs") #todo message
    except getopt.GetoptError:
        print 'bad argument format'
        sys.exit(0)
    #print opts
    #print args
    for opt, arg in opts:
        if opt == '-a':
            #adding
            add(arg)
        elif opt == '-r':
            #removing
            print arg
            delete(arg)
        elif opt==('-s'):
            #show commits
            show()
        elif opt== '-o':
            #add output file to track
            addOutput(arg)
        elif opt==('-E'):
            #run script no all outputs vith given name
            executeall(arg)
        
        elif opt==('-l'):
            #list of tracked files
            showtracked()
            
        elif opt in ("-x"):
            #run experiment with specific param file
            runExperiment(arg, " ".join(args))
        
        elif opt in ('-h', '--help', 'help'):
            #manpage
            man()
        

if __name__ == "__main__":
   main(sys.argv[1:])
