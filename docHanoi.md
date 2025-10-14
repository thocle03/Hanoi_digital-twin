# 🛰️ Digital Twin of Hanoi – Traffic Simulation

## 🎯 Objectif du projet

Ce projet vise à **simuler le trafic urbain de la ville de Hanoï** (Vietnam) à l’aide de **SUMO (Simulation of Urban Mobility)** et de scripts Python pour :

* générer le réseau routier à partir de données OpenStreetMap (OSM),
* créer un trafic réaliste (flux de véhicules aléatoires ou calibrés),
* exécuter et analyser la simulation,
* exporter les résultats pour étude et visualisation.

---

## 🧩 Architecture du projet

```
Hanoi_digital-twin/
│
├── hanoi.osm.pbf           ← Données brutes OpenStreetMap (binaire)
├── hanoi.osm               ← Version XML extraite du PBF
├── hanoi.net.xml           ← Réseau routier converti pour SUMO
├── hanoi.rou.xml           ← Routes et trajets générés aléatoirement
├── hanoi.sumocfg           ← Fichier de configuration SUMO
├── simulation_output.csv   ← Résultats (vitesse, nombre de véhicules, etc.)
├── analysis.ipynb          ← Analyse Python des résultats
└── build_net.bat / run_simulation.bat (scripts d’automatisation)
```

---

## ⚙️ Étapes de création

### **1. Préparation des données**

**Source :**

* Le fichier `vietnam.osm.pbf` a été téléchargé depuis [Geofabrik](https://download.geofabrik.de/asia/vietnam.html).

**Extraction de la zone de Hanoï :**
On a utilisé l’outil `osmium` pour convertir et extraire la zone d’intérêt :

```powershell
osmium extract --bbox 105.75,20.95,105.95,21.10 vietnam.osm.pbf -o hanoi.osm.pbf
```

---

### **2. Conversion en réseau SUMO**

À partir du fichier `.osm.pbf`, génération du réseau routier utilisable par SUMO :

```powershell
netconvert --osm-files hanoi.osm.pbf -o hanoi.net.xml
```

**Résultat :**

* `hanoi.net.xml` contient la topologie complète du réseau (noeuds, routes, intersections).
* Les warnings du type :

  ```
  Warning: Value of key 'maxspeed:type' is not numeric ('urban')
  ```

  sont normaux : SUMO les ignore ou les remplace par des valeurs par défaut.

---

### **3. Génération du trafic**

SUMO inclut un outil pratique : **`randomTrips.py`**, utilisé pour générer un trafic aléatoire.

Commande utilisée :

```powershell
python "C:\Program Files (x86)\Eclipse\Sumo\tools\randomTrips.py" -n hanoi.net.xml -r hanoi.rou.xml -e 3600 -l
```

**Paramètres :**

* `-n` : fichier réseau
* `-r` : fichier de sortie des routes
* `-e 3600` : fin de simulation à 3600 secondes (1 heure)
* `-l` : éviter les boucles infinies

**Résultat :**

* `hanoi.rou.xml` contient les trajets des véhicules générés aléatoirement.

---

### **4. Configuration de la simulation**

Fichier : `hanoi.sumocfg`

```xml
<?xml version="1.0" encoding="UTF-8"?>
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

---

### **5. Exécution de la simulation**

Deux options :

1. **Mode graphique (visualisation)**

   ```powershell
   sumo-gui hanoi.sumocfg
   ```

2. **Mode console (avec export des résultats)**

   ```powershell
   python run_simulation.py
   ```

   Ce script contrôle SUMO via TraCI et exporte :

   ```
   simulation_output.csv
   ```

---

### **6. Analyse des résultats**

Exemple de contenu du CSV :

```
step,n_vehicles,avg_speed_m_s
0,0,0.0
60,0,0.0
120,0,0.0
180,1,3.847
240,0,0.0
600,2,11.799
900,1,13.665
```

Le fichier `analysis.ipynb` permet :

* de charger les données avec pandas,
* de visualiser la densité du trafic et les vitesses moyennes,
* de repérer les périodes d’activité.

Exemple d’extraits du notebook :

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("simulation_output.csv")

plt.plot(df["step"], df["n_vehicles"])
plt.title("Nombre de véhicules au cours du temps")
plt.xlabel("Temps (s)")
plt.ylabel("Nombre de véhicules")
plt.show()

plt.plot(df["step"], df["avg_speed_m_s"])
plt.title("Vitesse moyenne du trafic")
plt.xlabel("Temps (s)")
plt.ylabel("Vitesse (m/s)")
plt.show()
```

---

## 🧠 Interprétation des résultats

* Les périodes avec `n_vehicles > 0` montrent des passages de véhicules détectés sur le réseau.
* Les vitesses moyennes (≈ 10–13 m/s, soit 36–45 km/h) sont cohérentes avec un trafic fluide sur certaines portions.
* La présence de nombreux `0` reflète soit une densité faible, soit un réseau étendu où les véhicules ne passent pas à chaque pas de simulation.

---

## 🚧 Points techniques

* Les warnings `maxspeed:type=urban` ou `Unknown lane use specifier` sont sans gravité.
* Le modèle actuel est **stochastique** (trafic aléatoire).
  Pour une simulation plus réaliste, on peut :

  * injecter des **données réelles de flux** (ex. : capteurs, données GPS),
  * définir des **zones génératrices de trafic** (habitations, zones de travail),
  * intégrer des **modes de transport multiples** (voitures, bus, motos).

