@echo off

:: echo Running Ruby code...
:: ruby bib_to_json.rb
echo Looking for New Publications
python test.py
echo Adding New Publications
python pubmerge.py

echo Running Jekyll...
call bundle update
call jekyll build

REM cls  REM Clear the screen

REM echo Enter username and password to upload files to Website
REM set /p username=Enter your username: 
REM scp -r _site/* %username%@webserv3.rz.uni-jena.de:web/
scp -r _site/* atthdanishfurkh@webserv3.rz.uni-jena.de:~/web/
echo All commands executed.

pause

