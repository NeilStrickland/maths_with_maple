@ECHO OFF
SETLOCAL
IF EXIST D:\wamp\www\pm1nps\courses\MAS100 (
 SET WEBDIR=D:\wamp\www\pm1nps\courses\MAS100
) ELSE (
IF EXIST C:\wamp\www\courses\MAS100 (
 SET WEBDIR=C:\wamp\www\courses\MAS100
) ELSE (
 SET WEBDIR=C:\wamp\www\pm1nps\courses\MAS100
))

pdflatex all_lectures
pdflatex -job-name=all_handouts \def\HO{1} \input{all_lectures}

REM copy all_lectures.pdf %WEBDIR%
REM copy all_handouts.pdf %WEBDIR%
