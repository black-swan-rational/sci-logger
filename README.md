sci-logger
==========

####Overview
Sci-loger is scientific experiment version control for linux. It allows you to easily track all experimental codes, parameters and outputs between every groundbreaking genial idea. And yes, it heavily depends on git.

Just tell (write) it what files (codes) do you want to keep track of, what outputs do you want to save and run some code. Code is committed (.git/), output is saved (cp to .snaps/- best version control ever), everything is fine.

Finally, we can process those outputs and do some data magic with them.

As you can imagine, there is a little dependency on git + now it is possible to use logger only in file already under git version control.

####MAN PAGE

*-h help
*-a [file]: add file to list of tracked files
*-r [file]: remove file from list of tracked files
*-A [file]: add file to list of tracked output files (will be copied)
*-R [file]: remove file from list of tracked output files 
*-x [code]: run given code (like python experimet.py). save output (standard output to file code_out, posibly Error) and other tracked output files, commit tracked files
*-s : Show list of tries
*-l : show List of tracked files
*-e [name] [code]: run [code] (bash scriptu) on all results in list (numbers), effectively it will peform code < name on each file
*-n [name]: print newline separated list of output files with given name (like code_out)

####Todo

automatic visualization, some default processing scripts, man, filtering, tagging, easily diff two states of experiments and restore some previous state
