🇩🇪 [Deutsche Version](fehlersuche.md)

# Troubleshooting

Known fault patterns from the project history (04.–08.10.2026).

| Fault pattern | Cause | Solution | confirmed? |
|---|---|---|---|
| Pump does not run, only ~0.86 V at the module output (VIN 4.77 V) | probably a **terminal contact** on the MOSFET module | Re-insert wires and diode into the terminals, tighten; afterwards it ran at 70 % | Cause **not** confirmed (08.10. 15:21–15:33) |
| MOSFET module does not switch at 5 V / only half | **D4184 module with PC817 optocoupler**: gate is supplied from the load voltage via 2 × 4.7 kΩ → gate = 50 % of the supply, only switches from ~6 V; PC817 too slow for 20 kHz; no flyback diode | Dual MOSFET module **without** optocoupler (CQUANZX B07VRCXGFY) + 1N5819 | confirmed (datasheet analysis + reviews, 06.10.) |
| Pressure does not build up / value too low, falling | **Leak at the branch to the old gauge**: check valve used as a plug leaks from ~10 mbar | Seal the branch firmly; leak test with 60 s settling time | confirmed (08.10., held shut → bubbles, value correct) |
| One-off drop in the leak test (10.44 → 6.65/6.47 mbar after 60 s) | unexplained – presumably push-fit connections settled after assembly | Repeat the run; two subsequent runs were tight | **not** confirmed |
| Zero point drifts in the first minutes (~38,500 raw ≈ 0.55 mbar ≈ 7 mm oil) | Sensor warming up (suspected) | wait ≥ 5 min before calibrating | Drift measured, cause suspected |
| Pressure near the raw-value limit / > 150 mbar | Measuring line blocked; pump pushes against a closed line | **abort immediately** (sensor only 0–40 kPa, pump 80–120 kPa); have the line blown clear | Limit from calculation |
| Pumping against closed hose ends | Operator error while testing | never pump without an open end / water column | Rule |
| Cross-check shows somewhat above 9.81 mbar (e.g. 10.0–10.8) | Immersion depth by hand inaccurate (+1 mm ≈ +0.1 mbar) | none – tolerance of the method | confirmed |
| Flashing aborts with "No more data to read" | this board does not handle 460800 baud | `esptool … --baud 115200` with `firmware.factory.bin` | confirmed (06.10.) |
| Fallback hotspot does not accept the password / API key wrong | Test build with dummy secrets flashed (on the sister device 06.10.) | only `esphome run` with real secrets; `esphome upload` does **not** recompile | confirmed |
| USB port locked after re-plugging (Linux) | `/dev/ttyUSB0` is recreated, the permission is gone | repeat `setfacl -m u:$USER:rw /dev/ttyUSB0` or use group `dialout` | confirmed |
| Values do not change | Sensor is only read during the measurement (`update_interval: never`), automatic mode off by default | press `Messung starten` ("Start measurement") or switch on automatic mode | Configuration |
| Old gauge was stuck at ~800 l with an empty tank | Measuring line silted up; sludge/water at the bottom heavier than oil → pneumatically too high | Blow the line clear (specialist company), dipstick comparison | Interpretation unconfirmed |

## Check steps for implausible values

1. Look at `sensor.oltank_druck_rohwert` (pressure raw value): the two readings per measurement are normally ~100–300 apart.
2. Pull the hose off the box, `Messung starten` ("Start measurement") → pressure must be ~0 mbar (otherwise redo the zero point, see [einmessen.en.md](einmessen.en.md)).
3. Glass test with 10 cm of water → ~9.8–10.5 mbar.
4. Leak test with 60 s settling time.
5. Only then suspect the line to the tank.
