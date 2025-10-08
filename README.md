# SUMO demo project — Mini réseau + scripts (pour entraînement)
**But** : fournir un projet minimal prêt à lancer sur ta machine (VSCode) pour s'entraîner à SUMO + Python (TraCI).  
Ce projet contient un petit réseau en XML (nodes/edges), des scripts pour construire le réseau avec `netconvert`, générer des routes, installer les dépendances, et un script Python `run_simulation.py` qui se connecte à SUMO via TraCI.

---

## 📦 Contenu du projet
- `nodes.nod.xml`, `edges.edg.xml` : définition d'un petit réseau 2x3 (noeuds + arêtes).
- `build_net.sh` / `build_net.bat` : commandes pour générer `demo.net.xml` (appelle `netconvert`).
- `generate_rou.py` : script Python qui génère `demo.rou.xml` (trafic aléatoire contrôlable).
- `demo.rou.xml` : fichier d'exemple (généré automatiquement).
- `demo.sumocfg` : configuration SUMO.
- `run_simulation.py` : script Python utilisant `traci` pour piloter la simulation et afficher des métriques.
- `install_deps.sh` / `install_deps.ps1` : scripts d'installation des dépendances.
- `requirements.txt` : paquets Python nécessaires.

---

## ⚙️ Prérequis
- Python ≥ 3.10  
- VSCode (ou tout éditeur)
- SUMO installé (et accessible via la commande `sumo` et `netconvert`).

### Installation rapide
#### Sous Linux / macOS :
```bash
bash install_deps.sh
