🇩🇪 [Deutsche Version](aufbau.md)

# Assembly and commissioning (on the bench)

Basis: [`plaene/tank-bestueckung.pdf`](../plaene/tank-bestueckung.pdf) (top view 2:1) and
[`plaene/tankmessung-schaltplan.pdf`](../plaene/tankmessung-schaltplan.pdf). Pin assignment: [README, section 4](../README.en.md#4-pin-assignment-and-wiring).

## 1. Preparation

1. Print box and lid (`gehaeuse/tank_box.stl`, `tank_deckel.stl`; PETG or PLA, 0.2 mm, no supports).
2. Pump: solder the red and black wires to the solder tabs (red = +).
3. Have the flyback diode 1N5819 ready – it goes **into the OUT terminals** of the MOSFET module together with the wires, stripe (cathode) to OUT+.
4. Flash the firmware beforehand (see README, section 6) – once installed, the USB port is still reachable, but tight.

## 2. Assembly (order according to the assembly plan)

1. **Dupont cables first** onto the ESP32 and HX710B – later there is no room for fingers under the boards.
2. Place the **ESP32** on the 4 standoffs, USB-C on the left into the wall opening. Pigtail onto U.FL, SMA socket into the front wall to the right of the divider.
3. **HX710B** with hot glue onto its 2 standoffs, pin header to the **front**, hose barb pointing **up**.
4. **MOSFET module** front right with 1 cable tie, terminals towards the middle. Diode 1N5819: stripe to OUT+.
5. **Pump** at the back with 2 cable ties, ports to the right. Outlet port → check valve (arrow towards the T), leave the **inlet port open**.
6. **Check valve** on the right with 1 cable tie, aquarium T below it: one outlet to the HX710B barb (2.5 mm silicone), one through the right wall to the measuring line.
7. Tidy up the cables, push on the lid.

## 3. Commissioning

| Step | Expectation | If not |
|---|---|---|
| Plug in the USB power supply (≥ 1 A) | Device `Öltank` (oil tank) online in HA, `sensor.oltank_wlan_signal` (Wi-Fi signal) has a value | Fallback hotspot `Tank-Fallback` → captive portal |
| Wait ≥ 5 min | Sensor warm (zero point drifts ~0.5 mbar in the first minutes) | – |
| Hose end open, `button.oltank_messung_starten` (start measurement) | Pump audibly runs for 30 s, air blows out of the hose end; afterwards `sensor.oltank_druck` (pressure) ≈ 0 mbar | Fault pattern "pump does not run" in [fehlersuche.en.md](fehlersuche.en.md) |
| Hose end 10 cm into a glass of water | bubbles; pressure ≈ 9.8–10.5 mbar | see [einmessen.en.md](einmessen.en.md) |

> ⚠️ **Never pump with closed hose ends.** The pump manages 80–120 kPa, the sensor only tolerates 0–40 kPa.
> When testing, always have an open end or a water column it can bubble out into.

Result on 08.10.2026: function in the box ✔ (10.44/10.53 mbar at 10 cm water, 10 s settling, 3.5 min after switching on).
