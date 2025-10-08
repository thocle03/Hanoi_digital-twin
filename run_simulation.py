#!/usr/bin/env python3
"""Lance SUMO via TraCI et affiche les statistiques simples."""
import os, csv
import traci

USE_GUI = os.environ.get('SUMO_GUI','0') not in ('0', '', None)
sumo_binary = "sumo-gui" if USE_GUI else "sumo"
# ...existing code...
config = "c:/Users/thoma/OneDrive/Bureau/Hanoi_digital-twin/demo.sumocfg"
# ...existing code...

sumo_cmd = [sumo_binary, "-c", config]
print("Starting SUMO:", ' '.join(sumo_cmd))
traci.start(sumo_cmd)
step = 0
out_csv = "simulation_output.csv"

with open(out_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['step','n_vehicles','avg_speed_m_s'])
    try:
        while step < 3600:
            traci.simulationStep()
            if step % 60 == 0:
                veh_ids = traci.vehicle.getIDList()
                n = len(veh_ids)
                avg_speed = 0.0
                if n>0:
                    avg_speed = sum(traci.vehicle.getSpeed(v) for v in veh_ids)/n
                print(f"Step {step}: vehicles={n} avg_speed={avg_speed:.2f} m/s")
                writer.writerow([step, n, round(avg_speed,3)])
            step += 1
    except KeyboardInterrupt:
        print("Simulation interrompue.")
    finally:
        traci.close()
        print(f"Résultats dans {out_csv}")
