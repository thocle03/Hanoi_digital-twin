#!/usr/bin/env bash
set -e
if ! command -v netconvert >/dev/null 2>&1; then
  echo "netconvert introuvable. Installe SUMO et ajoute-le au PATH."
  exit 1
fi
echo "Conversion nodes+edges -> demo.net.xml..."
netconvert -n nodes.nod.xml -e edges.edg.xml -o demo.net.xml
echo "OK: demo.net.xml créé."
