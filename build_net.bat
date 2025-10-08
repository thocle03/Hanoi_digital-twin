@echo off
where netconvert >nul 2>nul
if ERRORLEVEL 1 (
  echo netconvert introuvable. Assure-toi que SUMO est installe et dans le PATH.
  exit /b 1
)
echo Conversion nodes+edges -> demo.net.xml...
netconvert -n nodes.nod.xml -e edges.edg.xml -o demo.net.xml
echo OK: demo.net.xml cree.
