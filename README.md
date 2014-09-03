sci-logger
==========

####Overview
Sci-loger is scientific experiment version control for linux. It allows you to easily track all experimental codes, parameters and outputs between every groundbreaking genial idea. And yes, it heavily depends on git.

Just tell (write) it what files (codes) do you want to keep track of, what outputs do you want to save and run some code. Code is committed (.git/), output is saved (cp to .snaps/- best version control ever), everything is fine.

Finally, we can process those outputs and do some data magic with them.

As you can imagine, there is a little dependency on git + now it is possible to use logger only in file already under git version control.

####MAN PAGE
.-h help
.-a [file]: add file to list of tracked files"
.-r [file]: remove file from list of tracked files"
.-x [file] [code]: run given code (bashscript). save output (standard output), save param file and commit tracked files"""
.-s : Show list of commits"
.-d : dif two commits (states of experiment)" #todo
.-l : show List of tracked files"
.-o [file]: add file to list of tracked output files"
.-E [code] [file]: run [code] (bash script) on [file] from every commit"

####Todo

automatic visualization, some default processing scripts, man, filtering, tagging, easily diff two states of experiments and restore some previous state
