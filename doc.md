# 🧭 Documentation du mini-projet SUMO – Simulation de mobilité (Hanoï Digital Twin)

## 1. Objectif

Ce projet a pour but de créer une simulation de transport simplifiée inspirée du cas d’étude *Digital Twin for Smart Mobility, Air, and Health (Hanoi)*.
L’objectif est de comprendre les bases de SUMO (Simulation of Urban MObility), d’exécuter une simulation routière et de préparer l’intégration future dans un jumeau numérique urbain.

---

## 2. Structure du projet

```
Hanoi_digital-twin/
│
├── build_net.bat              # Script Windows pour construire le réseau
├── demo.sumocfg               # Fichier de configuration principal SUMO
├── demo.rou.xml               # Fichier définissant les flux de véhicules
├── demo.net.xml               # Réseau routier généré automatiquement
├── nodes.nod.xml              # Fichier des nœuds (intersections)
├── edges.edg.xml              # Fichier des routes reliant les nœuds
├── generate_rou.py            # Script Python pour générer dynamiquement les flux
├── run_simulation.py          # Script Python pour lancer la simulation SUMO
├── install_deps.ps1           # Script PowerShell d’installation des dépendances
├── requirements.txt           # Dépendances Python
└── README.md                  # Documentation du projet
```

---

## 3. Installation et préparation

### 3.1 Prérequis

* **Windows 10/11**
* **Python 3.9+**
* **PowerShell**
* **Visual Studio Code (VSCode)**

### 3.2 Étapes d’installation

#### Étape 1 – Exécuter le script d’installation

Depuis PowerShell, dans le dossier du projet :

```powershell
.\install_deps.ps1
```

Ce script :

* Télécharge et installe **SUMO** (≈ 80–100 Mo)
* Ajoute temporairement SUMO au `PATH`
* Installe les dépendances Python (`sumolib`, `traci`, etc.)

#### Étape 2 – Vérifier l’installation

```powershell
sumo --version
netconvert --version
```

Ces commandes doivent afficher la version installée de SUMO.

---

## 4. Construction du réseau routier

### 4.1 Fichiers utilisés

* **`nodes.nod.xml`** : définit les intersections (nœuds)
* **`edges.edg.xml`** : définit les routes (liaisons)
* **`build_net.bat`** : assemble le réseau à partir des fichiers XML

### 4.2 Exemple de fichier `nodes.nod.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<nodes>
    <node id="n0" x="0.0" y="0.0" type="priority"/>
    <node id="n1" x="100.0" y="0.0" type="priority"/>
    <node id="n2" x="200.0" y="0.0" type="priority"/>
    <node id="n3" x="0.0" y="100.0" type="priority"/>
    <node id="n4" x="100.0" y="100.0" type="priority"/>
    <node id="n5" x="200.0" y="100.0" type="priority"/>
</nodes>
```

### 4.3 Construction du réseau

Exécuter :

```powershell
.\build_net.bat
```

Ce script appelle :

```powershell
netconvert -n nodes.nod.xml -e edges.edg.xml -o demo.net.xml
```

et génère le fichier `demo.net.xml`.

---

## 5. Définition des flux de trafic

### 5.1 Fichier de routes (`demo.rou.xml`)

Contient la description des véhicules, leurs itinéraires et fréquences :

```xml
<routes>
    <vType id="car" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="20"/>
    <route id="r0" edges="e0 e1 e2"/>
    <route id="r1" edges="e3 e4 e5"/>
    <vehicle id="veh0" type="car" route="r0" depart="0"/>
    <vehicle id="veh1" type="car" route="r1" depart="10"/>
</routes>
```

### 5.2 Génération automatique (optionnelle)

Le script `generate_rou.py` peut créer un fichier de flux aléatoire :

```bash
python generate_rou.py
```

---

## 6. Configuration de la simulation

### 6.1 Fichier `demo.sumocfg`

Ce fichier relie tous les composants :

```xml
<configuration>
    <input>
        <net-file value="demo.net.xml"/>
        <route-files value="demo.rou.xml"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="1000"/>
    </time>
</configuration>
```

---

## 7. Exécution de la simulation

### 7.1 Mode graphique (SUMO-GUI)

Pour visualiser le trafic :

```powershell
sumo-gui demo.sumocfg
```

Interface interactive où l’on peut observer les véhicules en temps réel.

### 7.2 Mode console (Python)

Pour lancer et contrôler la simulation via Python :

```powershell
python run_simulation.py
```

Ce script utilise l’API **TraCI** pour piloter SUMO depuis Python.

---

## 8. Analyse et visualisation

Une fois la simulation terminée, les résultats (trafic, temps de trajet, densité, émissions, etc.) peuvent être analysés dans **Jupyter Notebook** via `analysis.ipynb`.

Exemple d’ouverture :

```bash
jupyter notebook analysis.ipynb
```

---

## 9. Vérification rapide du fonctionnement

1. `.\install_deps.ps1` → Installe SUMO et les libs Python
2. `.\build_net.bat` → Génère le réseau `demo.net.xml`
3. `sumo-gui demo.sumocfg` → Lance la simulation graphique
4. `python run_simulation.py` → Lancement programmatique
5. Analyse dans `analysis.ipynb`

---

## 10. Arborescence finale attendue

```
Hanoi_digital-twin/
│
├── demo.sumocfg
├── demo.net.xml
├── demo.rou.xml
├── nodes.nod.xml
├── edges.edg.xml
├── build_net.bat
├── run_simulation.py
├── generate_rou.py
├── install_deps.ps1
├── requirements.txt
└── analysis.ipynb
```

---

## 11. Résumé des concepts appris

| Élément                           | Description                                            |
| --------------------------------- | ------------------------------------------------------ |
| **SUMO**                          | Simulateur open-source de trafic multi-agents          |
| **TraCI**                         | Interface de contrôle de SUMO via Python               |
| **netconvert**                    | Générateur de réseaux routiers                         |
| **.nod / .edg / .rou / .sumocfg** | Fichiers XML structurants de la simulation             |
| **SUMO-GUI**                      | Interface graphique pour observer la simulation        |
| **Python API**                    | Permet d’intégrer SUMO à un jumeau numérique ou une IA |

---

## 12. Prochaines étapes possibles

* Charger une vraie carte OpenStreetMap de Hanoï via `netconvert --osm-files`.
* Ajouter des données de mobilité réelles (OD matrix, GPS, bus).
* Simuler des scénarios : véhicules électriques, voies réservées, prix de congestion.
* Intégrer les résultats à une interface de jumeau numérique (par ex. en Python Dash ou Unity).
