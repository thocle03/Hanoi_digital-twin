# 🛰️ Digital Twin – Traffic Simulation (Demo & Hanoi)

## 🚦 Aperçu du projet

Ce projet simule la circulation urbaine à l’aide de **SUMO (Simulation of Urban Mobility)**.
Il contient **deux environnements distincts** :

1. 🧩 **Démonstration** – un réseau simple (demo.net.xml) pour tester la configuration de base.
2. 🏙️ **Simulation réelle de Hanoï (Vietnam)** – un réseau routier extrait d’OpenStreetMap et converti pour SUMO.

Le projet permet de :

* générer et exécuter des simulations de trafic,
* enregistrer les résultats (vitesse moyenne, nombre de véhicules),
* analyser et visualiser les données.

---

## 📁 Structure du projet

```
Hanoi_digital-twin/
│
├── demo/                            ← Réseau de démonstration
│   ├── demo.net.xml
│   ├── demo.rou.xml
│   ├── demo.sumocfg
│   ├── simulation_output.csv
│   └── run_simulation.py
│
├── hanoi/                           ← Simulation réelle de Hanoi
│   ├── hanoi.osm.pbf                # Données OSM brutes
│   ├── hanoi.osm                    # Données converties (XML)
│   ├── hanoi.net.xml                # Réseau SUMO
│   ├── hanoi.rou.xml                # Trajets générés aléatoirement
│   ├── hanoi.sumocfg                # Configuration SUMO
│   ├── simulation_output.csv        # Résultats de la simulation
│   └── run_simulation.py
│
├── analysis.ipynb                   # Analyse des résultats CSV
├── install_deps.ps1 / build_net.bat # Scripts d’installation et de conversion
└── README.md                        # Ce fichier
```

---

## ⚙️ Installation

### **1. Prérequis**

* **Windows 10/11**
* **Python 3.10+**
* **SUMO (Simulation of Urban Mobility)**
  Téléchargement : [https://sumo.dlr.de/docs/Downloads.php](https://sumo.dlr.de/docs/Downloads.php)
* **pip packages** :

  ```bash
  pip install pandas matplotlib
  ```

---

### **2. Installation des dépendances**

Depuis PowerShell :

```powershell
.\install_deps.ps1
```

Ce script installe Python, SUMO et les librairies nécessaires s’ils ne sont pas déjà présents.

---

## 🚀 Simulation de démonstration

### **Fichiers utilisés**

* `demo/demo.net.xml` → réseau simplifié
* `demo/demo.rou.xml` → trafic aléatoire
* `demo/demo.sumocfg` → configuration de simulation

### **Exécution**

1. En mode texte (rapide) :

   ```powershell
   cd demo
   python run_simulation.py
   ```

2. En mode visuel :

   ```powershell
   sumo-gui demo.sumocfg
   ```

### **Résultat**

* Le fichier `demo/simulation_output.csv` contient :

  ```
  step,n_vehicles,avg_speed_m_s
  0,1,0.0
  60,1,13.866
  120,0,0.0
  ...
  ```
* Les véhicules apparaissent et disparaissent aléatoirement sur le petit réseau.

---

## 🏙️ Simulation réelle : HANOI

### **1. Données OpenStreetMap**

Fichier d’entrée :

```
hanoi/hanoi.osm.pbf
```

Téléchargé depuis [Geofabrik Vietnam](https://download.geofabrik.de/asia/vietnam.html).

### **2. Conversion en réseau SUMO**

```powershell
netconvert --osm-files hanoi.osm.pbf -o hanoi.net.xml
```

Cela génère le réseau complet de Hanoï dans le format SUMO (`.net.xml`).

### **3. Génération du trafic**

```powershell
python "C:\Program Files (x86)\Eclipse\Sumo\tools\randomTrips.py" -n hanoi.net.xml -r hanoi.rou.xml -e 3600 -l
```

### **4. Configuration SUMO**

Fichier `hanoi.sumocfg` :

```xml
<configuration>
    <input>
        <net-file value="hanoi.net.xml"/>
        <route-files value="hanoi.rou.xml"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="3600"/>
        <step-length value="1"/>
    </time>
</configuration>
```

### **5. Lancer la simulation**

En mode texte :

```powershell
cd hanoi
python run_simulation.py
```

En mode graphique :

```powershell
sumo-gui hanoi.sumocfg
```

### **6. Résultats**

Fichier : `hanoi/simulation_output.csv`

```
step,n_vehicles,avg_speed_m_s
0,0,0.0
180,1,3.847
600,2,11.799
900,1,13.665
```

---

## 📊 Analyse des résultats

Le notebook `analysis.ipynb` permet de visualiser les données issues du CSV :

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("simulation_output.csv")

plt.figure(figsize=(8,4))
plt.plot(df["step"], df["n_vehicles"], label="Nombre de véhicules")
plt.plot(df["step"], df["avg_speed_m_s"], label="Vitesse moyenne (m/s)")
plt.legend()
plt.title("Évolution du trafic au cours du temps")
plt.xlabel("Temps (s)")
plt.show()
```

---

## 🔍 Interprétation

* Les périodes avec `n_vehicles > 0` indiquent un trafic actif.
* Les vitesses moyennes (~10–13 m/s) reflètent un trafic fluide.
* Des valeurs nulles peuvent indiquer des zones calmes ou peu fréquentées.

---

## 🧠 Étapes suivantes

| Objectif                           | Description                             | Commande / Méthode               |
| ---------------------------------- | --------------------------------------- | -------------------------------- |
| 🔹 Densifier le trafic             | Générer plus de véhicules               | `randomTrips.py -p 0.5`          |
| 🔹 Ajouter des feux de circulation | Détection automatique via netconvert    | `--tls.guess --tls.join`         |
| 🔹 Scénario “heures de pointe”     | Ajuster les paramètres de génération    | augmenter le taux de création    |
| 🔹 Analyse avancée                 | Temps moyen de trajet, CO₂, congestions | `TraCI` dans `run_simulation.py` |
| 🔹 Visualisation web               | Créer un dashboard interactif           | `streamlit` ou `plotly`          |

---

## 🧾 Résumé global

| Élément            | Fichier / Commande      | Description                  |
| ------------------ | ----------------------- | ---------------------------- |
| Réseau démo        | `demo.net.xml`          | Petit réseau pour test       |
| Réseau Hanoï       | `hanoi.net.xml`         | Réseau réel importé d’OSM    |
| Trajets aléatoires | `randomTrips.py`        | Génération du trafic         |
| Configuration      | `.sumocfg`              | Paramètres de simulation     |
| Résultats          | `simulation_output.csv` | Données agrégées             |
| Analyse            | `analysis.ipynb`        | Graphiques et interprétation |

---

## 🧰 Outils utilisés

* **SUMO** (Simulation of Urban Mobility)
* **OSMium** – extraction OSM (.pbf → .osm)
* **Netconvert** – génération du réseau routier
* **randomTrips.py** – génération de trafic aléatoire
* **Python (TraCI)** – contrôle et collecte des données
* **Pandas / Matplotlib** – analyse et visualisation

---

## 👨‍💻 Auteurs et contact

**Projet :** Digital Twin – Traffic Simulation
**Auteur :** Thomas Clerc
**Technologies :** SUMO, Python, TraCI, OpenStreetMap
**Plateforme :** Windows + Anaconda (Jupyter Notebook)

