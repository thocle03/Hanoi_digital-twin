@echo off
echo Building SUMO network...
netconvert -n nodes.nod.xml -e edges.edg.xml -o demo.net.xml
echo Done.
pause
