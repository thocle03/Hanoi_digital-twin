#!/usr/bin/env python3
"""Génère un fichier demo.rou.xml avec N véhicules répartis sur des routes définies."""
import argparse, random, datetime

ROUTES = {
    "r0": "e0 e1 e6",
    "r1": "e0 e5 e3",
    "r2": "e4 e2 e3",
    "r3": "e5r e1",
    "r4": "e1r e0r"
}

def generate(nvehicles=200, seed=None, out="demo.rou.xml", depart_end=3000):
    if seed is not None:
        random.seed(seed)
    header = ['<routes>',
              '  <vType id="car" accel="2.6" decel="4.5" length="4.5" maxSpeed="13.9"/>']
    for rid, edges in ROUTES.items():
        header.append(f'  <route id="{rid}" edges="{edges}"/>')
    lines = []
    for i in range(nvehicles):
        rid = random.choice(list(ROUTES.keys()))
        depart = round(random.random()*depart_end, 2)
        lines.append(f'  <vehicle id="veh_{i}" type="car" route="{rid}" depart="{depart}"/>')
    footer = ['</routes>']
    with open(out, 'w', encoding='utf8') as f:
        f.write('\n'.join(header + lines + footer))
    print(f"Wrote {out} ({nvehicles} vehicles, seed={seed}) at {datetime.datetime.now()}")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("--vehicles", "-n", type=int, default=200)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--out", default="demo.rou.xml")
    args = p.parse_args()
    generate(nvehicles=args.vehicles, seed=args.seed, out=args.out)
