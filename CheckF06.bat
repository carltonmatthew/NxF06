rem
rem The following table outlines how you can modify the passed parameter.

rem Parameter  Description  
rem %1  The normal parameter. 
rem %~f1  Expands %1 to a fully qualified pathname. If you passed only a filename from the current directory, this parameter would also expand to the drive or directory. 
rem %~d1  Extracts the drive letter from %1. 
rem %~p1  Extracts the path from %1. 
rem %~n1  Extracts the filename from %1, without the extension. 
rem ~x1  Extracts the file extension from %1. 
rem %~s1  Changes the n and x options’ meanings to reference the short name. You would therefore use %~sn1 for the short filename and %~sx1 for the short extension. 
rem 
rem The following table shows how you can combine some of the parameters.
rem 
rem Parameter  Description 
rem %~dp1 Expands %1 to a drive letter and path only. 
rem %~sp1 For short path. 
%~nx1  Expands %1 to a filename and extension only. 
rem 
echo on
echo %~p1 	rem pathname
cd %~p1 rem change directory to current file directory
%~d1:\
echo %~n1	rem filename
echo %~x1	rem extension
set filein="%~p1%~n1"
echo %filein%

cmd /k D:\Carlton\Python27\python.exe D:\Carlton\SoftwareDevelopment\NxF06\NxF06.py %~n1