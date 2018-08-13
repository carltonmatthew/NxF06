# NxF06

Nastran .F06 file error extractor
USAGE:

python NxF06.py fileprefix FileLocation
The program processes file fileprefix.f06 which is in the directory FileLocation

If there are any errors/warnings, related Nodes & Elements are placed in filename.neu
to be read in to FFEMAP.
The directory contains the python coe and a selection of exable files containig the errors which can be processed.
