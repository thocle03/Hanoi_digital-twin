import requests

# URL du serveur Overpass API (OpenStreetMap)
overpass_url = "https://overpass-api.de/api/interpreter"

# Requête pour récupérer toute la zone de Hanoï (~20 km autour du centre)
query = """
[out:xml][timeout:120];
(
  node["highway"](20.95,105.75,21.10,105.95);
  way["highway"](20.95,105.75,21.10,105.95);
  relation["highway"](20.95,105.75,21.10,105.95);
);
out body;
>;
out skel qt;
"""

print("Téléchargement des données OSM de Hanoï en cours...")
response = requests.get(overpass_url, params={"data": query})

if response.status_code == 200:
    with open("hanoi.osm", "wb") as f:
        f.write(response.content)
    print("✅ Fichier téléchargé avec succès : hanoi.osm")
else:
    print(f"❌ Erreur {response.status_code} pendant le téléchargement.")
